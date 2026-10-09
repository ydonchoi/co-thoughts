# Research Note One-Stop Pipeline v0.1 (provisional project protocol)

Status: **PROJECT INTEGRATION / OPERATIONAL PROTOCOL CANDIDATE**  
Scope: Research Note invocation, generation, consistency decisions, Notion persistence, and post-write verification.

## 1. Purpose

This protocol connects Research Note Generation Engine v0.4 to a conversational entry point. A user can request conversion into a Research Note in natural language and, when persistence is available, complete generation and Notion database storage in one continuous workflow.

This is an adapter/orchestration layer. It does not replace the Research Note Engine, Data Model, SARA, D9 Gate, or Notion schema.

## 2. Invocation

### Explicit triggers
- `/연구노트`
- `/변환`

### Natural-language equivalents

Examples:
- “Turn this into a Research Note.”
- “Convert this conversation into a Research Note.”
- “Organize this as a Research Note.”
- “Generate a Research Note.”
- “Convert this into a Research Note and save it to Notion.”
- “Keep this content as a Research Note.”

Natural language is accepted when the intended operation is unambiguous from the current conversation.

If `/변환` is ambiguous and the target representation cannot be inferred, ask for clarification rather than silently selecting Research Note.

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

The engine may branch or stop early when the current Research Object does not justify a Research Note.

## 4. Existing-Note Consistency First

Before creating a durable note, search the target Notion Research Note collection and relevant project context.

Decision:
- **NO_CHANGE** — the substantive issue, evidence, and conclusion are the same and there is no meaningful extension. Do not duplicate.
- **REVISION** — new evidence or analysis changes an existing judgment/state. Preserve the prior state and create an explicit Revision Event; never silently overwrite history.
- **EXTENSION** — the session materially extends an existing note with a distinct question, evidence structure, conclusion, or lifecycle. Create a new Research Note linked to the prior note.
- **NEW** — no sufficiently related existing note exists. Create a new Research Note.
- **BLOCKED** — the persistence target is inaccessible or locked, or write capability is unavailable. Complete generation when possible, but do not claim persistence.

Agreement, Checkpoint, or conversation state alone is never enough to create Evidence or justify a Revision.

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

Mandatory distinctions:

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

Do not fabricate missing Evidence, Claims, Transformations, or Verification objects merely to complete a template.

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

Richer Research Note metadata may remain in page content or mapped properties as the target schema permits. Logical entity count does not require one-to-one Notion databases.

## 7. Write Safety

The one-stop command does not authorize bypassing Notion access controls.

Before mutation:
1. resolve the target data source;
2. fetch the current schema/state;
3. determine whether the target is writable;
4. preserve the fresh before-state;
5. choose NEW / REVISION / EXTENSION / NO_CHANGE;
6. perform the minimum necessary mutation;
7. fetch the resulting page;
8. verify title, key metadata, provenance, and content presence.

If any prerequisite fails, stop mutation and report the exact persistence state.

Never:
- claim a page was saved when creation/update failed;
- bypass a locked database;
- overwrite revision history;
- mark a generated Claim VERIFIED merely because the page was saved;
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

Do not expose hidden chain-of-thought. Provide an auditable Claim / Evidence / Verification / Revision / Provenance summary.

## 9. Human Final Agency

The pipeline automates routing, decomposition, drafting, metadata mapping, persistence, and post-write checking. It does not delegate final epistemic authority to the model.

In particular:
- PROMOTED ≠ VERIFIED;
- CANDIDATE ≠ PROMOTED;
- successful Notion storage ≠ verification;
- model agreement ≠ evidence;
- absence of contradiction ≠ proof.

## 10. Failure / Degradation Modes

### Generation available, Notion write unavailable
Generate the Research Note and return BLOCKED persistence status. Do not imply the note exists in Notion.

### Notion search unavailable
Do not blindly create a NEW record if duplication risk is material. Ask for clarification or produce a non-persisted candidate.

### Target locked
Do not bypass the lock. Return the generated candidate with BLOCKED persistence status.

### Post-write verification unavailable
Do not report persistence as fully verified. Report SAVED/UPDATED only if the write tool itself succeeded, and mark post-write verification as pending.

## 11. Relationship to Existing Protocols

This protocol depends on, and does not supersede:
- [Research Note Generation Engine v0.4](research_note_generation_engine_v0.4.md)
- [Research Note Data Model v0.4](research_note_data_model_v0.4.md)
- [Research Note Taxonomy v0.3](research_note_taxonomy_v0.3.md)
- [Research Note Document Types v0.1](research_note_document_types_v0.1.md)
- [D9 Promotion Gate v0.2](../lifecycle/d9_promotion_gate_v0.2.md)
- [Claim Transformation Traceability v0.1](../core/claim_transformation_traceability_v0.1.md)

It is the conversational adapter/orchestration layer between those semantics and durable Notion representation.

## 12. Status

This document specifies the intended one-stop operational contract. It does not prove that every Notion query/write path is currently operational.

Known condition at integration drafting:
- semantic Research Note generation: READY
- invocation routing: READY
- Notion schema mapping: IDENTIFIED
- live Notion write: capability/state dependent
- post-write verification: REQUIRED
- full operational closure: PENDING

The human remains the final epistemic decision authority.

## 13. AI Authorship / Provenance Disclosure

Every Research Note generated or structured through this adapter must include artifact-level disclosure:

**AI-generated / AI-structured Research Note**

This is a cross-cutting presentation/provenance requirement. It does not create a new Research Object, Claim, Evidence, Verification, Document Type, or Notion database.

Minimum rendered disclosure:
- generation/structuring system: Research Note Engine
- AI participation: YES
- human review: reported independently
- generation provenance: Conversation → Research Object → Claim/Evidence → Transformation → SARA → Research Note
- persistence state: reported independently

Use the existing `confession_report` field for structured disclosure/provenance where available.

Local attribution may distinguish A1 AI-generated, A2 AI-structured, A3 Human-authored, A4 Human-edited, and A5 Source-derived only when provenance supports the distinction. If attribution is uncertain, preserve artifact-level AI disclosure without inventing precision.

These are separate:
- AI authorship ≠ Evidence
- AI generation ≠ Verification
- AI synthesis ≠ Consensus
- Persistence ≠ Verification
- D9 Promotion ≠ Verification

The disclosure must remain present for NEW, REVISION, EXTENSION, NO_CHANGE, and BLOCKED outcomes. Human editing may add human-edit provenance but must not erase AI-generation/structuring provenance.

## 14. Validation / Closure State

T51–T56 validate the AI-disclosure contract, cross-document consistency, actual-output rendering requirements, and full-pipeline semantic integration for the tested scope.

Current closure:
- AI disclosure semantic architecture: CLOSED FOR TESTED SCOPE
- cross-document consistency: CLOSED FOR TESTED SCOPE
- full-pipeline semantic integration: CLOSED FOR TESTED SCOPE
- live writable Notion persistence: OPEN / CAPABILITY-BOUND
- post-write verification: OPEN / CAPABILITY-BOUND
- empirical repeated/large-scale generation validation: OPEN

Do not restart architecture design solely because live persistence or empirical generation validation remains open. Re-enter through capability checks and controlled implementation validation.

---

[Korean source](research_note_one_stop_pipeline_v0.1.md)
