# Research Note Engine v0.4 Architecture (provisional project model)

Status: **BASELINE CANDIDATE**

## Operational Entry / Adapter

`/연구노트`, `/변환`, or unambiguous natural-language equivalents route to the one-stop Research Note adapter. The adapter invokes the engine and, when permitted, performs existing-note consistency checking → Notion mapping → create/update → post-write verification.

Canonical adapter protocol: [One-Stop Pipeline v0.1](../../protocol/research_note/research_note_one_stop_pipeline_v0.1.md).

## Architecture

Conversation  
↓  
Research Object  
↓  
Claim ↔ Evidence  
↕ Transformation Event  
↕ Verification  
↕ Relation  
↓  
Research Note / D9

Cross-cutting: Version / Revision / Branch / Provenance  
Classification: Taxonomy / Document Type  
Promotion: D9 Gate

## Design Principle

Read less. Reuse valid state. Reference only what is relevant. Do not invent rules.

## Boundaries

- A conversation is a provenance origin, not itself a knowledge object.
- A Research Note is a representation/output artifact, not Evidence.
- Successful persistence is not epistemic verification.
- D9 promotion is not equivalent to verifying every integrated Claim.
- The human retains final epistemic authority.

---

[Korean source](research_note_engine_architecture_v0.4.md)
