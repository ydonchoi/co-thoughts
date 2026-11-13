# Whole-Conversation Independent Verification Contract v0.1

Status: Implemented (unit-tested against a fake SARA). The real provider round trip is confirmed only conditionally (§9)
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
| User-cited sources (added 2026-11-13) | Only the host's `user_claims[].source_urls` go as `evidence` in that utterance's SARA call. URLs a backend attaches are not sent |
| User-supplied full text (added 2026-11-13) | A source SARA can read only in part can be supplemented by a file the user obtained (`user_documents`). It goes only with that claim's calls, and its file name is not sent. SARA decides whether it is the cited work and how far to trust it (§10) |

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
  - An item in the request's `user_claims` may carry `source_urls`, the URLs the user cites. Up to five per claim, HTTPS on the default port only; one with credentials, a fragment or whitespace is rejected before the backend call with `USER_CLAIMS_INVALID`. Duplicate URLs are merged. When the same claim text arrives more than once, the first id is kept and the URLs of every copy are merged (five at most in total); the URLs of a dropped copy are validated all the same.
  - `source_urls` on the backend output's `claims` or `user_claims` are backend evidence and are not recorded.
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
| `source_urls_sent` | User-cited URLs that will be sent (summed over calls) |
| `user_documents` | Per document: `document` (`D<n>`), `file_name`, `media_type`, `pages`, `cites`, `claim_refs`, `sha256`, `chars`, `calls`. Never the text |
| `document_chars_to_sara`, `document_excerpt_chars_per_claim_max` | Document characters going to SARA (summed over calls), and the excerpt SARA sends to the external provider per claim at most (30,000) |
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
 "evidence": [{"id": "S<n>", "url": "<user-cited URL>", "snippet": "USER_SUPPLIED_SOURCE_URL"}],
 "provenance_ids": ["co-thoughts:cv-<run>:b<n>"]}
```

- Other turns' bodies, request `context`, backend evidence and backend-asserted statuses are not sent.
- `evidence` holds only the URLs the user cited for the claims in that call (at most 10 per call; more is refused at planning with `SOURCE_URLS_PER_CALL_EXCEEDED`). SARA applies a turn's evidence to every claim in it, so the other claims of the same call also see these URLs as candidates. A URL is an untrusted candidate: it becomes evidence only once SARA rereads the page through its own source adapters (SARA `SARA_OPEN_SOURCES_WEB_DOMAINS`).
- Each SARA call carries at most 8 claims (`SARAv3Connection.max_claims`). Beyond that, batches are split over the same body.
- A call with user documents adds `"user_documents": [{"id": "D<n>", "cites": "<cited URL>", "text": "<extracted text>", "sha256": "<SHA-256 of the text>"}]`, at most 5 per call (more is `USER_DOCUMENTS_PER_CALL_EXCEEDED`).

## 7. Result

- `execution_status`: `SUCCEEDED` / `PARTIALLY_FAILED` / `FAILED` / `NOT_APPLICABLE` (no claims to send) / `NOT_CONNECTED`
- `coverage`: `claims_total`, `claims_assessed`, `claims_not_required_by_sara`, `claims_not_assessed`
- `claim_results`: per claim, `claim_ref` (`<turn_id>:<USER|ASSISTANT>:<claim_id>`), `turn_id`, `role`, `claim_id`, `text`, `sara_claim_id`, `status` (`ASSESSED`/`NOT_REQUIRED_BY_SARA`/`NOT_ASSESSED`), and `sara_verification_status` or `reason_codes`
- `batches`: per batch, `sent_scope`, `execution_status`, `error_code`, `sara_reason_codes`
- A claim's `user_documents`: SARA's verdict on each document it saw for that claim. Each entry has `document`, `file_name`, `cites`, `identity` (`MATCHED`/`UNMATCHED`/`UNVERIFIED`), `reason_code`, `title_score` and `abstract_score`. A report whose digest differs from the document this plan sent is dropped.
- A claim's `full_text_requests`, and the top-level `full_text_requests`: sources SARA read only as an abstract or snippet and could not decide from. The top-level list is grouped by URL, with `claim_refs`. The host can use it to ask the user for the full text.
- `assessment_envelopes`: SARA's envelopes, unmodified, with pseudonymous claim ids `K<n>`. They can be carried into the next turn as `sara_assessment_envelopes`.
- `verification_status` is always `UNVERIFIED`, `is_evidence` is `false`, and `truthfulness_status` is `UNASSESSED`. SARA's verdicts live only in `claim_results`; Co-thoughts does not promote its own output.

**Preventing silent failure:**
- One failing batch does not stop the others.
- A claim for which SARA exited normally but returned no envelope is marked `NOT_ASSESSED`. SARA's own codes go into `reason_codes`, for example `JUDGMENT_UNAVAILABLE_OR_INVALID` and `LLM_PROVIDER_HTTP_ERROR_400`.
- Exception: when SARA itself **decides that no verification is needed**, the claim is counted separately as `NOT_REQUIRED_BY_SARA`. SARA starts verification only when its judgment finds an inference with HIGH confidence, so a plain factual claim is legitimately skipped. This applies only when SARA's `activation_decision` has `activation_action=NO_INFERENCE_TRIGGER` and `activation_triggered=false`. Anything else (a missing or inconsistent value, `SARA_PRECHECK_REVIEW`, and so on) stays `NOT_ASSESSED`. `NOT_REQUIRED_BY_SARA` does not mean verified.
- Free-text error messages are never surfaced.

## 8. Note on exposure

- Per call, exposure is minimal. But verifying the whole conversation eventually sends most claim-bearing utterances to the provider.
- Even with pseudonyms, the calls of one run share the same pseudonymous `conversation_id`, so the provider can group the calls within that run. What pseudonyms prevent is exposure of the real ids and linkage across separate runs.
- Claims that point at other turns ("that policy …") lack context and tend to end as `NOT_ASSESSED`. Claims are best extracted as self-contained sentences.
- User-cited URLs go to SARA, which fetches the page and has the provider LLM assess the relation, so the URL and the page content are exposed to the external provider too.
- Checked 2026-11-13: citing a 정책브리핑 policy-news article, SARA read its body as `ABSTRACT` and assessed the relation (Gemini: `SUPPORTS`). Page text read from HTML is `ABSTRACT`, so the claim stayed `UNVERIFIED` (`FULL_TEXT_NOT_ACCESSED`).

## 9. Verification status

| Item | Status |
|---|---|
| Recording, planning, confirmation, batching, pseudonyms, result mapping | Unit tests (fake SARA, `tests/unit/test_sara_v3_integration.py`) |
| SARA CLI process fail-closed | Run against a real SARA checkout (no provider settings) |
| User-supplied full text | Unit tests (`tests/unit/test_user_documents.py`: extraction, attachment, plan confirmation, result mapping). Live, 2026-11-13: an arXiv PDF (1706.03762, 15 pages, 39,521 characters) was extracted by co-thoughts and sent round trip through the SARA CLI and Gemini (`gemini-3.1-flash-lite`). Identity was `MATCHED` (title 1.0, abstract 0.942). With `SARA_TRUST_USER_DOCUMENTS=1` the claim became `VERIFIED`, on a `SUPPORTS` from the document excerpt. The same PDF offered as another paper's (BERT's) full text was `UNMATCHED` (abstract 0.019). The default (`0`) round trip could not be confirmed live: the judgment failed all 3 attempts (one 503, two invalid outputs). That case is covered by unit tests only (`PARTIALLY_VERIFIED`, `USER_DOCUMENT_TRUST_NOT_ENABLED`) |
| Real provider round trip | Conditionally confirmed (2026-11-12). With the Gemini API (`gemini-3.1-flash-lite`, free tier) the live test passed 3/3 (two inference claims, two envelopes, next turn `PRESERVED`). Conditions: (1) it ran against a **local copy** of SARA whose Gemini request uses `responseJsonSchema` instead of `responseSchema`; unmodified SARA always gets HTTP 400 from Gemini because of `additionalProperties`. (2) With no Brave search key, every envelope was `UNVERIFIED` (`BRAVE_SEARCH_API_KEY_REQUIRED`), so source-based verdicts were not tested. (3) In 1 of 3 separate attempts the judgment returned `INVALID_OUTPUT` and one claim was `NOT_ASSESSED`. The 2026-11-04 Anthropic attempt failed on a low credit balance (HTTP 400) |

## 10. User-supplied full text (`user_documents`)

SARA counts as full text (`FULL_TEXT`) only what it fetched itself. For a source SARA cannot read in full, such as a paywalled article or a site whose robots.txt refuses automated clients, the user can supply a file they obtained.

```python
docs = [{"path": "paper.pdf", "cites": "https://doi.org/10.1000/xyz", "claim_refs": ["T1:USER:U1"]}]
plan = runtime.plan_conversation_verification(cid, user_documents=docs)   # preview: no text
result = runtime.verify_conversation(cid, confirmation=plan["plan_id"], user_documents=docs)
```

- **Formats**
  - PDF, read with the optional `pypdf` package. Without it, loading fails with `PDF_SUPPORT_UNAVAILABLE`.
  - `.txt` and `.md`, read as UTF-8, falling back to CP949.
  - `.html`, using its text only, without scripts or styles.
  - Files must be at most 50 MB, with 500 to 2,000,000 characters of extracted text. One plan takes at most 20 documents and 10,000,000 characters of text in total (`USER_DOCUMENTS_TOO_MANY`, `USER_DOCUMENTS_TOO_LARGE`). The count is checked before any file is read, and PDF extraction stops at the page that crosses the bound. A file without a text layer, such as a scanned PDF, is refused with `USER_DOCUMENT_TEXT_TOO_SHORT`.
- **Attachment**
  - A document goes with the calls of the claims in its `claim_refs`, and with calls that cite its `cites` URL in `source_urls`.
  - A document attached to no call is refused with `USER_DOCUMENT_NOT_ATTACHED`, including one left out by a narrowed selection.
  - A reference to an unrecorded claim is refused with `USER_DOCUMENT_CLAIM_REF_NOT_RECORDED`.
- **Confirmation**
  - The plan id includes each document's digest and `cites`, so a file changed after the preview is `VERIFICATION_PLAN_NOT_CONFIRMED`.
  - The same file for the same source is sent once, with the `claim_refs` merged.
- **What SARA decides**
  - SARA fetches the cited source itself and checks that its title and abstract are in the document. Only a matching document is used as full text.
  - By default such a document cannot alone make a claim `VERIFIED` or `CONTRADICTED`. With `SARA_TRUST_USER_DOCUMENTS=1` set by the operator on SARA, it can, under the trusted-domain policy of the source it cites.
  - `USER_SUPPLIED_DOCUMENT_USED` is recorded whenever a document is used.
- **Exposure**
  - The whole document goes only as far as the SARA process, which runs locally. The external provider gets at most a 30,000-character excerpt per claim.
  - File names and `claim_refs` are not sent.
  - Whether a paywalled article may go to an external provider is for the user to judge, under that document's terms of use.

---

[Korean source](conversation_verification_contract_v0.1.md)
