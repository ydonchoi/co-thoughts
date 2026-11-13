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

The user may also supply the full text of a source SARA can read only in part
(``user_documents``). A document goes with the calls whose claims it is for,
or that cite the same URL. SARA checks it against the source it cites and
reports, per claim, which sources it could not read in full
(``full_text_requests``), so the host can ask the user for those.
"""

from __future__ import annotations

from collections import OrderedDict
import hashlib
import json
import secrets
from typing import Any, Iterable, Mapping
from urllib.parse import urlparse

from sara_integration import SARAv3Connection, SARAv3Error, _ERROR_CODE, _validated_v3_result
from user_documents import document_summary

ROLES = ("USER", "ASSISTANT")
RESULT_SCHEMA = "co-thoughts.conversation-verification.v1"
PLAN_SCHEMA = "co-thoughts.conversation-verification-plan.v1"
MAX_SOURCE_URLS_PER_CLAIM = 5
MAX_SOURCE_URLS_PER_CALL = 10
# SARA's limits: documents per call, and how much of one it gives its relation assessor.
MAX_USER_DOCUMENTS_PER_CALL = 5
SARA_DOCUMENT_EXCERPT_CHARS = 30_000
USER_SOURCE_SNIPPET = "USER_SUPPLIED_SOURCE_URL"
SARA_NO_TRIGGER = "NO_INFERENCE_TRIGGER"


def _source_urls(value: Any, error: str) -> list[str]:
    """Validate the source URLs a user cites for a claim (HTTPS, no credentials or fragment)."""
    if not isinstance(value, (list, tuple)) or len(value) > MAX_SOURCE_URLS_PER_CLAIM:
        raise ValueError(error)
    urls: list[str] = []
    for item in value:
        if not isinstance(item, str) or not item or len(item) > 2048 or any(c.isspace() for c in item):
            raise ValueError(error)
        try:
            parsed = urlparse(item)
            port = parsed.port
        except ValueError:
            raise ValueError(error) from None
        if (parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password
                or parsed.fragment or port not in (None, 443)):
            raise ValueError(error)
        if item not in urls:
            urls.append(item)
    return urls


def normalize_claims(value: Any, *, prefix: str, error: str, allow_sources: bool = False) -> list[dict[str, Any]]:
    """Return [{id, text[, source_urls]}] from a claim list; ids default to ``prefix-N``.

    Identical texts within one utterance are kept once. ``source_urls`` are kept
    only when ``allow_sources`` (claims the host supplies for the user); a
    backend's URLs are backend evidence, which is never forwarded, so they are dropped.
    """
    if value is None:
        return []
    if not isinstance(value, (list, tuple)):
        raise ValueError(error)
    claims: list[dict[str, Any]] = []
    by_text: dict[str, dict[str, Any]] = {}
    for index, item in enumerate(value):
        if not isinstance(item, Mapping):
            raise ValueError(error)
        text = item.get("text")
        if not isinstance(text, str) or not text.strip():
            raise ValueError(error)
        text = " ".join(text.split())
        # Validate every item's sources, including a duplicate's, before deduplicating.
        urls = (_source_urls(item["source_urls"], error)
                if allow_sources and item.get("source_urls") is not None else [])
        if text in by_text:
            # A repeated claim keeps its first id; the citations of every copy are merged.
            kept = by_text[text]
            merged = list(dict.fromkeys([*kept.get("source_urls", []), *urls]))
            if len(merged) > MAX_SOURCE_URLS_PER_CLAIM:
                raise ValueError(error)
            if merged:
                kept["source_urls"] = merged
            continue
        claim_id = item.get("id")
        claim_id = str(claim_id).strip() if claim_id is not None and str(claim_id).strip() else f"{prefix}-{index + 1}"
        claim: dict[str, Any] = {"id": claim_id, "text": text}
        if urls:
            claim["source_urls"] = urls
        by_text[text] = claim
        claims.append(claim)
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
    documents: list[Mapping[str, Any]] | None = None,
) -> dict[str, Any]:
    """Describe exactly what a verification run would send, without sending it.

    ``documents`` are loaded user documents (see ``user_documents``). The plan
    refers to them by position and digest; their text is not part of the plan.
    """
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
                chunk = claims[start:start + max_claims_per_call]
                # SARA applies a turn's evidence to every claim in it, so the call carries
                # the URLs cited for any claim of this chunk, and only those.
                urls = list(dict.fromkeys(u for claim in chunk for u in claim.get("source_urls", [])))
                if len(urls) > MAX_SOURCE_URLS_PER_CALL:
                    raise ValueError("SOURCE_URLS_PER_CALL_EXCEEDED")
                batches.append({
                    "batch": len(batches) + 1, "turn_id": turn["turn_id"], "turn_position": position,
                    "role": role, "content": utterance["content"],
                    "claims": chunk, "source_urls": urls,
                })
    if wanted_refs is not None and not wanted_refs <= matched_refs:
        raise ValueError("CLAIM_REF_NOT_RECORDED")

    documents = list(documents or [])
    # Turn and claim ids may contain colons, so one reference string can name two claims.
    # A document goes only where the user meant it, so such a reference is refused.
    ref_counts: dict[str, int] = {}
    for t in turns:
        for role in ROLES:
            for c in (t["utterances"].get(role) or {}).get("claims", []):
                ref = claim_ref(t["turn_id"], role, c["id"])
                ref_counts[ref] = ref_counts.get(ref, 0) + 1
    attached = [0] * len(documents)
    for index, doc in enumerate(documents):
        if not set(doc["claim_refs"]) <= set(ref_counts):
            raise ValueError("USER_DOCUMENT_CLAIM_REF_NOT_RECORDED")
        if any(ref_counts[ref] > 1 for ref in doc["claim_refs"]):
            raise ValueError("USER_DOCUMENT_CLAIM_REF_AMBIGUOUS")
    for batch in batches:
        refs = {claim["claim_ref"] for claim in batch["claims"]}
        # A document goes with a call when it is for one of the call's claims, or when the
        # call already cites the source it is the full text of.
        batch["documents"] = [index for index, doc in enumerate(documents)
                              if refs & set(doc["claim_refs"]) or doc["cites"] in batch["source_urls"]]
        if len(batch["documents"]) > MAX_USER_DOCUMENTS_PER_CALL:
            raise ValueError("USER_DOCUMENTS_PER_CALL_EXCEEDED")
        for index in batch["documents"]:
            attached[index] += 1
    if any(count == 0 for count in attached):
        # A document for no call in this selection would be silently unused.
        raise ValueError("USER_DOCUMENT_NOT_ATTACHED")

    sent_turns = sorted({item["turn_id"] for item in batches}, key=[t["turn_id"] for t in turns].index)
    preview = {
        "destination": "SARA_V3_EXTERNAL_PROVIDERS",
        "provider_calls": len(batches),
        "turns_sent": len(sent_turns),
        "turn_ids_sent": sent_turns,
        "claims_sent": sum(len(item["claims"]) for item in batches),
        "claims_by_role": {role: sum(len(b["claims"]) for b in batches if b["role"] == role) for role in ROLES},
        "content_chars_sent": sum(len(item["content"]) for item in batches),
        "source_urls_sent": sum(len(item["source_urls"]) for item in batches),
        # The full text goes to SARA, which runs locally; its relation assessor sends at most
        # an excerpt of each document, per claim, to the external provider.
        "user_documents": [{**document_summary(doc), "document": f"D{index + 1}",
                            "calls": attached[index]} for index, doc in enumerate(documents)],
        "document_chars_to_sara": sum(documents[i]["chars"] for b in batches for i in b["documents"]),
        "document_excerpt_chars_per_claim_max": SARA_DOCUMENT_EXCERPT_CHARS if documents else 0,
        "send_unit": "ONE_UTTERANCE_BODY_PER_CALL",
        "context_forwarded": False,
        "identifiers": "PSEUDONYMIZED_PER_RUN",
        "turns_recorded": len(turns),
        "turns_evicted_before_plan": ledger.evicted(conversation_id),
    }
    digest_input = {"conversation_id": conversation_id, "batches": batches,
                    "evicted": preview["turns_evicted_before_plan"], "max_claims": max_claims_per_call,
                    # A changed file, or a document for another source, is a different plan.
                    "documents": [{"sha256": d["sha256"], "cites": d["cites"]} for d in documents]}
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


def run_plan(plan: Mapping[str, Any], connection: SARAv3Connection,
             documents: list[Mapping[str, Any]] | None = None) -> dict[str, Any]:
    """Send each planned batch to SARA v3 under per-run pseudonyms.

    ``documents`` must be the documents the plan was built with, in order.
    """
    documents = list(documents or [])
    if [{"sha256": d["sha256"], "cites": d["cites"]} for d in documents] != [
            {"sha256": d["sha256"], "cites": d["cites"]} for d in plan["preview"].get("user_documents", [])]:
        raise ValueError("USER_DOCUMENTS_DO_NOT_MATCH_PLAN")
    base = {
        "schema_version": RESULT_SCHEMA, "conversation_id": plan["conversation_id"], "plan_id": plan["plan_id"],
        "preview": plan["preview"], "verification_status": "UNVERIFIED",
        "truthfulness_status": "UNASSESSED", "is_evidence": False, "full_text_requests": [],
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
            # User-cited URLs only; SARA treats them as untrusted candidates and reads
            # them through its own source adapters before any relation is assessed.
            "evidence": [{"id": f"S{n}", "url": url, "snippet": USER_SOURCE_SNIPPET}
                         for n, url in enumerate(batch.get("source_urls", []), start=1)],
            "provenance_ids": [f"co-thoughts:cv-{run_tag}:b{batch['batch']}"],
        }
        if batch.get("documents"):
            # File names and claim links stay local; SARA gets a per-plan id, the cited URL,
            # the text and its digest.
            payload["user_documents"] = [{"id": f"D{i + 1}", "cites": documents[i]["cites"],
                                          "text": documents[i]["text"], "sha256": documents[i]["sha256"]}
                                         for i in batch["documents"]]
        report = {
            "batch": batch["batch"], "turn_id": batch["turn_id"], "role": batch["role"],
            "sent_scope": {"sara_claim_ids": list(id_map), "content_chars": len(batch["content"]),
                           "source_urls": len(batch.get("source_urls", [])),
                           "user_documents": [f"D{i + 1}" for i in batch.get("documents", [])],
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
            action = _sara_activation(result)
            if action:
                report["sara_activation_action"] = action
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
                found = by_claim[sara_id]
                entry.update(status="ASSESSED", sara_verification_status=found["verification_status"])
                reports = _document_reports(found, plan["preview"].get("user_documents", []))
                if reports:
                    entry["user_documents"] = reports
                requests = _full_text_requests(found)
                if requests:
                    entry["full_text_requests"] = requests
            elif report.get("sara_activation_action") == SARA_NO_TRIGGER:
                # SARA itself judged, with high confidence, that this utterance needs no
                # verification. That is SARA's decision, not a failure to assess.
                entry.update(status="NOT_REQUIRED_BY_SARA", reason_codes=report.get("sara_reason_codes", []))
            else:
                entry.update(status="NOT_ASSESSED",
                             reason_codes=([report["error_code"]] if "error_code" in report
                                           else report.get("sara_reason_codes") or ["SARA_RETURNED_NO_ENVELOPE"]))
            claim_results.append(entry)
        batch_reports.append(report)

    failed = sum(1 for item in batch_reports if item["execution_status"] != "SUCCEEDED")
    status = "SUCCEEDED" if not failed else ("FAILED" if failed == len(batch_reports) else "PARTIALLY_FAILED")
    return {**base, "execution_status": status, "coverage": _coverage(claim_results),
            "claim_results": claim_results, "batches": batch_reports, "assessment_envelopes": envelopes_out,
            "full_text_requests": _collect_requests(claim_results)}


def _document_reports(envelope: Mapping[str, Any], summaries: list[Mapping[str, Any]]) -> list[dict[str, Any]]:
    """SARA's verdict on each supplied document, mapped back to the user's file."""
    by_id = {item["document"]: item for item in summaries}
    out = []
    reports = envelope.get("user_documents")
    for report in reports if isinstance(reports, list) else []:
        # SARA's extension fields are optional and unvalidated upstream: check each type
        # before using it, and drop what is malformed rather than fail the batch.
        if not isinstance(report, Mapping) or not isinstance(report.get("id"), str) or report["id"] not in by_id:
            continue
        local = by_id[report["id"]]
        identity = report.get("identity") if isinstance(report.get("identity"), str) else None
        # A report must carry the digest of the document this plan sent. The one exception is
        # SARA's report for a document it refused at validation: no digest, and only UNVERIFIED.
        refused = report.get("sha256") is None and identity == "UNVERIFIED"
        if report.get("sha256") != local["sha256"] and not refused:
            continue  # not the document this plan sent
        reason = report.get("reason_code")
        out.append({"document": report["id"], "file_name": local["file_name"], "cites": local["cites"],
                    "identity": identity if identity in {"MATCHED", "UNMATCHED", "UNVERIFIED"} else "UNVERIFIED",
                    **({"reason_code": reason} if isinstance(reason, str) and _ERROR_CODE.fullmatch(reason) else {}),
                    **{key: report[key] for key in ("title_score", "abstract_score")
                       if isinstance(report.get(key), (int, float)) and not isinstance(report.get(key), bool)}})
    return out


def _full_text_requests(envelope: Mapping[str, Any]) -> list[dict[str, Any]]:
    out = []
    requests = envelope.get("full_text_requests")
    for item in requests if isinstance(requests, list) else []:
        if not isinstance(item, Mapping):
            continue
        url, title = item.get("url"), item.get("title")
        try:
            ok = isinstance(url, str) and urlparse(url).scheme == "https"
        except ValueError:
            ok = False
        if ok:
            level = item.get("access_level")
            out.append({"url": url, "title": title if isinstance(title, str) else url,
                        "access_level": level if isinstance(level, str) and level in {
                            "ABSTRACT", "SEARCH_SNIPPET", "METADATA"} else "UNKNOWN"})
    return out


def _collect_requests(claim_results: list[Mapping[str, Any]]) -> list[dict[str, Any]]:
    """One entry per source the user could supply, with the claims it would help settle."""
    by_url: dict[str, dict[str, Any]] = {}
    for entry in claim_results:
        for item in entry.get("full_text_requests", []):
            found = by_url.setdefault(item["url"], {**item, "claim_refs": []})
            found["claim_refs"].append(entry["claim_ref"])
    return list(by_url.values())


def _coverage(claim_results: list[Mapping[str, Any]]) -> dict[str, int]:
    counts = {status: sum(1 for item in claim_results if item["status"] == status)
              for status in ("ASSESSED", "NOT_REQUIRED_BY_SARA", "NOT_ASSESSED")}
    return {"claims_total": len(claim_results), "claims_assessed": counts["ASSESSED"],
            "claims_not_required_by_sara": counts["NOT_REQUIRED_BY_SARA"],
            "claims_not_assessed": counts["NOT_ASSESSED"]}


def _sara_activation(result: Mapping[str, Any]) -> str | None:
    """SARA's routing action; NO_INFERENCE_TRIGGER only counts when SARA also says it did not trigger."""
    decision = result.get("activation_decision")
    if not isinstance(decision, Mapping):
        return None
    action = decision.get("activation_action")
    if not isinstance(action, str) or not _ERROR_CODE.fullmatch(action):
        return None
    if action == SARA_NO_TRIGGER and decision.get("activation_triggered") is not False:
        return None
    return action


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
