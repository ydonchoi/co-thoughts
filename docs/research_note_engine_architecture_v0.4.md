# Research Note Engine v0.4 Architecture (가칭)

Status: **BASELINE CANDIDATE**

## Operational Entry / Adapter

`/연구노트`, `/변환`, or unambiguous natural-language equivalents route to the one-stop Research Note adapter. The adapter invokes the engine and, when permitted, performs existing-note consistency checking → Notion mapping → create/update → post-write verification.

Canonical adapter protocol: `protocol/research_note_one_stop_pipeline_v0.1.md`.

## Architecture

Conversation
↓
Research Object
↓
Claim ↔ Evidence
↕
Transformation Event
↕
Verification
↕
Relation
↓
Research Note / D9

Cross-cutting:
Version / Revision / Branch / Provenance

Classification:
Taxonomy / Document Type

Promotion:
D9 Gate

## Design Principle

Read less. Reuse valid state. Reference only what is relevant. Preserve provenance. Do not invent project rules.

## Layer Separation

| Layer | Responsibility |
|---|---|
| Conversation | provenance origin |
| Research Object | identified unit of inquiry |
| Claim | truth-evaluable proposition |
| Evidence | support/contradiction/context unit |
| Transformation Event | input→output/claim trace |
| Verification | SARA lifecycle |
| Relation | knowledge relation |
| Version/Revision | non-destructive state history |
| Branch | parallel revision |
| Provenance | origin and lineage |
| Research Note | document representation |
| Taxonomy | classification |
| Document Type | structured output |
| D9 Gate | promotion decision |

## Architecture Invariants

- Research Purpose ≠ Method
- Research Purpose ≠ Document Type
- Claim ≠ Evidence
- Evidence ≠ Verification
- Research Note ≠ Evidence
- Transformation Event ≠ Claim
- Transformation Event ≠ Evidence
- Transformation Event ≠ Verification
- Revision ≠ Replacement
- Branch ≠ Truth
- Merge ≠ Agreement
- Conflict ≠ Error
- D9 Promotion ≠ Verification

## Implementation Constraint

Logical entities do not require one-to-one Notion databases. Database normalization must not destroy semantic distinctions or provenance.

## Persistence Boundary

Notion persistence is an operational side effect, not an epistemic state transition. A saved page does not become VERIFIED, and a failed write does not invalidate the generated Research Note.

## Human Final Agency

The architecture supports human judgment; it does not delegate final epistemic authority to the model.

## Scope Note

This architecture is a project-level proposal. New concepts marked (가칭) are not claimed to be established academic terminology.


## AI Disclosure / Provenance Cross-Cutting Layer

The architecture includes a cross-cutting AI authorship/provenance presentation layer:

**Visible Marker + Provenance Block + `confession_report` + Human Review Status**

Canonical marker:

**AI 작성·구조화 연구노트**

This layer does not add a logical epistemic entity. It remains independent from Claim, Evidence, Verification, D9 Gate, and persistence state.

Local attribution, when reliable, may distinguish A1 AI-generated, A2 AI-structured, A3 Human-authored, A4 Human-edited, and A5 Source-derived. Uncertain local attribution remains unresolved.

## Validation State

T51–T56: AI disclosure and full-pipeline semantic integration **CLOSED FOR TESTED SCOPE**.

Live persistence verification and large-scale empirical generation remain open/capability-bound. No architecture expansion is justified by the current evidence.
