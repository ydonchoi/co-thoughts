# T39 — Common Research Note Schema / Template Contract v0.1

Status: **PASS — COMMON CONTRACT DEFINED / D1–D9 MAPPING NEXT**

## 1. Purpose

T39 defines the common contract shared by all Research Note Document Types without replacing their type-specific body structures.

The contract establishes the boundary between:

- shared metadata;
- common document framing;
- Document Type-specific body sections;
- conditional analytical modules;
- epistemic/provenance controls.

It does not create a new Notion database schema and does not change the underlying Research Note Data Model v0.4.

## 2. Design Principle

The standard is:

**Common Metadata + Common Framing + Document-Type Body + Conditional Modules**

It is not:

**One Universal Body Template**

D1–D9 retain their distinct information-arrangement structures.

## 3. Common Metadata Layer

The logical Research Note metadata remains governed by Research Note Data Model v0.4.

Common metadata may include:

- Note ID
- Title
- Source Conversation
- Source Objects
- Related Notes
- Document Type
- Taxonomy / Classification
- Primary Research Purpose
- Secondary Research Purpose
- Question Operator
- Domain
- Research Design
- Method
- Review Type
- R&D Orientation
- Knowledge Product
- Epistemic State
- Evidence State
- SARA Status
- Uncertainty
- Boundary
- Counter-evidence
- Revision Version
- Previous Version
- Synthesis Status
- Provenance

These are metadata, not automatically body sections.

The persistence layer may collapse these fields according to the existing Notion representation; logical metadata semantics must remain intact.

## 4. Common Document Framing

Every Research Note should expose, at minimum, when applicable:

### F1. Research Object / Target

What is being investigated, described, evaluated, predicted, analyzed, or synthesized.

### F2. Primary Research Question

The normalized question governing the note.

### F3. Scope / Boundary

What is inside and outside the current inquiry.

### F4. Research Purpose

Primary purpose and, when relevant, secondary purpose.

### F5. Document Type

The selected D1–D9 representation type.

### F6. Epistemic / Verification Summary

A concise user-facing representation of the current epistemic state, verification status, uncertainty, and material limitations.

This framing does not override the underlying Claim-level epistemic states.

## 5. Section Contract

Every body section in a standardized template must be definable by the following contract:

| Field | Definition |
|---|---|
| Section ID | Stable identifier within the template |
| Section Title | User-facing heading |
| Status | REQUIRED / CONDITIONAL / OPTIONAL |
| Purpose | Why the section exists |
| Inputs | Research Objects / Claims / Evidence / Relations / prior notes |
| Outputs | Claims / Results / structured interpretation / questions |
| Evidence Role | SUPPORT / CONTRADICT / CONTEXT / ILLUSTRATE / BACKGROUND where applicable |
| Transformation | Transformation Event type when applicable |
| Verification Display | How relevant verification state is exposed |
| Omission Rule | When the section may be omitted |
| Missing-State Rule | What to display when required information is unavailable |
| Prohibited Inference | What the generator must not infer |
| Provenance | Required origin/lineage information |
| Rendering | Expected document representation |

## 6. Section Status Semantics

### REQUIRED

The section expresses a structural element essential to the selected Document Type.

If the underlying information is unavailable, the section remains structurally recognized but must explicitly report the missing/unresolved state rather than fabricate content.

### CONDITIONAL

The section is rendered only when its trigger condition is satisfied.

Examples:

- counter-evidence exists;
- competing explanations exist;
- a prediction scenario is justified;
- a revision occurred;
- a D9 integration relation exists.

### OPTIONAL

The section may be included when useful but does not define the minimum structural validity of the Document Type.

## 7. Missing-Information Contract

Templates must distinguish at least:

- NOT_AVAILABLE — information was not obtained;
- NOT_ESTABLISHED — information cannot currently be established;
- NOT_APPLICABLE — the section does not apply;
- REQUIRES_VERIFICATION — a relevant assertion exists but verification is pending;
- UNRESOLVED — competing or insufficient information prevents resolution.

These labels are presentation/operational states and must not be silently substituted for the canonical epistemic-state vocabulary.

No template may cause the generator to fabricate:

- Claims;
- Evidence;
- Verification;
- Relations;
- mechanisms;
- prediction variables;
- evaluation criteria;
- literature findings.

## 8. Claim / Evidence / Verification Rendering Rule

The document may present prose synthesis, tables, or structured sections, but underlying semantics remain separate.

Required conceptual separation:

**Claim**
→ proposition being asserted

**Evidence**
→ support/contradiction/context/illustration/background unit

**Verification**
→ explicit evaluation/revision/re-verification record

**Transformation Event**
→ operation linking inputs to outputs relevant to a Claim

A section titled “근거” does not itself become Evidence, and a section titled “검증” does not itself become Verification unless the underlying objects/records exist.

## 9. Transformation Rendering Rule

Transformation Events may be displayed when they materially explain how a result or Claim was produced.

Typical mappings include:

- ATTRIBUTE
- MEASURE
- ANALYZE
- SYNTHESIZE
- MODEL
- GENERALIZE
- INTERPRET
- RECLASSIFY

The template must not confuse an operation with its result.

## 10. SARA Rendering Rule

SARA may appear as:

- concise verification status in the common framing;
- detailed verification/revision section when material;
- audit detail on request.

SARA remains:

**Verification → Revision → Re-verification**

It is not a document approval mechanism and not equivalent to agreement.

## 11. D9 Rendering Rule

D9 may include:

- integrated relations;
- higher-order question;
- novel structure;
- claim decomposition;
- evidence mapping;
- network-level SARA;
- D9 Gate status.

The template must distinguish:

- D9 CANDIDATE;
- D9 PROMOTED;
- claim-level epistemic states.

D9 PROMOTED must never be rendered as equivalent to VERIFIED.

## 12. Generation Safety Rules

The template generator must:

1. preserve the selected Document Type unless evidence requires reclassification;
2. omit unsupported analytical content rather than invent it;
3. preserve Claim/Evidence/Verification distinctions;
4. preserve provenance;
5. preserve revision history;
6. expose material uncertainty;
7. permit non-monotonic epistemic states;
8. avoid converting persistence into verification;
9. preserve human final epistemic agency.

## 13. Common Rendering Order

Unless a Document Type explicitly changes the order, the preferred rendering order is:

1. Title / metadata
2. Research Object / target
3. Research Question
4. Purpose / Document Type
5. Scope / Boundary
6. Document-Type-specific body
7. Claim / Evidence / Verification summary where useful
8. Uncertainty / Limitations
9. Conclusion / Current State
10. Follow-up Questions
11. Provenance / Revision / SARA details when applicable

This is a default rendering convention, not a universal fixed TOC.

## 14. Relationship to D1–D9 Templates

D1–D9 templates inherit this contract.

Each D1–D9 specification must next define:

- section IDs;
- section status;
- section purpose;
- input/output object mapping;
- evidence mapping;
- transformation mapping;
- verification rendering;
- omission conditions;
- prohibited inference;
- provenance requirements.

## 15. Decision

**T39 = PASS**

The common Research Note Template Contract is sufficiently defined for formal D1–D9 template specification.

No new logical entity is introduced.

No Notion schema expansion is required.

No change is made to Research Note Engine v0.4 semantics.

## 16. Next Test

**T40 — D1–D9 Standard Template Specification v0.1**

T40 should translate the existing D1–D9 proposal structures into contract-compliant, executable template specifications.

## 17. Status Boundary

This document is a project-level architecture proposal for template execution. It is not an established external academic standard.

Human remains final epistemic decision authority.
