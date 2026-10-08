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

## Minimum Implementation Principle

Logical entity count does not dictate Notion DB count. Tables may be collapsed when semantics remain explicit and provenance is not lost.
