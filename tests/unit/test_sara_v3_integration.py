import json
import os

import pytest

from runtime import CognitiveRuntime
from sara_integration import (
    SARAConnection,
    SARAv3Connection,
    SARAv3Error,
    SubprocessSARAv3Runner,
    default_sara_v3_root,
)

SECRET = "sk-test-secret-value"


class FakeV24Adapter:
    def evaluate(self, payload):
        return {"claim_id": payload["claim"]["id"], "verification_status": "UNVERIFIED", "is_evidence": False}


def envelope(claim_id="C1", status="VERIFIED"):
    return {
        "schema_version": "sara.assessment.v3", "claim_id": claim_id,
        "verification_status": status, "workflow_status": "PROPOSED",
        "truthfulness_status": "UNASSESSED", "is_evidence": False,
        "evidence_refs": ["E1"], "uncertainty": ["TRUSTED_FULL_TEXT_SUPPORTS_CLAIM"],
    }


def sara_result(*envelopes):
    return {
        "schema_version": "sara.dialogue-result.v3", "runtime_revision": "sara-v3-runtime-0.1",
        "verification_status": envelopes[0]["verification_status"] if envelopes else "NOT_ASSESSED",
        "assessment_envelopes": list(envelopes), "external_llm_response": None,
        "truthfulness_status": "UNASSESSED", "is_evidence": False,
    }


class RecordingSARA:
    def __init__(self, result=None, error=None):
        self.turns = []
        self.result = result
        self.error = error

    def __call__(self, turn, timeout_seconds):
        assert timeout_seconds > 0
        self.turns.append(turn)
        if self.error:
            raise self.error
        return self.result if self.result is not None else sara_result(envelope())


class Backend:
    def __init__(self, echo=None):
        self.requests = []
        self.echo = echo

    def generate(self, request):
        self.requests.append(request)
        output = {
            "execution_id": "EXEC-1", "status": "SUCCEEDED", "mode": request["mode"],
            "response": "The policy reduced cases by 20 percent.",
            "claims": [{"id": "C1", "text": "The policy reduced cases by 20 percent.",
                        "verification_status": "VERIFIED"}],
            "epistemic_states": ["FACT"], "reasoning_artifact": {},
        }
        if self.echo is not None:
            output["sara_assessment_envelopes"] = self.echo
        return output


def runtime(backend, sara):
    return CognitiveRuntime(backend, sara_connection=SARAConnection(adapter=FakeV24Adapter()),
                            sara_v3_connection=SARAv3Connection(sara))


def request(**extra):
    return {"request_id": "REQ-1", "conversation_id": "CONV-1", "turn_id": "TURN-1",
            "task": "Summarize the policy study.", "mode": "DEEP",
            "context": {"private_note": SECRET}, **extra}


def test_v3_receives_only_the_approved_turn_scope():
    sara = RecordingSARA()
    result = runtime(Backend(), sara).run(request())

    turn = sara.turns[0]
    assert set(turn) == {"request_id", "conversation_id", "turn_id", "content",
                         "claim_candidates", "evidence", "provenance_ids"}
    assert turn["claim_candidates"] == [{"id": "C1", "text": "The policy reduced cases by 20 percent."}]
    assert turn["content"] == "The policy reduced cases by 20 percent."
    assert turn["evidence"] == []
    assert SECRET not in json.dumps(turn)
    assert "Summarize the policy study." not in json.dumps(turn)
    assessment = result["sara_v3_assessment"]
    assert assessment["execution_status"] == "SUCCEEDED"
    assert assessment["sent_scope"] == {"claim_ids": ["C1"], "content_chars": len(turn["content"]),
                                        "context_forwarded": False}


def test_sara_status_stays_separate_from_cognitive_output():
    result = runtime(Backend(), RecordingSARA()).run(request())
    assert result["sara_v3_assessment"]["verification_status"] == "VERIFIED"
    assert result["sara_v3_assessment"]["assessment_envelopes"][0]["workflow_status"] == "PROPOSED"
    assert result["verification_status"] == "UNVERIFIED"
    assert result["claims"][0]["verification_status"] == "UNVERIFIED"
    assert result["is_evidence"] is False


def test_v3_is_not_called_unless_configured():
    result = CognitiveRuntime(Backend(), sara_connection=SARAConnection(adapter=FakeV24Adapter())).run(request())
    assert "sara_v3_assessment" not in result


def test_envelopes_round_trip_to_the_next_backend_call():
    sara = RecordingSARA()
    backend = Backend()
    rt = runtime(backend, sara)
    first = rt.run(request())
    carried = first["sara_v3_assessment"]["assessment_envelopes"]

    second = rt.run(request(turn_id="TURN-2", sara_assessment_envelopes=carried))
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


def test_sara_failure_is_fail_closed_and_sanitized():
    sara = RecordingSARA(error=RuntimeError(f"Authorization: Bearer {SECRET}"))
    assessment = runtime(Backend(), sara).run(request())["sara_v3_assessment"]
    assert assessment["execution_status"] == "FAILED"
    assert assessment["error_code"] == "RUNTIMEERROR"
    assert assessment["verification_status"] == "UNVERIFIED"
    assert SECRET not in json.dumps(assessment)


@pytest.mark.parametrize("result, code", [
    ({"schema_version": "other"}, "SARA_V3_RESULT_INVALID"),
    (sara_result(envelope(claim_id="C-UNSENT")), "SARA_V3_ENVELOPE_CLAIM_NOT_SENT"),
    ({**sara_result(envelope()), "truthfulness_status": "TRUE"}, "SARA_V3_RESULT_INVALID"),
])
def test_invalid_sara_result_is_rejected(result, code):
    assessment = runtime(Backend(), RecordingSARA(result=result)).run(request())["sara_v3_assessment"]
    assert assessment["execution_status"] == "FAILED"
    assert assessment["error_code"] == code
    assert assessment["assessment_envelopes"] == []


def test_claim_limit_keeps_v3_from_running():
    sara = RecordingSARA()
    connection = SARAv3Connection(sara, max_claims=1)

    class ManyClaims(Backend):
        def generate(self, request):
            output = super().generate(request)
            output["claims"] = [{"id": f"C{i}", "text": f"Claim {i}"} for i in range(2)]
            return output

    result = CognitiveRuntime(ManyClaims(), sara_connection=SARAConnection(adapter=FakeV24Adapter()),
                              sara_v3_connection=connection).run(request())
    assert result["sara_v3_assessment"]["execution_status"] == "NOT_RUN"
    assert result["sara_v3_assessment"]["error_code"] == "CLAIM_LIMIT_EXCEEDED"
    assert sara.turns == []


def test_missing_sara_checkout_reports_not_connected():
    connection = SARAv3Connection(root="C:/path/that/does/not/exist")
    assert connection.connected is False
    assessment = connection.assess_turn(request(), {"claims": [{"id": "C1", "text": "x"}]})
    assert assessment["execution_status"] == "NOT_CONNECTED"
    assert assessment["connection_error"] == "SARA_V3_CLI_NOT_FOUND"


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


@pytest.mark.skipif(not (LIVE and SIBLING), reason="set CO_THOUGHTS_SARA_V3_LIVE=1 with SARA_LLM_* configured")
def test_live_cothoughts_to_sara_v3_round_trip():
    backend = Backend()
    rt = CognitiveRuntime(backend, sara_v3_connection=SARAv3Connection())
    first = rt.run(request())
    assessment = first["sara_v3_assessment"]
    assert assessment["execution_status"] == "SUCCEEDED", assessment
    assert first["verification_status"] == "UNVERIFIED"

    carried = assessment["assessment_envelopes"]
    second = rt.run(request(turn_id="TURN-2", sara_assessment_envelopes=carried))
    assert backend.requests[1]["sara_assessment_envelopes"] == carried
    assert second["sara_assessment_envelopes"] == carried
    report = os.environ.get("CO_THOUGHTS_SARA_V3_LIVE_REPORT", "").strip()
    if report:
        with open(report, "w", encoding="utf-8") as handle:
            json.dump({"first_turn": assessment, "second_turn_integrity": second["sara_envelope_integrity"]},
                      handle, ensure_ascii=False, indent=2, default=str)
