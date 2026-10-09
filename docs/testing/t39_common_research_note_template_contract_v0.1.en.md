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

It does not create a new Notion database schema or change the Research Note Data Model v0.4.

## 2. Design Principle
The standard is:

**Common Metadata + Common Framing + Document-Type Body + Conditional Modules**

It is not a universal body template. D1–D9 retain their distinct information-arrangement structures.

## 3. Common Metadata Layer
Research Note metadata remain governed by Research Note Data Model v0.4.

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

These are metadata, not automatically body sections. The persistence layer may collapse fields according to the existing Notion representation, but logical metadata semantics must remain intact.

## 4. Common Document Framing
Every Research Note should expose the following, when applicable:

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
A concise user-facing representation of epistemic state, verification status, uncertainty, and material limitations.

This framing does not override underlying Claim-level epistemic states.

## 5. Section Contract
Every body section in a standardized template must be definable by this contract:

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
The section expresses a structural element essential to the selected Document Type. If the underlying information is unavailable, the section remains structurally recognized but must explicitly report the missing/unresolved state rather than fabricate content.

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

These are presentation/operational states and must not silently replace the canonical epistemic-state vocabulary.

No template may cause the generator to fabricate Claims, Evidence, Verification, Relations, mechanisms, prediction variables, evaluation criteria, or literature findings.

## 8. Claim / Evidence / Verification Rendering Rule
The document may present prose synthesis, tables, or structured sections, but the underlying semantics remain separate.

- **Claim** → proposition being asserted
- **Evidence** → unit of support/contradiction/context/illustration/background
- **Verification** → explicit evaluation/revision/re-verification record
- **Transformation Event** → operation linking inputs to outputs relevant to a Claim

A section titled “Evidence” does not itself become Evidence, and a section titled “Verification” does not itself become Verification unless the underlying objects/records exist.

## 9. Transformation Rendering Rule
Transformation Events may be displayed when they materially explain how a result or Claim was produced.

Typical mappings: ATTRIBUTE, MEASURE, ANALYZE, SYNTHESIZE, MODEL, GENERALIZE, INTERPRET, RECLASSIFY.

The template must not confuse an operation with its result.

## 10. SARA Rendering Rule
SARA may appear as:
- concise verification status in common framing;
- detailed verification/revision section when material;
- audit detail on request.

SARA remains **Verification → Revision → Re-verification**. It is not a document-approval mechanism and is not equivalent to agreement.

## 11. D9 Rendering Rule
D9 may include integrated relations, a higher-order question, novel structure, claim decomposition, evidence mapping, network-level SARA, and D9 Gate status.

The template must distinguish:
- D9 CANDIDATE;
- D9 PROMOTED;
- Claim-level epistemic states.

D9 PROMOTED must never be rendered as equivalent to VERIFIED.

## 12. Generation Safety Rules
The template generator must:
1. preserve the selected Document Type unless Evidence requires reclassification;
2. omit unsupported analytical content rather than invent it;
3. preserve Claim/Evidence/Verification distinctions;
4. preserve provenance;
5. preserve revision history;
6. expose material uncertainty;
7. permit non-monotonic epistemic states;
8. avoid converting persistence into verification;
9. preserve human final epistemic agency.

## 13. Common Rendering Order
Unless a Document Type explicitly changes the order, the preferred order is:
1. Title / metadata
2. Research Object / target
3. Research Question
4. Purpose / Document Type
5. Scope / Boundary
6. Document-Type-specific body
7. Claim / Evidence / Verification summary when useful
8. Uncertainty / Limitations
9. Conclusion / Current State
10. Follow-up Questions
11. Provenance / Revision / SARA details when applicable

This is a default rendering convention, not a universal fixed TOC.

## 14. Relationship to D1–D9 Templates
D1–D9 templates inherit this contract. Each specification must define section IDs, status, purpose, input/output mapping, evidence mapping, transformation mapping, verification rendering, omission conditions, prohibited inference, and provenance requirements.

## 15. Decision
**T39 = PASS**

The common Research Note Template Contract is sufficiently defined for formal D1–D9 template specification.

No new logical entity is introduced. No Notion schema expansion is required. Research Note Engine v0.4 semantics remain unchanged.

## 16. Next Test
**T40 — D1–D9 Standard Template Specification v0.1**

T40 should translate the existing D1–D9 proposal structures into contract-compliant, executable template specifications.

## 17. Status Boundary
This document is a project-level architecture proposal for template execution. It is not an established external academic standard. The human remains the final epistemic decision authority.

## AI Disclosure Rendering Contract
AI disclosure is a common cross-document layer and must not depend on any D1–D9 body section.

Required artifact marker: **AI-generated / AI-structured Research Note**

The common rendering contract should expose the generation/structuring system, AI participation, human-review status, generation provenance, and persistence state when applicable.

AI disclosure is presentation/provenance metadata, not a Claim, Evidence, Verification, or epistemic state.

Human/source attribution must remain distinct from AI generation when provenance supports that distinction.

---

[Korean source](t39_common_research_note_template_contract_v0.1.md)
