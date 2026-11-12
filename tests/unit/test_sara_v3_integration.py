import json
import os

import pytest

from conversation_verification import ConversationLedger
from runtime import CognitiveRuntime
from sara_integration import (
    SARAConnection,
    SARAv3Connection,
    SARAv3Error,
    SubprocessSARAv3Runner,
    default_sara_v3_root,
)

SECRET = "sk-test-secret-value"
USER_TEXT = "Our city's 2025 mask policy cut cases by 20 percent, right?"
ASSISTANT_TEXT = "The policy reduced cases by 20 percent."


class FakeV24Adapter:
    def evaluate(self, payload):
        return {"claim_id": payload["claim"]["id"], "verification_status": "UNVERIFIED", "is_evidence": False}


def envelope(claim_id="K1", status="VERIFIED"):
    return {
        "schema_version": "sara.assessment.v3", "claim_id": claim_id,
        "verification_status": status, "workflow_status": "PROPOSED",
        "truthfulness_status": "UNASSESSED", "is_evidence": False,
        "evidence_refs": ["E1"], "uncertainty": ["TRUSTED_FULL_TEXT_SUPPORTS_CLAIM"],
    }


def sara_result(*envelopes, **extra):
    return {
        "schema_version": "sara.dialogue-result.v3", "runtime_revision": "sara-v3-runtime-0.1",
        "verification_status": envelopes[0]["verification_status"] if envelopes else "NOT_ASSESSED",
        "assessment_envelopes": list(envelopes), "external_llm_response": None,
        "truthfulness_status": "UNASSESSED", "is_evidence": False, **extra,
    }


class RecordingSARA:
    """Fake SARA v3: by default returns one VERIFIED envelope per sent claim."""

    def __init__(self, result=None, error=None, fail_on_call=None):
        self.turns = []
        self.result = result
        self.error = error
        self.fail_on_call = fail_on_call

    def __call__(self, turn, timeout_seconds):
        assert timeout_seconds > 0
        self.turns.append(json.loads(json.dumps(turn)))
        if self.error and (self.fail_on_call is None or self.fail_on_call == len(self.turns)):
            raise self.error
        if self.result is not None:
            return self.result
        return sara_result(*[envelope(item["id"]) for item in turn["claim_candidates"]])


class Backend:
    def __init__(self, echo=None, claims=None, user_claims=None):
        self.requests = []
        self.echo = echo
        self.claims = claims
        self.user_claims = user_claims

    def generate(self, request):
        self.requests.append(request)
        output = {
            "execution_id": "EXEC-1", "status": "SUCCEEDED", "mode": request["mode"],
            "response": ASSISTANT_TEXT,
            "claims": self.claims if self.claims is not None else [
                {"id": "C1", "text": ASSISTANT_TEXT, "verification_status": "VERIFIED"}],
            "epistemic_states": ["FACT"], "reasoning_artifact": {},
        }
        if self.user_claims is not None:
            output["user_claims"] = self.user_claims
        if self.echo is not None:
            output["sara_assessment_envelopes"] = self.echo
        return output


def runtime(backend, sara, **kwargs):
    connection = sara if isinstance(sara, SARAv3Connection) else SARAv3Connection(sara)
    return CognitiveRuntime(backend, sara_connection=SARAConnection(adapter=FakeV24Adapter()),
                            sara_v3_connection=connection, **kwargs)


def request(turn_id="TURN-1", task=USER_TEXT, user_claims=None, **extra):
    base = {"request_id": f"REQ-{turn_id}", "conversation_id": "CONV-1", "turn_id": turn_id,
            "task": task, "mode": "DEEP", "context": {"private_note": SECRET}, **extra}
    if user_claims is not None:
        base["user_claims"] = user_claims
    return base


USER_CLAIM = [{"id": "U1", "text": "The 2025 mask policy cut cases by 20 percent."}]


def verify(rt, conversation_id="CONV-1", **selection):
    plan = rt.plan_conversation_verification(conversation_id, **selection)
    return plan, rt.verify_conversation(conversation_id, confirmation=plan["plan_id"], **selection)


# --- Nothing is sent during the conversation -------------------------------------------------

def test_turns_are_recorded_but_nothing_is_sent_per_turn():
    sara = RecordingSARA()
    result = runtime(Backend(), sara).run(request(user_claims=USER_CLAIM))
    assert sara.turns == []
    assert "sara_v3_assessment" not in result
    status = result["conversation_verification"]
    assert status["status"] == "NOT_REQUESTED"
    assert status["verification_status"] == "UNVERIFIED"
    assert status["recorded_claim_refs"] == ["TURN-1:USER:U1", "TURN-1:ASSISTANT:C1"]
    assert result["verification_status"] == "UNVERIFIED"
    assert result["claims"][0]["verification_status"] == "UNVERIFIED"


def test_nothing_is_recorded_or_offered_unless_v3_is_configured():
    rt = CognitiveRuntime(Backend(), sara_connection=SARAConnection(adapter=FakeV24Adapter()))
    result = rt.run(request(user_claims=USER_CLAIM))
    assert "conversation_verification" not in result
    assert rt.conversation_ledger.turns("CONV-1") == []
    with pytest.raises(RuntimeError, match="SARA_V3_NOT_CONFIGURED"):
        rt.plan_conversation_verification("CONV-1")


# --- Plan, preview and confirmation ----------------------------------------------------------

def test_plan_previews_the_exact_send_scope_without_sending():
    sara = RecordingSARA()
    rt = runtime(Backend(), sara)
    rt.run(request("TURN-1", user_claims=USER_CLAIM))
    rt.run(request("TURN-2", task="Thanks."))  # no user claims: the user utterance is not sent
    plan = rt.plan_conversation_verification("CONV-1")
    assert sara.turns == []
    preview = plan["preview"]
    assert preview["provider_calls"] == 3
    assert preview["turn_ids_sent"] == ["TURN-1", "TURN-2"]
    assert preview["claims_by_role"] == {"USER": 1, "ASSISTANT": 2}
    assert preview["content_chars_sent"] == len(USER_TEXT) + 2 * len(ASSISTANT_TEXT)
    assert preview["context_forwarded"] is False
    assert preview["identifiers"] == "PSEUDONYMIZED_PER_RUN"
    assert preview["send_unit"] == "ONE_UTTERANCE_BODY_PER_CALL"
    assert plan["plan_id"] == rt.plan_conversation_verification("CONV-1")["plan_id"]


def test_verification_requires_the_current_plan_id():
    sara = RecordingSARA()
    rt = runtime(Backend(), sara)
    rt.run(request("TURN-1", user_claims=USER_CLAIM))
    with pytest.raises(PermissionError, match="VERIFICATION_PLAN_NOT_CONFIRMED"):
        rt.verify_conversation("CONV-1", confirmation="cvp-guess")
    stale = rt.plan_conversation_verification("CONV-1")["plan_id"]
    rt.run(request("TURN-2"))
    with pytest.raises(PermissionError, match="VERIFICATION_PLAN_NOT_CONFIRMED"):
        rt.verify_conversation("CONV-1", confirmation=stale)
    narrowed = rt.plan_conversation_verification("CONV-1", turn_ids=["TURN-2"])["plan_id"]
    with pytest.raises(PermissionError, match="VERIFICATION_PLAN_NOT_CONFIRMED"):
        rt.verify_conversation("CONV-1", confirmation=narrowed)  # confirmed a different selection
    assert sara.turns == []


def test_unknown_conversation_turn_or_claim_is_rejected():
    rt = runtime(Backend(), RecordingSARA())
    with pytest.raises(ValueError, match="CONVERSATION_NOT_RECORDED"):
        rt.plan_conversation_verification("CONV-X")
    rt.run(request())
    with pytest.raises(ValueError, match="TURN_NOT_RECORDED"):
        rt.plan_conversation_verification("CONV-1", turn_ids=["TURN-9"])
    with pytest.raises(ValueError, match="CLAIM_REF_NOT_RECORDED"):
        rt.plan_conversation_verification("CONV-1", claim_refs=["TURN-1:USER:U9"])
    with pytest.raises(ValueError, match="TURN_IDS_INVALID"):
        rt.plan_conversation_verification("CONV-1", turn_ids="TURN-1")


# --- What each SARA call carries --------------------------------------------------------------

def test_each_call_carries_one_utterance_body_and_its_claims_only():
    sara = RecordingSARA()
    rt = runtime(Backend(), sara)
    rt.run(request("TURN-1", user_claims=USER_CLAIM))
    rt.run(request("TURN-2", task="A second, unrelated question about tax law?",
                   user_claims=[{"id": "U1", "text": "Tax law changed in 2026."}]))
    verify(rt)

    assert [turn["content"] for turn in sara.turns] == [
        USER_TEXT, ASSISTANT_TEXT, "A second, unrelated question about tax law?", ASSISTANT_TEXT]
    for turn in sara.turns:
        assert set(turn) == {"request_id", "conversation_id", "turn_id", "content",
                             "claim_candidates", "evidence", "provenance_ids"}
        assert turn["evidence"] == []
        assert SECRET not in json.dumps(turn)
    assert "tax law" not in json.dumps(sara.turns[:2]).lower()
    assert sara.turns[0]["claim_candidates"] == [{"id": "K1", "text": USER_CLAIM[0]["text"]}]


def test_identifiers_sent_to_sara_are_per_run_pseudonyms():
    sara = RecordingSARA()
    rt = runtime(Backend(), sara)
    rt.run(request("TURN-1", user_claims=USER_CLAIM))
    verify(rt)
    first_run = sara.turns[:]
    sent = json.dumps(first_run)
    for real in ("CONV-1", "TURN-1", "REQ-TURN-1", "EXEC-1", "\"U1\"", "\"C1\""):
        assert real not in sent
    assert {turn["conversation_id"] for turn in first_run} == {first_run[0]["conversation_id"]}
    verify(rt)
    assert sara.turns[-1]["conversation_id"] != first_run[0]["conversation_id"]


def test_claims_beyond_the_per_call_limit_are_split_into_batches():
    sara = RecordingSARA()
    claims = [{"id": f"C{i}", "text": f"Claim number {i}."} for i in range(10)]
    rt = runtime(Backend(claims=claims), SARAv3Connection(sara, max_claims=8))
    rt.run(request())
    plan, result = verify(rt)
    assert [len(turn["claim_candidates"]) for turn in sara.turns] == [8, 2]
    assert sara.turns[0]["content"] == sara.turns[1]["content"] == ASSISTANT_TEXT
    assert result["coverage"] == {"claims_total": 10, "claims_assessed": 10,
                                  "claims_not_required_by_sara": 0, "claims_not_assessed": 0}


def test_identical_claims_within_one_utterance_are_sent_once():
    sara = RecordingSARA()
    claims = [{"id": "C1", "text": "Same  claim."}, {"id": "C2", "text": "Same claim."}]
    rt = runtime(Backend(claims=claims), sara)
    rt.run(request())
    verify(rt)
    assert sara.turns[0]["claim_candidates"] == [{"id": "K1", "text": "Same claim."}]


def test_selection_limits_the_send_scope():
    sara = RecordingSARA()
    rt = runtime(Backend(), sara)
    rt.run(request("TURN-1", user_claims=USER_CLAIM))
    rt.run(request("TURN-2", user_claims=USER_CLAIM))
    plan, result = verify(rt, turn_ids=["TURN-2"])
    assert plan["preview"]["turn_ids_sent"] == ["TURN-2"]
    assert {item["turn_id"] for item in result["claim_results"]} == {"TURN-2"}
    sara.turns.clear()
    plan, result = verify(rt, claim_refs=["TURN-1:USER:U1"])
    assert len(sara.turns) == 1 and sara.turns[0]["content"] == USER_TEXT
    assert [item["claim_ref"] for item in result["claim_results"]] == ["TURN-1:USER:U1"]


# --- Results ------------------------------------------------------------------------------------

def test_results_map_back_to_turns_roles_and_claims():
    rt = runtime(Backend(), RecordingSARA())
    rt.run(request(user_claims=USER_CLAIM))
    plan, result = verify(rt)
    assert result["execution_status"] == "SUCCEEDED"
    assert [(item["claim_ref"], item["sara_claim_id"], item["status"], item["sara_verification_status"])
            for item in result["claim_results"]] == [
        ("TURN-1:USER:U1", "K1", "ASSESSED", "VERIFIED"),
        ("TURN-1:ASSISTANT:C1", "K2", "ASSESSED", "VERIFIED")]
    # SARA's statuses stay inside the report; Co-thoughts itself does not promote anything.
    assert result["verification_status"] == "UNVERIFIED"
    assert result["is_evidence"] is False
    assert [item["claim_id"] for item in result["assessment_envelopes"]] == ["K1", "K2"]


def test_sara_that_assesses_nothing_is_reported_not_silent():
    silent = sara_result(activation_decision={"reason_code": "JUDGMENT_UNAVAILABLE_OR_INVALID"},
                         external_llm_response={"error_code": "LLM_PROVIDER_HTTP_ERROR_400"})
    rt = runtime(Backend(), RecordingSARA(result=silent))
    rt.run(request())
    plan, result = verify(rt)
    assert result["execution_status"] == "SUCCEEDED"
    assert result["coverage"] == {"claims_total": 1, "claims_assessed": 0,
                                  "claims_not_required_by_sara": 0, "claims_not_assessed": 1}
    assert result["claim_results"][0]["status"] == "NOT_ASSESSED"
    assert result["claim_results"][0]["reason_codes"] == ["JUDGMENT_UNAVAILABLE_OR_INVALID",
                                                         "LLM_PROVIDER_HTTP_ERROR_400"]


def test_sara_deciding_no_verification_is_reported_separately_from_failure():
    no_trigger = sara_result(activation_decision={
        "activation_action": "NO_INFERENCE_TRIGGER", "activation_triggered": False,
        "reason_code": "NO_INFERENCE_DETECTED_WITH_HIGH_CONFIDENCE"})
    rt = runtime(Backend(), RecordingSARA(result=no_trigger))
    rt.run(request())
    plan, result = verify(rt)
    assert result["coverage"] == {"claims_total": 1, "claims_assessed": 0,
                                  "claims_not_required_by_sara": 1, "claims_not_assessed": 0}
    claim = result["claim_results"][0]
    assert claim["status"] == "NOT_REQUIRED_BY_SARA"
    assert claim["reason_codes"] == ["NO_INFERENCE_DETECTED_WITH_HIGH_CONFIDENCE"]
    assert result["batches"][0]["sara_activation_action"] == "NO_INFERENCE_TRIGGER"
    assert result["verification_status"] == "UNVERIFIED"


@pytest.mark.parametrize("decision", [
    {"activation_action": "NO_INFERENCE_TRIGGER", "activation_triggered": True},
    {"activation_action": "NO_INFERENCE_TRIGGER"},
    {"activation_action": "SARA_PRECHECK_REVIEW", "activation_triggered": True,
     "reason_code": "JUDGMENT_CONFIDENCE_NOT_HIGH"},
    {"activation_action": "no trigger, trust me", "activation_triggered": False},
])
def test_anything_short_of_a_consistent_no_trigger_stays_not_assessed(decision):
    rt = runtime(Backend(), RecordingSARA(result=sara_result(activation_decision=decision)))
    rt.run(request())
    plan, result = verify(rt)
    assert result["claim_results"][0]["status"] == "NOT_ASSESSED"
    assert result["coverage"]["claims_not_required_by_sara"] == 0


def test_one_failing_batch_does_not_stop_the_others_and_is_sanitized():
    sara = RecordingSARA(error=RuntimeError(f"Authorization: Bearer {SECRET}"), fail_on_call=1)
    rt = runtime(Backend(), sara)
    rt.run(request(user_claims=USER_CLAIM))
    plan, result = verify(rt)
    assert result["execution_status"] == "PARTIALLY_FAILED"
    assert [b["execution_status"] for b in result["batches"]] == ["FAILED", "SUCCEEDED"]
    assert result["batches"][0]["error_code"] == "RUNTIMEERROR"
    assert result["claim_results"][0]["status"] == "NOT_ASSESSED"
    assert result["claim_results"][0]["reason_codes"] == ["RUNTIMEERROR"]
    assert result["claim_results"][1]["status"] == "ASSESSED"
    assert SECRET not in json.dumps(result)


@pytest.mark.parametrize("result, code", [
    ({"schema_version": "other"}, "SARA_V3_RESULT_INVALID"),
    (sara_result(envelope(claim_id="K-UNSENT")), "SARA_V3_ENVELOPE_CLAIM_NOT_SENT"),
    ({**sara_result(envelope()), "truthfulness_status": "TRUE"}, "SARA_V3_RESULT_INVALID"),
])
def test_invalid_sara_result_is_rejected(result, code):
    rt = runtime(Backend(), RecordingSARA(result=result))
    rt.run(request())
    plan, report = verify(rt)
    assert report["execution_status"] == "FAILED"
    assert report["batches"][0]["error_code"] == code
    assert report["assessment_envelopes"] == []


def test_missing_sara_checkout_reports_not_connected():
    connection = SARAv3Connection(root="C:/path/that/does/not/exist")
    assert connection.connected is False
    assert connection.connection_error == "SARA_V3_CLI_NOT_FOUND"
    rt = runtime(Backend(), connection)
    rt.run(request())
    plan, result = verify(rt)
    assert result["execution_status"] == "NOT_CONNECTED"
    assert result["connection_error"] == "SARA_V3_CLI_NOT_FOUND"


def test_no_claims_means_nothing_to_send():
    sara = RecordingSARA()
    rt = runtime(Backend(claims=[]), sara)
    rt.run(request())
    plan, result = verify(rt)
    assert plan["preview"]["provider_calls"] == 0
    assert result["execution_status"] == "NOT_APPLICABLE"
    assert sara.turns == []


# --- User claims -------------------------------------------------------------------------------

def test_backend_extracted_user_claims_are_used_when_host_gives_none():
    rt = runtime(Backend(user_claims=[{"text": "Cases fell by a fifth."}]), RecordingSARA())
    result = rt.run(request())
    assert result["conversation_verification"]["recorded_claim_refs"][0] == "TURN-1:USER:UC-1"


def test_host_user_claims_take_precedence_over_backend_ones():
    rt = runtime(Backend(user_claims=[{"id": "B1", "text": "Backend view."}]), RecordingSARA())
    result = rt.run(request(user_claims=USER_CLAIM))
    assert "TURN-1:USER:U1" in result["conversation_verification"]["recorded_claim_refs"]
    assert not any(":B1" in ref for ref in result["conversation_verification"]["recorded_claim_refs"])


def test_malformed_backend_user_claims_do_not_fail_the_turn():
    rt = runtime(Backend(user_claims="not-a-list"), RecordingSARA())
    result = rt.run(request())
    assert result["status"] == "SUCCEEDED"
    assert result["conversation_verification"]["warnings"] == ["BACKEND_USER_CLAIMS_INVALID"]


@pytest.mark.parametrize("bad", ["x", [{"id": "U1"}], [{"text": "  "}], ["plain"]])
def test_malformed_host_user_claims_are_rejected_before_backend_call(bad):
    backend = Backend()
    with pytest.raises(ValueError, match="USER_CLAIMS_INVALID"):
        runtime(backend, RecordingSARA()).run(request(user_claims=bad))
    assert backend.requests == []


def test_user_claims_reach_the_record_through_workflow_paths():
    sara = RecordingSARA()
    rt = runtime(Backend(), sara)
    via_workflow = rt.run_workflow("problem_diagnosis", request("TURN-1", user_claims=USER_CLAIM))
    via_language = rt.run_natural_language(request("TURN-2", task="잠정 해결안을 제안해줘", user_claims=USER_CLAIM))
    assert via_workflow["workflow"]["name"] == "problem_diagnosis"
    assert via_language["workflow"]["name"] == "solution_design"
    for result, turn in ((via_workflow, "TURN-1"), (via_language, "TURN-2")):
        assert result["conversation_verification"]["recorded_claim_refs"] == [
            f"{turn}:USER:U1", f"{turn}:ASSISTANT:C1"]
    plan, report = verify(rt)
    assert [turn["content"] for turn in sara.turns if turn["turn_id"].endswith("-u")] == [
        USER_TEXT, "잠정 해결안을 제안해줘"]
    assert report["coverage"]["claims_not_assessed"] == 0


# --- User-cited source URLs ---------------------------------------------------------------

PRESS = "https://www.korea.kr/news/policyNewsView.do?newsId=148975578"
STATS = "https://doi.org/10.1101/2021.05.18.21257385"


def test_user_cited_urls_go_only_with_their_own_utterance():
    sara = RecordingSARA()
    rt = runtime(Backend(), sara)
    rt.run(request("TURN-1", user_claims=[{"id": "U1", "text": USER_CLAIM[0]["text"],
                                           "source_urls": [PRESS, STATS, PRESS]}]))
    plan, result = verify(rt)
    assert plan["preview"]["source_urls_sent"] == 2
    user_call, assistant_call = sara.turns
    assert user_call["evidence"] == [
        {"id": "S1", "url": PRESS, "snippet": "USER_SUPPLIED_SOURCE_URL"},
        {"id": "S2", "url": STATS, "snippet": "USER_SUPPLIED_SOURCE_URL"}]
    assert assistant_call["evidence"] == []
    assert result["batches"][0]["sent_scope"]["source_urls"] == 2


def test_backend_supplied_urls_are_never_forwarded():
    sara = RecordingSARA()
    backend = Backend(claims=[{"id": "C1", "text": ASSISTANT_TEXT, "source_urls": [PRESS]}],
                      user_claims=[{"text": "Cases fell by a fifth.", "source_urls": [STATS]}])
    rt = runtime(backend, sara)
    rt.run(request())
    plan, _ = verify(rt)
    assert plan["preview"]["source_urls_sent"] == 0
    assert all(turn["evidence"] == [] for turn in sara.turns)


@pytest.mark.parametrize("urls", [
    "https://www.korea.kr/x",                          # not a list
    ["http://www.korea.kr/x"],                         # not https
    ["https://user:pw@www.korea.kr/x"],                # credentials
    ["https://www.korea.kr/x#top"],                    # fragment
    ["https://www.korea.kr:8443/x"],                   # non-default port
    ["https://www.korea.kr/a b"],                      # whitespace
    ["https:///nohost"],                               # no host
    [f"https://www.korea.kr/{i}" for i in range(6)],   # more than five
    [7],
])
def test_invalid_user_source_urls_are_rejected_before_backend_call(urls):
    backend = Backend()
    with pytest.raises(ValueError, match="USER_CLAIMS_INVALID"):
        runtime(backend, RecordingSARA()).run(
            request(user_claims=[{"id": "U1", "text": "x", "source_urls": urls}]))
    assert backend.requests == []


def test_repeated_claim_text_merges_its_citations_and_validates_every_copy():
    sara = RecordingSARA()
    rt = runtime(Backend(), sara)
    rt.run(request(user_claims=[{"id": "U1", "text": "Same claim.", "source_urls": [PRESS]},
                                {"id": "U2", "text": "Same  claim.", "source_urls": [STATS, PRESS]}]))
    verify(rt)
    assert sara.turns[0]["claim_candidates"] == [{"id": "K1", "text": "Same claim."}]
    assert [item["url"] for item in sara.turns[0]["evidence"]] == [PRESS, STATS]
    for dupes in ([{"text": "Same claim."}, {"text": "Same claim.", "source_urls": ["http://bad.example"]}],
                  [{"text": "Same claim.", "source_urls": [f"https://www.korea.kr/{i}" for i in range(3)]},
                   {"text": "Same claim.", "source_urls": [f"https://www.korea.kr/x{i}" for i in range(3)]}]):
        backend = Backend()
        with pytest.raises(ValueError, match="USER_CLAIMS_INVALID"):
            runtime(backend, RecordingSARA()).run(request(user_claims=dupes))
        assert backend.requests == []


def test_too_many_urls_in_one_call_is_refused_at_planning():
    claims = [{"id": f"U{i}", "text": f"Claim {i}.",
               "source_urls": [f"https://www.korea.kr/{i}-{j}" for j in range(5)]} for i in range(3)]
    rt = runtime(Backend(), RecordingSARA())
    rt.run(request(user_claims=claims))
    with pytest.raises(ValueError, match="SOURCE_URLS_PER_CALL_EXCEEDED"):
        rt.plan_conversation_verification("CONV-1")
    narrowed = rt.plan_conversation_verification("CONV-1", claim_refs=["TURN-1:USER:U0", "TURN-1:USER:U1"])
    assert narrowed["preview"]["source_urls_sent"] == 10


def test_changing_cited_urls_changes_the_plan_id():
    rt = runtime(Backend(), RecordingSARA())
    rt.run(request(user_claims=[{"id": "U1", "text": "x", "source_urls": [PRESS]}]))
    first = rt.plan_conversation_verification("CONV-1")["plan_id"]
    rt.run(request(user_claims=[{"id": "U1", "text": "x", "source_urls": [STATS]}]))
    assert rt.plan_conversation_verification("CONV-1")["plan_id"] != first


# --- Ledger -------------------------------------------------------------------------------------

def test_retried_turn_replaces_its_record():
    rt = runtime(Backend(), RecordingSARA())
    rt.run(request("TURN-1"))
    rt.run(request("TURN-1", user_claims=USER_CLAIM))
    plan = rt.plan_conversation_verification("CONV-1")
    assert plan["preview"]["turns_recorded"] == 1
    assert plan["preview"]["claims_by_role"] == {"USER": 1, "ASSISTANT": 1}


def test_evicted_turns_are_reported_in_the_plan():
    rt = runtime(Backend(), RecordingSARA(), conversation_ledger=ConversationLedger(max_turns_per_conversation=2))
    for index in range(3):
        rt.run(request(f"TURN-{index}"))
    preview = rt.plan_conversation_verification("CONV-1")["preview"]
    assert preview["turns_recorded"] == 2
    assert preview["turns_evicted_before_plan"] == 1


# --- Carried envelopes stay authoritative ----------------------------------------------------

def test_envelopes_round_trip_to_the_next_backend_call():
    backend = Backend()
    rt = runtime(backend, RecordingSARA())
    rt.run(request("TURN-1"))
    carried = verify(rt)[1]["assessment_envelopes"]
    second = rt.run(request("TURN-2", sara_assessment_envelopes=carried))
    assert backend.requests[1]["sara_assessment_envelopes"] == carried
    assert second["sara_assessment_envelopes"] == carried
    assert second["sara_envelope_integrity"] == "PRESERVED"


def test_backend_cannot_rewrite_carried_envelopes():
    carried = [envelope(status="UNVERIFIED")]
    tampered = [envelope(status="VERIFIED")]
    result = runtime(Backend(echo=tampered), RecordingSARA()).run(request(sara_assessment_envelopes=carried))
    assert result["sara_assessment_envelopes"] == carried
    assert result["sara_envelope_integrity"] == "BACKEND_MODIFICATION_DISCARDED"


def test_backend_cannot_fabricate_envelopes_without_prior_turn():
    result = runtime(Backend(echo=[envelope()]), RecordingSARA()).run(request())
    assert result["sara_assessment_envelopes"] == []
    assert result["sara_envelope_integrity"] == "BACKEND_MODIFICATION_DISCARDED"


@pytest.mark.parametrize("bad", [
    [{"claim_id": "C1", "verification_status": "VERIFIED", "is_evidence": False}],
    [{**envelope(), "is_evidence": True}],
    "not-a-list",
])
def test_invalid_carried_envelopes_are_rejected_before_backend_call(bad):
    backend = Backend()
    with pytest.raises(ValueError, match="SARA_ENVELOPES_INVALID"):
        runtime(backend, RecordingSARA()).run(request(sara_assessment_envelopes=bad))
    assert backend.requests == []


# --- Real SARA checkout ----------------------------------------------------------------------

SIBLING = (default_sara_v3_root() / "SARA_v3" / "cli.py").is_file()


@pytest.mark.skipif(not SIBLING, reason="Sibling SARA v3 checkout is not present")
def test_sibling_sara_v3_process_fails_closed_without_provider_configuration(monkeypatch):
    for var in [name for name in os.environ if name.startswith("SARA_")]:
        monkeypatch.delenv(var, raising=False)
    runner = SubprocessSARAv3Runner(default_sara_v3_root())
    with pytest.raises(SARAv3Error, match=r"^SARA_V3_[A-Z0-9_]+$"):
        runner({"request_id": "REQ-1", "conversation_id": "CONV-1", "turn_id": "TURN-1",
                "content": "x", "claim_candidates": [{"id": "C1", "text": "x"}], "evidence": []}, 5)


LIVE = os.environ.get("CO_THOUGHTS_SARA_V3_LIVE", "").strip() == "1"
# SARA starts verification only when its judgment finds an inference with HIGH confidence,
# so the live claim must contain one; a plain factual claim is legitimately skipped by SARA.
LIVE_INFERENCE = "Cases fell 20 percent after the mask policy started, so the mask policy caused the decline."


@pytest.mark.skipif(not (LIVE and SIBLING), reason="set CO_THOUGHTS_SARA_V3_LIVE=1 with SARA_LLM_* configured")
def test_live_conversation_verification_round_trip():
    backend = Backend(claims=[{"id": "C1", "text": LIVE_INFERENCE}])
    rt = CognitiveRuntime(backend, sara_v3_connection=SARAv3Connection())
    rt.run(request("TURN-1", task=LIVE_INFERENCE, user_claims=[{"id": "U1", "text": LIVE_INFERENCE}]))
    plan = rt.plan_conversation_verification("CONV-1")
    result = rt.verify_conversation("CONV-1", confirmation=plan["plan_id"])
    report = os.environ.get("CO_THOUGHTS_SARA_V3_LIVE_REPORT", "").strip()
    if report:
        with open(report, "w", encoding="utf-8") as handle:
            json.dump({"plan_preview": plan["preview"], "verification": result},
                      handle, ensure_ascii=False, indent=2, default=str)
    assert result["execution_status"] == "SUCCEEDED", result["batches"]
    # A run that assessed nothing (e.g. a provider error SARA absorbed) is not a passing round trip,
    # and at least one real envelope must exist so the carry-over leg below is exercised.
    assert result["coverage"]["claims_not_assessed"] == 0, result["claim_results"]
    assert result["coverage"]["claims_assessed"] >= 1, result["claim_results"]

    carried = result["assessment_envelopes"]
    second = rt.run(request("TURN-2", sara_assessment_envelopes=carried))
    assert backend.requests[1]["sara_assessment_envelopes"] == carried
    assert second["sara_assessment_envelopes"] == carried
    assert second["sara_envelope_integrity"] == "PRESERVED"
