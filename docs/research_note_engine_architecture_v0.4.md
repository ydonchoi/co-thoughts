# Research Note Engine v0.4 Architecture (가칭)

Status: **BASELINE CANDIDATE**

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

## Human Final Agency

The architecture supports human judgment; it does not delegate final epistemic authority to the model.

## Scope Note

This architecture is a project-level proposal. New concepts marked (가칭) are not claimed to be established academic terminology.
