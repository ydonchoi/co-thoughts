# T38 — Document Type Standard Architecture Audit v0.1

Status: **PASS — ARCHITECTURE DEFINED / TEMPLATE STANDARDIZATION REQUIRED**

## 1. Purpose
T38 audits the existing Research Note Document Types v0.1 and defines the minimum architecture needed to turn existing D1–D9 proposed structures into an operational document-template system.

It does not replace the document-type taxonomy. It evaluates whether current D1–D9 structures can serve as the basis for standardized Research Note templates.

## 2. Current Baseline
Canonical source: `protocol/research_note_document_types_v0.1.md`  
Status: PROJECT PROPOSAL

Existing document types:
- D1 Exploratory
- D2 Descriptive / Current State
- D3 Concept Analysis
- D4 Relation / Impact Analysis
- D5 Mechanism / Process Analysis
- D6 Prediction
- D7 Evaluation
- D8 Literature / Evidence Synthesis
- D9 Integrated / Synthesis

The source defines different fixed structures, not one universal Research Note table of contents.

## 3. Findings

### F1. Document Type Differentiation — PASS
D1–D9 have materially different information-arrangement requirements. A universal fixed TOC should not replace existing type-specific structures.

### F2. Document Type / Research Purpose Separation — PASS
Document Type is an output/representation structure. Research Purpose is an independent classification axis.

For example, a D5 note may primarily serve R3.3 Mechanism Explanation, but Document Type must not be treated as Research Purpose itself.

### F3. Common Metadata Layer — PASS
Common Metadata provides a shared layer: Note ID, title, source conversation, related notes, document type, taxonomy code, purpose, operator, domain, design, method, evidence type, R&D orientation, knowledge product, Claim, Premise, Evidence, epistemic state, uncertainty, boundary, counter-evidence, verification state, and revision history.

Metadata are not equivalent to body sections.

### F4. Body-Template Layer — PASS
D1–D9 structures should be treated as document-body templates determining information arrangement, section order, and type-specific emphasis.

They must not redefine the underlying semantics of Claim, Evidence, Verification, Transformation Event, Relation, Revision, or D9.

### F5. Template Execution Specification — NOT YET DEFINED
The v0.1 document defines section sequences but does not yet specify:
- required / conditional / optional status for each section;
- section purpose;
- expected object types;
- Claim/Evidence/Transformation/Verification mapping;
- allowed omission conditions;
- prohibited inference;
- generation trigger;
- epistemic-state display rule.

Therefore v0.1 is a structural proposal, not yet an operational template specification.

### F6. Common Core + Type-Specific Modules — REQUIRED
The standard system should use:

Common Metadata + Document-Type Body Structure + Conditional Analytical Modules

It should not create nine entirely independent schemas.

### F7. D9 Special Handling — REQUIRED
D9 must preserve its distinct integration and promotion semantics. Its template may represent Relation → Higher-order Question → Novel Structure → Claim Decomposition → Evidence Mapping → Network-level SARA, but the template itself must not imply D9 PROMOTED or VERIFIED.

### F8. Missing-Information Safety — REQUIRED
A template must not force the engine to invent missing Claims, Evidence, Verification, Relations, mechanisms, predictions, or evaluation criteria.

When required analytical information is unsupported or unavailable, explicit states such as Not available, Not established, Not applicable, Requires verification, or Unresolved must be allowed. The exact epistemic state remains governed by the engine/data model.

## 4. Standard Template Architecture

~~~text
Research Note Template System
├── A. Common Metadata Layer
├── B. Document-Type Body Template
│   ├── D1
│   ├── D2
│   ├── D3
│   ├── D4
│   ├── D5
│   ├── D6
│   ├── D7
│   ├── D8
│   └── D9
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
~~~

This is an architecture proposal derived from project documents, not an established external academic standard.

## 5. Template Section Contract
Each standardized section should eventually define:
1. Section ID
2. Section title
3. Section status: REQUIRED / CONDITIONAL / OPTIONAL
4. Section purpose
5. Input Research Object(s)
6. Expected Claim(s)
7. Evidence relationship
8. Transformation relationship, when applicable
9. Verification display rule
10. Omission condition
11. Prohibited inference
12. Output format
13. Provenance requirement

This contract is the minimum needed to make a template executable through the one-stop Research Note pipeline.

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

The existing D1–D9 proposal is sufficient as the structural baseline for a standardized template system, but it is not yet operationally complete.

No new Document Type is required. No universal fixed TOC should be introduced. No separate database/schema is justified at this stage.

The next task is to define the Common Research Note Schema / Template Contract, followed by formal D1–D9 specifications.

## 8. Next Test
**T39 — Common Research Note Schema / Template Contract**

T39 should define the common metadata/body boundary and section-level contract without prematurely expanding the Notion database schema.

## 9. Evidence / Provenance
Primary evidence:
- `protocol/research_note_document_types_v0.1.md`
- `protocol/research_note_generation_engine_v0.4.md`
- `protocol/research_note_data_model_v0.4.md`
- `protocol/research_note_one_stop_pipeline_v0.1.md`

Human final epistemic agency remains unchanged.

---

[Korean source](t38_document_type_standard_architecture_audit_v0.1.md)
