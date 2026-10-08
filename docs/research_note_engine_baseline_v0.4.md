# Research Note Engine v0.4 — Baseline Consolidation

Status: **BASELINE v0.4 — CONSOLIDATED**

## 1. Baseline Scope

This document consolidates T2–T13 and the current Notion/GitHub implementation state. It is the semantic baseline for the project. Historical versions remain in history/ and do not override this baseline.

## 2. Canonical Layer Model

### Core knowledge objects
1. Research Object
2. Claim
3. Evidence
4. Transformation Event
5. Verification
6. Relation

Conversation is the provenance origin.

### Representation
- Research Note

### Classification
- Research Purpose
- Question Operator
- Research Design
- Method
- Evidence/Source
- Knowledge Domain
- R&D Orientation
- Knowledge Product
- Document Type
- Review Type
- Synthesis Operation

### Lifecycle / provenance
- Version
- Revision Event
- Branch
- Provenance

### Promotion
- D9 Gate

## 3. Canonical Semantics

Research Object = independently identifiable unit of inquiry/knowledge processing.

Claim = truth-evaluable proposition.

Evidence = source-derived or generated support/contradiction/context unit mapped to claims/relations.

Transformation Event = operation that maps input object(s) to output object(s) relevant to a claim.

Verification = explicit evaluation/revision/re-verification record.

Relation = typed relation between knowledge objects.

Research Note = document representation, not an independent claim-level epistemic object.

Note-level epistemic state is a document-level assessment of the note's principal proposition set. Claim-level epistemic state belongs to each truth-evaluable Claim. A note-level state must not be interpreted as uniform verification of all claims; heterogeneous claim states require an explicit basis for any aggregate note-level assessment.

Taxonomy = classification metadata, not evidence or truth.

Document Type = output structure, not research purpose and not epistemic state.

D9 Gate = promotion mechanism, not verification.

## 4. Canonical Classification Rules

Primary Research Purpose: maximum 1.

Secondary Research Purpose: zero or more.

If a secondary purpose has an independent question, evidence structure, conclusion, or lifecycle, create a separate Research Object.

Document Type is selected provisionally and can be reclassified after evidence/SARA.

Legacy '문서 형식' is retained for backward compatibility. '표준 문서 유형' is the canonical D1–D9 field.

## 5. Canonical Evidence / Epistemic Rules

Evidence roles:
- SUPPORT
- CONTRADICT
- CONTEXT
- ILLUSTRATE
- BACKGROUND

Epistemic states:
- VERIFIED
- SUPPORTED
- PARTIALLY_SUPPORTED
- UNCERTAIN
- HYPOTHESIS
- INTERPRETATION
- UNVERIFIED
- CONTRADICTED

Evidence does not automatically determine epistemic state.

Agreement is not verification.

D9 promotion does not imply that every component claim is verified.

D9 applicability is distinct from promotion state: NOT_APPLICABLE ≠ CANDIDATE-not-promoted. HOLD is an operational review label, not a canonical promotion state unless explicitly defined.

## 6. SARA

SARA = Verification → Revision → Re-verification.

State changes are non-destructive and require explicit revision/verification records.

Historical states remain queryable.

## 7. Transformation Trace

Canonical graph:

Input → Transformation Event → Output → Evidence Role → Claim → Verification → Epistemic State

Transformation Type is not a research-purpose taxonomy.

Current candidate operation types:
ATTRIBUTE, MEASURE, ANALYZE, SYNTHESIZE, MODEL, GENERALIZE, INTERPRET, RECLASSIFY.

These remain project-level terminology marked (가칭).

## 8. Revision / Branch / Merge

Revision is non-destructive.

Conflict ≠ Error.

Branch ≠ Truth.

Merge ≠ Agreement.

Merge creates a new reconciliation/synthesis event and receives its own verification.

Failed merge preserves parallel branches.

## 9. D9

G1 Relation
G2 Higher-order Question
G3 Novel Structure
G4 Claim Decomposition
G5 Evidence Mapping
G6 Network-level SARA

Promotion requires all six gates PASS.

G6 partial pass triggers revision and promotion re-entry.

## 10. Notion Implementation Mapping

Existing core metadata is preserved.

| Existing property | Baseline role |
|---|---|
| 연구 목적 | Primary Research Purpose |
| 보조 연구 목적 | Secondary Research Purpose |
| 표준 문서 유형 | Canonical Document Type D1–D9 |
| 문서 형식 | Legacy / auxiliary representation label |
| 분류 코드 | Taxonomy code |
| 분류 근거 | Classification provenance/rationale |
| 인식론적 상태 | Note-level epistemic state; Claim-level state is stored at Claim layer |
| 근거 상태 | Evidence mapping state |
| SARA 상태 | Verification/revision lifecycle |
| 연구 설계 | Research Design |
| 연구 방법 | Method |
| R&D 방향 | R&D Orientation |
| 버전 | Version |
| 이전 연구노트 | Revision lineage |
| 적용 범위·경계 | Boundary |
| 반대 근거 | Counter-evidence |
| 관련 연구노트 / 연구노트 관계 | Relations |
| Research Object ID | Object lineage |
| Claim ID | Claim lineage |
| Evidence Mapping | Claim/evidence trace |
| Transformation Trace | Transformation provenance |
| Revision Type | Revision event |
| Branch ID | Parallel revision |
| D9 상태 | D9 applicability / promotion state; canonical states: NOT_APPLICABLE, CANDIDATE, PROMOTED |

## 11. Metadata vs Page Body

Metadata stores classification, lifecycle, provenance, and state.

Page body stores the document-type-specific research narrative and fixed TOC.

Do not encode an entire claim/evidence graph only in prose.

Do not force every logical entity into a separate Notion database. Separate databases are justified only when they improve queryability, lifecycle management, or provenance without increasing semantic ambiguity.

## 12. Canonical Invariants

- Research Purpose ≠ Method
- Research Purpose ≠ Document Type
- Claim ≠ Evidence
- Evidence ≠ Verification
- Verification ≠ Agreement
- Research Note ≠ Evidence
- Transformation Event ≠ Claim
- Transformation Event ≠ Evidence
- Transformation Event ≠ Verification
- Operation ≠ Result
- Result ≠ Claim
- Revision ≠ Replacement
- Branch ≠ Truth
- Merge ≠ Agreement
- Conflict ≠ Error
- D9 Promotion ≠ Verification

## 13. Version Authority

Current:
- protocol/research_note_generation_engine_v0.4.md
- protocol/research_note_data_model_v0.4.md
- protocol/research_note_taxonomy_v0.3.md
- protocol/research_note_document_types_v0.1.md
- protocol/d9_promotion_gate_v0.2.md
- protocol/claim_transformation_traceability_v0.1.md
- this baseline document

Historical:
- history/research_note_engine/*

Current baseline overrides historical rules where they differ.

## 14. Baseline Constraints

This baseline does not claim external academic validation of the entire architecture.

Academic taxonomy provenance and project architecture are separate evidence tracks.

New project-level terms remain (가칭) until independently established or explicitly adopted.

Human remains final epistemic decision authority.

## 15. Baseline Decision

**BASELINE v0.4 — CONSOLIDATED**

T2–T13: PASS / CONDITIONAL PASS as recorded.

No additional core object is introduced by this consolidation.

Next implementation phase:
- metadata population audit
- sample-note migration test
- schema/query usability test
- reproducibility test against the consolidated baseline
