# Research Note One-Stop Pipeline v0.1 (가칭)

Status: **PROJECT INTEGRATION / OPERATIONAL PROTOCOL CANDIDATE**
Scope: research-note invocation, generation, consistency decision, Notion persistence, and post-write verification.

## 1. Purpose

This protocol connects the Research Note Generation Engine v0.4 to the conversational entrypoint so that a user can request research-note conversion in natural language and, when the persistence capability is available, complete generation and Notion DB storage in one continuous workflow.

It is an adapter/orchestration layer. It does not replace the Research Note Engine, Data Model, SARA, D9 Gate, or Notion schema.

## 2. Invocation

### Explicit triggers

- `/연구노트`
- `/변환`

### Natural-language equivalents

Examples include:

- "이걸 연구노트로 만들어줘."
- "이 대화를 연구노트로 변환해줘."
- "연구노트로 정리해줘."
- "연구노트 생성해줘."
- "연구노트로 변환해서 노션에 저장해줘."
- "이 내용 연구노트로 남겨줘."

Natural language is accepted when the intended operation is unambiguous from the current conversation.

If `/변환` is ambiguous and the target representation is not inferable, ask for clarification rather than silently choosing Research Note.

## 3. One-Stop Execution Contract

Trigger
→ Existing-state/context check
→ Research Object Detection
→ Boundary / Decomposition
→ Question Normalization
→ Provisional Classification
→ Candidate Document Type
→ Evidence Mapping
→ Claim Decomposition
→ Transformation Trace
→ SARA
→ Final Reclassification
→ Research Note Generation
→ Existing-note Consistency Decision
→ Relation / Revision Mapping
→ D9 Gate when applicable
→ Notion Property Mapping
→ Notion Page Create / Update
→ Post-write Verification
→ Result Report

The engine may branch or stop early when the current Research Object does not justify a research note.

## 4. Existing-Note Consistency First

Before creating a new durable note, search the target Notion research-note collection and relevant project context.

Decision:

- **NO_CHANGE** — same substantive issue, evidence, conclusion, and no meaningful extension. Do not duplicate.
- **REVISION** — existing judgment/state is changed by new evidence or analysis. Preserve the previous state and create an explicit Revision Event; never silently overwrite history.
- **EXTENSION** — the current session materially extends an existing note with a distinct question, evidence structure, conclusion, or lifecycle. Create a new Research Note linked to the prior note.
- **NEW** — no sufficiently related existing note exists. Create a new Research Note.
- **BLOCKED** — persistence target is inaccessible, locked, or write capability is unavailable. Complete generation when possible, but do not claim persistence.

Agreement, Checkpoint, or conversation state is never sufficient by itself to create Evidence or justify a Revision.

## 5. Research Note Generation Rules

The generation engine remains authoritative for:

- Research Object identification
- Primary/Secondary Research Purpose
- Document Type D1–D9
- Claim decomposition
- Evidence roles
- Transformation Events
- SARA
- Revision / Branch / Merge
- D9 promotion

The following distinctions are mandatory:

Source ≠ Evidence
Claim ≠ Evidence
Evidence ≠ Verification
Research Note ≠ Evidence
Transformation Event ≠ Claim
Transformation Event ≠ Evidence
Transformation Event ≠ Verification
Revision ≠ Replacement
Merge ≠ Agreement
D9 Promotion ≠ Verification

No missing Evidence, Claim, Transformation, or Verification object may be fabricated merely to complete a template.

## 6. Notion Persistence Contract

Current project target:

- Data source: `👨‍💻 research_assisstant_prototype_-ing- 공식 문서`
- Data source identifier: `collection://ae3996b1-f4b1-442f-872d-db499f283f66`

Current mapped properties:

- `연구노트` — title
- `주제` — topic
- `제작 단계 목표` — production-stage goal
- `github_저장소` — repository provenance
- `핵심 키워드` — keywords
- `confession_report` — epistemic/provenance disclosure field
- system-managed: `생성 일시`, `최종 편집 일시`, `최종 편집자`

The richer Research Note metadata defined by v0.4 may remain in page content or mapped properties as the target schema permits. Logical entity count does not require one-to-one Notion databases.

## 7. Write Safety

The one-stop command is not permission to bypass Notion access controls.

Before mutation:

1. resolve the target data source;
2. fetch the current schema/state;
3. determine whether the target is writable;
4. preserve the fresh before-state;
5. choose NEW / REVISION / EXTENSION / NO_CHANGE;
6. perform the minimum necessary mutation;
7. fetch the resulting page;
8. verify title, key metadata, provenance, and content presence.

If any write prerequisite fails, stop the mutation path and report the exact persistence state.

Never:

- claim a page was saved when creation/update failed;
- bypass a locked database;
- overwrite revision history;
- convert a generated claim into VERIFIED merely because the page was saved;
- treat successful persistence as epistemic verification.

## 8. Output Contract

After execution, report at minimum:

- operation: Research Note generation
- decision: NEW / REVISION / EXTENSION / NO_CHANGE / BLOCKED
- Research Object / Note identifier when available
- Document Type
- primary Research Purpose
- note-level epistemic state
- key Claim states when material
- SARA state
- D9 state when applicable
- Notion persistence: SAVED / UPDATED / NOT_CHANGED / BLOCKED
- Notion URL when available
- unresolved uncertainty or required human decision

Do not expose hidden chain-of-thought. Provide an auditable Claim / Evidence / Verification / Revision / Provenance summary instead.

## 9. Human Final Agency

The one-stop pipeline automates routing, decomposition, drafting, metadata mapping, persistence, and post-write checking. It does not delegate final epistemic authority to the model.

In particular:

- PROMOTED is not equivalent to VERIFIED;
- CANDIDATE is not equivalent to PROMOTED;
- successful Notion storage is not verification;
- model agreement is not evidence;
- absence of contradiction is not proof.

## 10. Failure / Degradation Modes

### Generation available, Notion write unavailable

Generate the Research Note and return a persistence status of BLOCKED. Do not imply that the note exists in the Notion DB.

### Notion search unavailable

Do not perform a blind NEW creation if duplication risk is material. Either request clarification or produce a non-persisted candidate.

### Target locked

Do not bypass the lock. Return the generated candidate and BLOCKED persistence status.

### Post-write verification unavailable

Do not report persistence as fully verified. Report SAVED/UPDATED only if the write tool itself succeeded, with post-write verification marked pending.

## 11. Relationship to Existing Protocols

This protocol depends on, and does not supersede:

- `protocol/research_note_generation_engine_v0.4.md`
- `protocol/research_note_data_model_v0.4.md`
- `protocol/research_note_taxonomy_v0.3.md`
- `protocol/research_note_document_types_v0.1.md`
- `protocol/d9_promotion_gate_v0.2.md`
- `protocol/claim_transformation_traceability_v0.1.md`

It is the conversational **adapter/orchestration layer** between those semantics and the durable Notion representation.

## 12. Status

This document specifies the intended one-stop operational contract. It does not by itself prove that every Notion query/write path is currently operational.

Current known condition at integration drafting:

- semantic Research Note generation: READY
- invocation routing: READY
- Notion schema mapping: IDENTIFIED
- live Notion write: capability/state dependent
- post-write verification: REQUIRED
- full operational closure: PENDING

Human remains final epistemic decision authority.


## 13. AI Authorship / Provenance Disclosure

Every Research Note generated or structured through this adapter must include the artifact-level disclosure:

**AI 작성·구조화 연구노트**

The disclosure is a cross-cutting presentation/provenance requirement. It does not create a new Research Object, Claim, Evidence, Verification, Document Type, or Notion database.

Minimum rendered disclosure:
- generation/structuring system: Research Note Engine
- AI participation: YES
- human review: independently reported
- generation provenance: Conversation → Research Object → Claim/Evidence → Transformation → SARA → Research Note
- persistence state: independently reported

Use the existing `confession_report` field for structured disclosure/provenance where available.

Local attribution may distinguish A1 AI-generated, A2 AI-structured, A3 Human-authored, A4 Human-edited, and A5 Source-derived only when provenance supports the distinction. If local attribution is uncertain, preserve artifact-level AI disclosure without inventing precision.

The following are explicitly distinct:

AI authorship ≠ Evidence  
AI generation ≠ Verification  
AI synthesis ≠ Consensus  
Persistence ≠ Verification  
D9 Promotion ≠ Verification

The disclosure must remain present for NEW, REVISION, EXTENSION, NO_CHANGE, and BLOCKED outcomes. Human editing may add human-edit provenance but must not erase the fact of AI generation/structuring.

## 14. Validation / Closure State

T51–T56 validate the AI disclosure contract, cross-document consistency, actual output rendering requirements, and full-pipeline semantic integration for the tested scope.

Current closure:
- AI disclosure semantic architecture: CLOSED FOR TESTED SCOPE
- Cross-document consistency: CLOSED FOR TESTED SCOPE
- Full-pipeline semantic integration: CLOSED FOR TESTED SCOPE
- Live writable Notion persistence: OPEN / CAPABILITY-BOUND
- Post-write verification: OPEN / CAPABILITY-BOUND
- Empirical repeated/large-scale generation validation: OPEN

Do not restart architecture design solely because live persistence or empirical generation validation remains open. Re-enter through capability check and controlled implementation validation.
