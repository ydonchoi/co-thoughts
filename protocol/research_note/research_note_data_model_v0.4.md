# Research Note Data Model v0.4 (가칭)

Status: **BASELINE CANDIDATE**

Logical entities:

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
Provenance origin. Not a knowledge object.

### Research Object
What has been identified for investigation or knowledge processing.

Fields:
RO ID, Original Expression, Normalized Question, Object Type, Source Session, Source Segment, Parent Object, Primary Purpose, Secondary Purpose, Question Operator, Domain, Candidate Document Type, Final Document Type, Epistemic Status, Evidence Status, SARA Status, Object Decision, Research Note, Taxonomy Provenance, Generation Provenance, Revision History.

### Research Note
Document representation layer.

Fields:
Note ID, Title, Document Type, Research Purpose, Primary Question, Secondary Questions, Source Session, Source Objects, Related Notes, Domain, Design, Method, Review Type, R&D Orientation, Knowledge Product, Epistemic State, Evidence State, Verification Date, SARA Status, Uncertainty, Boundary, Counter-evidence, Revision Version, Previous Version, Synthesis Status.

Page body contains the document-type-specific TOC; database properties are metadata.

### Claim
Truth-evaluable proposition.

Fields:
Claim ID, Claim Text, Note, Object, Claim Type, Epistemic State, Evidence, Counter-evidence, Verification, Confidence, Boundary, Attribution/Interpretation provenance, Revision History.

A note can be overall supported while individual claims remain hypotheses.

### Evidence
A support/contradiction/context/illustration/background unit.

Fields:
Evidence ID, Source, Source Type, Source Date, Evidence Text, Supports, Contradicts, Contextualizes, Illustrates, Evidence Strength, Directness, Verification Status, Provenance.

Source ≠ Evidence. Evidence ≠ Verification.

### Verification
Verification record:
Verification ID, Target, Verification Type, Initial State, Evidence, Finding, Revision Required, Revision, Re-verification, Final State, Date.

SARA:
Claim → Verification → Revision → Re-verification → Final Epistemic State.

### Transformation Event
Traceability operation.

Fields:
Transformation ID, Input Reference(s), Transformation Type, Output Reference(s), Target Claim(s), Evidence Role, Validation State, Provenance, Revision Reference, optional uncertainty/boundary/conditions/agent/method/timestamp/version.

### Relation
Fields:
Relation ID, Source, Relation Type, Target, Basis, Evidence, Qualification, Confidence, Verification State, Description.

Core relation types:
DERIVED_FROM, SUPPORTS, CHALLENGES, EXTENDS, REFINES, CONTRADICTS, SYNTHESIZES, CONTEXTUALIZES, EVIDENCES.

Prefer qualification metadata over proliferating relation types.

### Version / Revision Event
Non-destructive lifecycle record.

Fields:
Version ID, Parent Version, Revision Type, Reason, Affected Objects, Evidence Changes, Transformation Changes, Relation Changes, Verification Changes, Created At, Author/Agent, Status.

### Branch
Parallel revision state.

Fields:
Branch ID, Parent Version, Derived Revision, Evidence Set, Transformation Set, Claim Version, Epistemic State, Scope, Conditions, Revision Reason.

Branch is not a truth judgment.

### Provenance
Tracks origin and transformation lineage.

## D9 Gate
G1 Relation, G2 Higher-order Question, G3 Novel Structure, G4 Claim Decomposition, G5 Evidence Mapping, G6 Network-level SARA.

Promotion requires all PASS. Promotion is independent from claim truth.

## Operational Persistence Representation

The one-stop adapter may map the logical entities into a collapsed Notion representation. The current project target is `👨‍💻 research_assisstant_prototype_-ing- 공식 문서`. The adapter must fetch the current target schema before page mutation and must distinguish NEW, REVISION, EXTENSION, NO_CHANGE, and BLOCKED outcomes.

Persistence metadata must preserve provenance and must not be interpreted as verification. Post-write fetch is the preferred persistence verification step.

## Minimum Implementation Principle

Logical entity count does not dictate Notion DB count. Tables may be collapsed when semantics remain explicit and provenance is not lost.


## AI Disclosure / Generation Provenance Representation

AI authorship disclosure is represented as cross-cutting provenance metadata rather than as a logical knowledge entity.

Required artifact-level disclosure for generated/structured Research Notes:

**AI 작성·구조화 연구노트**

Recommended structured representation through existing `confession_report`:
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

Live durable persistence and broad empirical generation validation remain open/capability-bound.
