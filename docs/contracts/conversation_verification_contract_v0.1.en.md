# Whole-Conversation Independent Verification Contract v0.1

Status: Implemented (unit-tested against a fake SARA). The real provider round trip is not verified
Implementation: `src/co_thoughts/conversation_verification.py`, `src/co_thoughts/runtime.py`
Decision: 2026-11-04, project owner (ydonchoi)

## 1. Purpose and background

SARA v3 calls external LLM and search providers on every turn (judgment plus response generation, at least two calls). Running it on each turn makes cost and latency grow with the number of turns. It also needs API credit separate from the chat subscription. In the 2026-11-04 live attempt the provider failed (credit balance too low, HTTP 400). SARA absorbed that as `NOT_ASSESSED`, so the missing verification was not visible.

The SARA v3 call therefore moves from **automatic on every turn** to **once, over the whole conversation, when the user asks**.

## 2. Decisions

| Item | Decision |
|---|---|
| When | Only on user request. SARA is never called while conversation turns run |
| What | Claims in user utterances and in assistant responses |
| Send unit | One utterance body (user or assistant) of one turn ID and only the claims from that utterance. One per SARA call |
| Default range | The whole conversation. It can be narrowed with `turn_ids` or `claim_refs` |
| Confirmation | The plan preview is shown first; the run needs that plan's `plan_id` as confirmation |
| Identifiers | `conversation_id`, `request_id`, `turn_id`, claim ids and provenance ids sent to SARA are pseudonyms generated per run. The mapping to real ids stays local |

## 3. Flow

```text
Conversation turn (runtime.run)
  └─ Only when SARA v3 is configured, record the turn: user utterance + user_claims, assistant response + claims
     Output: conversation_verification = {status: NOT_REQUESTED, verification_status: UNVERIFIED, recorded_claim_refs}
     Nothing is sent

User asks for verification
  1. plan = runtime.plan_conversation_verification(conversation_id, turn_ids=?, claim_refs=?)
     → show plan["preview"] to the user. Nothing is sent
  2. User confirms
  3. result = runtime.verify_conversation(conversation_id, confirmation=plan["plan_id"], same selection)
     → per-utterance batches go to SARA v3; per-claim results come back
```

## 4. Turn recording

- **Assistant claims:** the backend output's `claims` (`id`, `text`)
- **User claims:**
  - The request's `user_claims` (set by the host) are used first. Without them, the backend output's `user_claims` (extracted by the backend) are used.
  - Co-thoughts does not extract claims from user text itself.
  - Claims without an id get `UC-n`.
  - Requests through `run_workflow` and `run_natural_language` carry `user_claims` through to the record as well (pinned by a regression test).
- **User utterance body:** the request's `task`
- **Assistant body:** the output's `response`. If it is empty, the claim texts are joined.
- **Malformed input:**
  - Malformed request `user_claims` are rejected before the backend call with `USER_CLAIMS_INVALID`.
  - Malformed backend `user_claims` do not fail the conversation turn. The user claims are left out of the record and reported as `warnings: ["BACKEND_USER_CLAIMS_INVALID"]`.
- **Recording units:**
  - Utterances without claims are not recorded and not sent.
  - Re-running the same `turn_id` replaces its earlier record.
  - Within one utterance, claims whose whitespace-normalized text is identical are sent once. The same sentence in another utterance is sent separately, since its body context differs.
- **Storage:**
  - Records live in process memory only (no persistence).
  - Up to 500 turns per conversation and 100 conversations are kept; beyond that the oldest are evicted.
  - The number of evicted turns appears in the plan preview as `turns_evicted_before_plan`.
- **When SARA v3 is not configured:** nothing is recorded.

## 5. Plan and confirmation

`plan["preview"]` contains the following.

| Field | Meaning |
|---|---|
| `provider_calls` | Number of SARA calls (per-utterance batches) |
| `turns_sent`, `turn_ids_sent` | Turns that will be sent |
| `claims_sent`, `claims_by_role` | Claims that will be sent (USER / ASSISTANT) |
| `content_chars_sent` | Total body characters sent |
| `send_unit` | `ONE_UTTERANCE_BODY_PER_CALL` |
| `context_forwarded` | Always `false` |
| `identifiers` | `PSEUDONYMIZED_PER_RUN` |
| `turns_recorded`, `turns_evicted_before_plan` | Recorded turns, and turns evicted by the storage limit |

- `plan_id` is a hash of the conversation id, the batch contents, the evicted-turn count and the batch limit.
- When a new turn is added or the selection changes, `plan_id` changes.
- So a range the user did not confirm cannot be sent. Using an earlier plan's id raises `VERIFICATION_PLAN_NOT_CONFIRMED`.

## 6. What is sent (one SARA call)

```json
{"request_id": "cv-<run>-b<n>", "conversation_id": "cv-<run>", "turn_id": "t<position>-u|a",
 "content": "<that utterance body>", "claim_candidates": [{"id": "K<n>", "text": "..."}],
 "evidence": [], "provenance_ids": ["co-thoughts:cv-<run>:b<n>"]}
```

- Other turns' bodies, request `context`, backend evidence and backend-asserted statuses are not sent.
- Each SARA call carries at most 8 claims (`SARAv3Connection.max_claims`). Beyond that, batches are split over the same body.

## 7. Result

- `execution_status`: `SUCCEEDED` / `PARTIALLY_FAILED` / `FAILED` / `NOT_APPLICABLE` (no claims to send) / `NOT_CONNECTED`
- `coverage`: `claims_total`, `claims_assessed`, `claims_not_assessed`
- `claim_results`: per claim, `claim_ref` (`<turn_id>:<USER|ASSISTANT>:<claim_id>`), `turn_id`, `role`, `claim_id`, `text`, `sara_claim_id`, `status` (`ASSESSED`/`NOT_ASSESSED`), and `sara_verification_status` or `reason_codes`
- `batches`: per batch, `sent_scope`, `execution_status`, `error_code`, `sara_reason_codes`
- `assessment_envelopes`: SARA's envelopes, unmodified, with pseudonymous claim ids `K<n>`. They can be carried into the next turn as `sara_assessment_envelopes`.
- `verification_status` is always `UNVERIFIED`, `is_evidence` is `false`, and `truthfulness_status` is `UNASSESSED`. SARA's verdicts live only in `claim_results`; Co-thoughts does not promote its own output.

**Preventing silent failure:**
- One failing batch does not stop the others.
- A claim for which SARA exited normally but returned no envelope is marked `NOT_ASSESSED`. SARA's own codes go into `reason_codes`, for example `JUDGMENT_UNAVAILABLE_OR_INVALID` and `LLM_PROVIDER_HTTP_ERROR_400`.
- Free-text error messages are never surfaced.

## 8. Note on exposure

- Per call, exposure is minimal. But verifying the whole conversation eventually sends most claim-bearing utterances to the provider.
- Even with pseudonyms, the calls of one run share the same pseudonymous `conversation_id`, so the provider can group the calls within that run. What pseudonyms prevent is exposure of the real ids and linkage across separate runs.
- Claims that point at other turns ("that policy …") lack context and tend to end as `NOT_ASSESSED`. Claims are best extracted as self-contained sentences.

## 9. Verification status

| Item | Status |
|---|---|
| Recording, planning, confirmation, batching, pseudonyms, result mapping | Unit tests (fake SARA, `tests/unit/test_sara_v3_integration.py`) |
| SARA CLI process fail-closed | Run against a real SARA checkout (no provider settings) |
| Real provider round trip | Not verified. In the 2026-11-04 attempt the provider failed with a low credit balance (HTTP 400). The new live test reported this exactly as `claims_not_assessed=2` and failed |

---

[Korean source](conversation_verification_contract_v0.1.md)
