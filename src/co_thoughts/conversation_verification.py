"""User-requested, whole-conversation independent verification through SARA v3.

During a conversation nothing is sent to SARA. The runtime only records, per
turn, the user utterance and the assistant response together with their claim
candidates. When the user asks for verification, the host first builds a plan
(a preview of exactly what would leave the process) and then runs it with the
plan id as the confirmation.

Send scope per SARA call: one utterance body (user or assistant) of one turn
and the claims taken from that utterance. Other turns, request context and
backend evidence are never attached. Identifiers sent to SARA are pseudonyms
generated per run; the mapping back to real turn and claim ids stays local.
"""

from __future__ import annotations

from collections import OrderedDict
import hashlib
import json
import secrets
from typing import Any, Iterable, Mapping

from sara_integration import SARAv3Connection, SARAv3Error, _ERROR_CODE, _validated_v3_result

ROLES = ("USER", "ASSISTANT")
RESULT_SCHEMA = "co-thoughts.conversation-verification.v1"
PLAN_SCHEMA = "co-thoughts.conversation-verification-plan.v1"


def normalize_claims(value: Any, *, prefix: str, error: str) -> list[dict[str, str]]:
    """Return [{id, text}] from a claim list; ids default to ``prefix-N``.

    Identical texts within one utterance are kept once.
    """
    if value is None:
        return []
    if not isinstance(value, (list, tuple)):
        raise ValueError(error)
    claims: list[dict[str, str]] = []
    seen_texts: set[str] = set()
    for index, item in enumerate(value):
        if not isinstance(item, Mapping):
            raise ValueError(error)
        text = item.get("text")
        if not isinstance(text, str) or not text.strip():
            raise ValueError(error)
        text = " ".join(text.split())
        if text in seen_texts:
            continue
        seen_texts.add(text)
        claim_id = item.get("id")
        claim_id = str(claim_id).strip() if claim_id is not None and str(claim_id).strip() else f"{prefix}-{index + 1}"
        claims.append({"id": claim_id, "text": text})
    return claims


class ConversationLedger:
    """In-memory record of turns, kept only while SARA v3 is configured.

    Bounded: the oldest turns of a conversation and the oldest conversations
    are evicted, and the eviction count is reported in every plan so that lost
    coverage is visible.
    """

    def __init__(self, *, max_turns_per_conversation: int = 500, max_conversations: int = 100) -> None:
        if max_turns_per_conversation <= 0 or max_conversations <= 0:
            raise ValueError("LEDGER_LIMIT_INVALID")
        self.max_turns = max_turns_per_conversation
        self.max_conversations = max_conversations
        self._conversations: OrderedDict[str, OrderedDict[str, dict[str, Any]]] = OrderedDict()
        self._evicted: dict[str, int] = {}

    def record(self, conversation_id: str, turn_id: str, utterances: Mapping[str, Mapping[str, Any]]) -> None:
        turns = self._conversations.get(conversation_id)
        if turns is None:
            turns = self._conversations[conversation_id] = OrderedDict()
            while len(self._conversations) > self.max_conversations:
                dropped, _ = self._conversations.popitem(last=False)
                self._evicted.pop(dropped, None)
        self._conversations.move_to_end(conversation_id)
        # A retried turn replaces its earlier record instead of adding a second one.
        turns.pop(turn_id, None)
        turns[turn_id] = json.loads(json.dumps({"turn_id": turn_id, "utterances": dict(utterances)}))
        while len(turns) > self.max_turns:
            turns.popitem(last=False)
            self._evicted[conversation_id] = self._evicted.get(conversation_id, 0) + 1

    def turns(self, conversation_id: str) -> list[dict[str, Any]]:
        return [json.loads(json.dumps(item)) for item in self._conversations.get(conversation_id, {}).values()]

    def evicted(self, conversation_id: str) -> int:
        return self._evicted.get(conversation_id, 0)


def claim_ref(turn_id: str, role: str, claim_id: str) -> str:
    return f"{turn_id}:{role}:{claim_id}"


def build_plan(
    ledger: ConversationLedger,
    conversation_id: str,
    *,
    max_claims_per_call: int,
    turn_ids: Iterable[str] | None = None,
    claim_refs: Iterable[str] | None = None,
) -> dict[str, Any]:
    """Describe exactly what a verification run would send, without sending it."""
    if not isinstance(conversation_id, str) or not conversation_id.strip():
        raise ValueError("CONVERSATION_ID_REQUIRED")
    turns = ledger.turns(conversation_id)
    if not turns and not ledger.evicted(conversation_id):
        raise ValueError("CONVERSATION_NOT_RECORDED")
    known_turns = {item["turn_id"] for item in turns}
    wanted_turns = _selection(turn_ids, "TURN_IDS_INVALID")
    if wanted_turns is not None and not wanted_turns <= known_turns:
        raise ValueError("TURN_NOT_RECORDED")
    wanted_refs = _selection(claim_refs, "CLAIM_REFS_INVALID")

    batches: list[dict[str, Any]] = []
    matched_refs: set[str] = set()
    for position, turn in enumerate(turns, start=1):
        if wanted_turns is not None and turn["turn_id"] not in wanted_turns:
            continue
        for role in ROLES:
            utterance = turn["utterances"].get(role)
            if not utterance:
                continue
            claims = []
            for claim in utterance["claims"]:
                ref = claim_ref(turn["turn_id"], role, claim["id"])
                if wanted_refs is not None and ref not in wanted_refs:
                    continue
                matched_refs.add(ref)
                claims.append({**claim, "claim_ref": ref})
            for start in range(0, len(claims), max_claims_per_call):
                batches.append({
                    "batch": len(batches) + 1, "turn_id": turn["turn_id"], "turn_position": position,
                    "role": role, "content": utterance["content"],
                    "claims": claims[start:start + max_claims_per_call],
                })
    if wanted_refs is not None and not wanted_refs <= matched_refs:
        raise ValueError("CLAIM_REF_NOT_RECORDED")

    sent_turns = sorted({item["turn_id"] for item in batches}, key=[t["turn_id"] for t in turns].index)
    preview = {
        "destination": "SARA_V3_EXTERNAL_PROVIDERS",
        "provider_calls": len(batches),
        "turns_sent": len(sent_turns),
        "turn_ids_sent": sent_turns,
        "claims_sent": sum(len(item["claims"]) for item in batches),
        "claims_by_role": {role: sum(len(b["claims"]) for b in batches if b["role"] == role) for role in ROLES},
        "content_chars_sent": sum(len(item["content"]) for item in batches),
        "send_unit": "ONE_UTTERANCE_BODY_PER_CALL",
        "context_forwarded": False,
        "identifiers": "PSEUDONYMIZED_PER_RUN",
        "turns_recorded": len(turns),
        "turns_evicted_before_plan": ledger.evicted(conversation_id),
    }
    digest_input = {"conversation_id": conversation_id, "batches": batches,
                    "evicted": preview["turns_evicted_before_plan"], "max_claims": max_claims_per_call}
    plan_id = "cvp-" + hashlib.sha256(
        json.dumps(digest_input, ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest()[:32]
    return {"schema_version": PLAN_SCHEMA, "conversation_id": conversation_id, "plan_id": plan_id,
            "preview": preview, "batches": batches}


def _selection(value: Iterable[str] | None, error: str) -> set[str] | None:
    if value is None:
        return None
    if isinstance(value, (str, bytes)) or not isinstance(value, Iterable):
        raise ValueError(error)
    items = list(value)
    if not items or any(not isinstance(item, str) or not item.strip() for item in items):
        raise ValueError(error)
    return set(items)


def run_plan(plan: Mapping[str, Any], connection: SARAv3Connection) -> dict[str, Any]:
    """Send each planned batch to SARA v3 under per-run pseudonyms."""
    base = {
        "schema_version": RESULT_SCHEMA, "conversation_id": plan["conversation_id"], "plan_id": plan["plan_id"],
        "preview": plan["preview"], "verification_status": "UNVERIFIED",
        "truthfulness_status": "UNASSESSED", "is_evidence": False,
    }
    if not connection.connected:
        return {**base, "execution_status": "NOT_CONNECTED", "claim_results": [], "batches": [],
                "assessment_envelopes": [], "coverage": _coverage([]),
                "connection_error": connection.connection_error or "SARA_V3_UNAVAILABLE"}
    if not plan["batches"]:
        return {**base, "execution_status": "NOT_APPLICABLE", "claim_results": [], "batches": [],
                "assessment_envelopes": [], "coverage": _coverage([])}

    run_tag = secrets.token_hex(6)
    claim_results: list[dict[str, Any]] = []
    batch_reports: list[dict[str, Any]] = []
    envelopes_out: list[dict[str, Any]] = []
    sara_counter = 0
    for batch in plan["batches"]:
        id_map: dict[str, dict[str, str]] = {}
        candidates = []
        for claim in batch["claims"]:
            sara_counter += 1
            sara_id = f"K{sara_counter}"
            id_map[sara_id] = claim
            candidates.append({"id": sara_id, "text": claim["text"]})
        payload = {
            "request_id": f"cv-{run_tag}-b{batch['batch']}",
            "conversation_id": f"cv-{run_tag}",
            "turn_id": f"t{batch['turn_position']}-{batch['role'][0].lower()}",
            "content": batch["content"],
            "claim_candidates": candidates,
            "evidence": [],
            "provenance_ids": [f"co-thoughts:cv-{run_tag}:b{batch['batch']}"],
        }
        report = {
            "batch": batch["batch"], "turn_id": batch["turn_id"], "role": batch["role"],
            "sent_scope": {"sara_claim_ids": list(id_map), "content_chars": len(batch["content"]),
                           "context_forwarded": False, "identifiers": "PSEUDONYMIZED_PER_RUN"},
        }
        envelopes: list[dict[str, Any]] = []
        try:
            result = connection.process_turn(payload, connection.timeout_seconds)
            envelopes = _validated_v3_result(result, set(id_map))
            report["execution_status"] = "SUCCEEDED"
            report["sara_verification_status"] = result["verification_status"]
            reasons = _sara_reasons(result)
            if reasons:
                report["sara_reason_codes"] = reasons
        except Exception as exc:
            code = str(exc)
            report["execution_status"] = "FAILED"
            report["error_code"] = (code if isinstance(exc, (SARAv3Error, ValueError)) and _ERROR_CODE.fullmatch(code)
                                    else type(exc).__name__.upper())
        by_claim = {item["claim_id"]: item for item in envelopes}
        envelopes_out.extend(envelopes)
        for sara_id, claim in id_map.items():
            entry = {"claim_ref": claim["claim_ref"], "turn_id": batch["turn_id"], "role": batch["role"],
                     "claim_id": claim["id"], "text": claim["text"], "sara_claim_id": sara_id,
                     "batch": batch["batch"]}
            if sara_id in by_claim:
                entry.update(status="ASSESSED", sara_verification_status=by_claim[sara_id]["verification_status"])
            else:
                entry.update(status="NOT_ASSESSED",
                             reason_codes=([report["error_code"]] if "error_code" in report
                                           else report.get("sara_reason_codes") or ["SARA_RETURNED_NO_ENVELOPE"]))
            claim_results.append(entry)
        batch_reports.append(report)

    failed = sum(1 for item in batch_reports if item["execution_status"] != "SUCCEEDED")
    status = "SUCCEEDED" if not failed else ("FAILED" if failed == len(batch_reports) else "PARTIALLY_FAILED")
    return {**base, "execution_status": status, "coverage": _coverage(claim_results),
            "claim_results": claim_results, "batches": batch_reports, "assessment_envelopes": envelopes_out}


def _coverage(claim_results: list[Mapping[str, Any]]) -> dict[str, int]:
    assessed = sum(1 for item in claim_results if item["status"] == "ASSESSED")
    return {"claims_total": len(claim_results), "claims_assessed": assessed,
            "claims_not_assessed": len(claim_results) - assessed}


def _sara_reasons(result: Mapping[str, Any]) -> list[str]:
    """Surface SARA's own reason codes (never free text): routing reason, then provider error."""
    codes = []
    for path in (("activation_decision", "reason_code"), ("external_llm_response", "error_code")):
        value: Any = result
        for key in path:
            value = value.get(key) if isinstance(value, Mapping) else None
        if isinstance(value, str) and _ERROR_CODE.fullmatch(value):
            codes.append(value)
    return codes
