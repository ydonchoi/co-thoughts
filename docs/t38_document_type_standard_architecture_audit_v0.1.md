# T38 — Document Type Standard Architecture Audit v0.1

Status: **PASS — ARCHITECTURE DEFINED / TEMPLATE STANDARDIZATION REQUIRED**

## 1. Purpose

T38 audits the existing Research Note Document Types v0.1 and defines the minimum architecture required to turn the existing D1–D9 proposal structures into an operational document-template system.

This test does not replace the existing document-type taxonomy. It evaluates whether the current D1–D9 structures can serve as the foundation for standardized research-note templates.

## 2. Current Baseline

Canonical source:

- `protocol/research_note_document_types_v0.1.md`
- Status: PROJECT PROPOSAL

Existing Document Types:

- D1 탐색
- D2 기술·현황
- D3 개념 분석
- D4 관계·영향 분석
- D5 메커니즘·과정 분석
- D6 예측
- D7 평가
- D8 문헌·근거 종합
- D9 통합·종합

The current document already defines distinct fixed structures rather than a single universal Research Note TOC.

## 3. Findings

### F1. Document Type differentiation — PASS

D1–D9 have materially different information-arrangement requirements.

Therefore a universal fixed TOC should not replace the existing type-specific structures.

### F2. Document Type / Research Purpose separation — PASS

Document Type is an output/representation structure.

Research Purpose remains an independent classification axis.

A D5 note, for example, may be primarily R3.3 메커니즘 설명, but Document Type must not be interpreted as the Research Purpose itself.

### F3. Common metadata layer — PASS

The existing Common Metadata provides a shared metadata layer:

Note ID, title, source conversation, related notes, document type, taxonomy code, purpose, operator, domain, design, method, evidence type, R&D orientation, knowledge product, claim, premise, evidence, epistemic state, uncertainty, boundary, counter-evidence, verification state, revision history.

These metadata are not equivalent to body sections.

### F4. Body-template layer — PASS

The D1–D9 structures are appropriately treated as document-body templates.

They should determine information arrangement, section ordering, and type-specific emphasis.

They must not redefine the underlying Claim, Evidence, Verification, Transformation Event, Relation, Revision, or D9 semantics.

### F5. Template execution specification — NOT YET DEFINED

The current v0.1 document defines section sequences but does not yet specify, for each section:

- required / conditional / optional status;
- section purpose;
- expected object types;
- Claim/Evidence/Transformation/Verification mapping;
- allowed omission conditions;
- prohibited inference;
- generation trigger;
- epistemic-state display rule.

Therefore v0.1 is a structural proposal, not yet an operational template specification.

### F6. Common core + type-specific modules — REQUIRED

The standard system should use:

Common Metadata
+
Document-Type Body Structure
+
Conditional Analytical Modules

It should not create nine completely independent schemas.

### F7. D9 special handling — REQUIRED

D9 must retain its distinct integration and promotion semantics.

Its template may represent:

Relation
→ Higher-order Question
→ Novel Structure
→ Claim Decomposition
→ Evidence Mapping
→ Network-level SARA

but the document template itself must not imply D9 PROMOTED or VERIFIED.

### F8. Missing-information safety — REQUIRED

A template must not force the engine to invent missing Claims, Evidence, Verification, Relations, mechanisms, predictions, or evaluation criteria.

If a required analytical component is unsupported or unavailable, the template must permit explicit states such as:

- Not available
- Not established
- Not applicable
- Requires verification
- Unresolved

The exact epistemic state remains governed by the engine/data model.

## 4. Standard Template Architecture

The proposed operational architecture is:

Research Note Template System
│
├── A. Common Metadata Layer
│
├── B. Document Type Body Template
│   ├── D1
│   ├── D2
│   ├── D3
│   ├── D4
│   ├── D5
│   ├── D6
│   ├── D7
│   ├── D8
│   └── D9
│
└── C. Conditional Analytical Modules
    ├── Evidence Mapping
    ├── Claim Decomposition
    ├── Counter-evidence
    ├── Competing Explanation
    ├── Comparison
    ├── Prediction Scenario
    ├── Evaluation Criteria
    ├── Literature Screening
    ├── SARA
    ├── Revision
    └── D9 Gate

This is an architecture proposal derived from the existing project documents; it is not an established external academic standard.

## 5. Template Section Contract

Each standardized section should eventually define:

1. Section ID
2. Section title
3. Section status: REQUIRED / CONDITIONAL / OPTIONAL
4. Section purpose
5. Input Research Object(s)
6. Expected Claim(s)
7. Evidence relationship
8. Transformation relationship when applicable
9. Verification display rule
10. Omission condition
11. Prohibited inference
12. Output format
13. Provenance requirement

This contract is the minimum needed to make a template executable by the one-stop Research Note pipeline.

## 6. Core Invariants

- Document Type ≠ Research Purpose
- Document Type ≠ Epistemic State
- Document Type ≠ Research Object
- Research Note ≠ Evidence
- Claim ≠ Evidence
- Evidence ≠ Verification
- Transformation Event ≠ Claim
- Transformation Event ≠ Evidence
- Transformation Event ≠ Verification
- Template ≠ Truth
- Missing section ≠ Missing evidence
- Persistence ≠ Verification
- D9 Promotion ≠ Claim Verification

## 7. Decision

**T38 = PASS**

The existing D1–D9 proposal is sufficient as the structural baseline for a standardized template system.

However, it is not yet operationally complete.

No new Document Type is required.

No universal fixed TOC should be introduced.

No separate database/schema is justified at this stage.

The next task is to define the **Common Research Note Schema / Template Contract**, followed by formal D1–D9 template specifications.

## 8. Next Test

**T39 — Common Research Note Schema / Template Contract**

T39 should define the common metadata/body boundary and the section-level contract without prematurely expanding the Notion database schema.

## 9. Evidence / Provenance

Primary evidence:

- `protocol/research_note_document_types_v0.1.md`
- `protocol/research_note_generation_engine_v0.4.md`
- `protocol/research_note_data_model_v0.4.md`
- `protocol/research_note_one_stop_pipeline_v0.1.md`

Human final epistemic agency remains unchanged.
