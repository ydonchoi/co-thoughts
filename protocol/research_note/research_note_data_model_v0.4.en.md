# Research Note Data Model v0.4 (provisional project model)

Status: **BASELINE CANDIDATE**

## Logical Entities

1. Conversation Session
2. Research Object
3. Research Note
4. Claim
5. Evidence
6. Verification
7. Transformation Event
8. Relation
9. Taxonomy
10. Version / Revision Event
11. Branch
12. Provenance
13. D9 Gate

## Core Semantics

### Conversation Session
The origin of provenance. It is not itself a knowledge object.

### Research Object
An item identified for investigation or knowledge processing.

Fields:
RO ID, Original Expression, Normalized Question, Object Type, Source Session, Source Segment, Parent Object, Primary Purpose, Secondary Purpose, Question Operator, Domain, Candidate Document Type, Final Document Type, Epistemic Status, Evidence Status, SARA Status, Object Decision, Research Note, Taxonomy Provenance, Generation Provenance, Revision History.

### Research Note
The document-representation layer.

Fields:
Note ID, Title, Document Type, Research Purpose, Primary Question, Secondary Questions, Source Session, Source Objects, Related Notes, Domain, Design, Method, Review Type, R&D Orientation, Knowledge Product, Epistemic State, Evidence State, Verification Date, SARA Status, Uncertainty, Boundary, Counter-evidence, Revision Version, Previous Version, Synthesis Status.

The page body contains the table of contents specific to the document type; database properties are metadata.

### Claim
A proposition that can be evaluated for truth.

Fields:
Claim ID, Claim Text, Note, Object, Claim Type, Epistemic State, Evidence, Counter-evidence, Verification, Confidence, Boundary, Attribution/Interpretation provenance, Revision History.

A note may be supported overall while individual Claims remain hypotheses.

### Evidence
A unit of support, contradiction, context, illustration, or background.

Fields:
Evidence ID, Source, Source Type, Source Date, Evidence Text, Supports, Contradicts, Contextualizes, Illustrates, Evidence Strength, Directness, Verification Status, Provenance.

Source ≠ Evidence. Evidence ≠ Verification.

### Verification
A verification record containing:
Verification ID, Target, Verification Type, Initial State, Evidence, Finding, Revision Required, Revision, Re-verification, Final State, Date.

SARA:
Claim → Verification → Revision → Re-verification → Final Epistemic State.

### Transformation Event
A traceability operation.

Fields:
Transformation ID, Input Reference(s), Transformation Type, Output Reference(s), Target Claim(s), Evidence Role, Validation State, Provenance, Revision Reference, and optional uncertainty/boundary/conditions/agent/method/timestamp/version.

### Relation
Fields:
Relation ID, Source, Relation Type, Target, Basis, Evidence, Qualification, Confidence, Verification State, Description.

Core relation types:
DERIVED_FROM, SUPPORTS, CHALLENGES, EXTENDS, REFINES, CONTRADICTS, SYNTHESIZES, CONTEXTUALIZES, EVIDENCES.

Prefer qualification metadata over proliferating relation types.

### Version / Revision Event
A non-destructive lifecycle record.

Fields:
Version ID, Parent Version, Revision Type, Reason, Affected Objects, Evidence Changes, Transformation Changes, Relation Changes, Verification Changes, Created At, Author/Agent, Status.

### Branch
A parallel revision state.

Fields:
Branch ID, Parent Version, Derived Revision, Evidence Set, Transformation Set, Claim Version, Epistemic State, Scope, Conditions, Revision Reason.

A Branch is not a truth judgment.

### Provenance
Tracks origin and transformation lineage.

## D9 Gate

G1 Relation, G2 Higher-order Question, G3 Novel Structure, G4 Claim Decomposition, G5 Evidence Mapping, G6 Network-level SARA.

Promotion requires all gates to PASS. Promotion is independent of claim truth.

## Operational Persistence Representation

The one-stop adapter may map logical entities into a collapsed Notion representation. The current project target is `👨‍💻 research_assisstant_prototype_-ing- 공식 문서`. The adapter must fetch the current target schema before page mutation and distinguish NEW, REVISION, EXTENSION, NO_CHANGE, and BLOCKED outcomes.

Persistence metadata must preserve provenance and must not be interpreted as verification. A post-write fetch is the preferred persistence-verification step.

## Minimum Implementation Principle

The number of logical entities does not dictate the number of Notion databases. Tables may be collapsed if semantics remain explicit and provenance is not lost.

## AI Disclosure / Generation Provenance Representation

AI authorship disclosure is represented as cross-cutting provenance metadata rather than as a logical knowledge entity.

Required artifact-level disclosure for generated/structured Research Notes:

**AI-generated / AI-structured Research Note**

Recommended structured representation using the existing `confession_report` field:

- ai_participation = YES
- generation_system = Research Note Engine
- artifact_attribution = AI_GENERATED / AI_STRUCTURED
- human_review = PENDING / IN_PROGRESS / COMPLETED
- human_editing = NONE / MATERIAL / UNKNOWN
- source_derived_content = YES / NO / UNKNOWN
- provenance_reference = [reference]
- disclosure_version = v0.1

Optional local attribution labels:
A1 AI-generated; A2 AI-structured; A3 Human-authored; A4 Human-edited; A5 Source-derived.

These are provenance labels, not epistemic states. No new Research Object, Claim, Evidence, Verification, or database is required.

## Validation Closure Extension

T51–T56 establish, for the tested scope, that AI disclosure is compatible with D1–D9, lifecycle decisions, human post-editing, D9 integration, BLOCKED persistence, and full-pipeline output semantics.

Live durable persistence and broad empirical generation validation remain open and capability-bound.

---

[Korean source](research_note_data_model_v0.4.md)
