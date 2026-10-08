# Research Note Generation Engine v0.4 (가칭)

Status: **BASELINE CANDIDATE**  
Scope: research-note decomposition, classification, verification, traceability, revision, branch/merge, D9 synthesis promotion, and conversational one-stop execution through the Research Note adapter.

## 1. Purpose

This engine converts a conversation into independently identifiable Research Objects and, when justified, into research notes. A conversation is provenance, not itself a research note.

Core pipeline:

Conversation
→ Research Object Detection
→ Boundary / Decomposition
→ Question Normalization
→ Provisional Classification
→ Candidate Document Type
→ Evidence Mapping
→ Claim Decomposition
→ Transformation Trace
→ SARA
→ Final Reclassification
→ Research Note Generation
→ Relation Mapping
→ D9 Candidate Gate
→ Network-level SARA
→ Revision Loop
→ Re-verification
→ Promotion Re-entry

## 2. Invocation and Operational Adapter

The engine is callable through the project-level Research Note one-stop adapter. Explicit triggers include `/연구노트` and `/변환`; equivalent natural-language requests are accepted when intent is unambiguous. The adapter orchestrates generation, existing-note consistency checking, Notion property mapping, persistence, and post-write verification. The adapter does not change the engine's epistemic semantics.

Canonical operational contract: `protocol/research_note_one_stop_pipeline_v0.1.md`.

A successful write is a persistence event, not epistemic verification. Locked or inaccessible targets must not be bypassed, and failed writes must not be reported as saved.

## 3. Research Object

Candidate object types:
- Research Question
- Claim
- Concept
- Phenomenon
- Hypothesis
- Model
- Evidence Problem
- Contradiction
- Research Gap

Split when an object has an independent question, purpose, evidence structure, conclusion, or follow-up.

Do not force all conversation content into notes.

## 4. Classification

Primary Purpose: max 1. Secondary Purpose: 0+.

Purpose is distinct from:
- Question Operator
- Research Design
- Method
- Evidence/Source
- Domain
- R&D Orientation
- Claim/Epistemic Status
- Knowledge Product
- Document Type
- Review Type
- Synthesis Operation

Initial classification is provisional. Evidence may trigger RETAIN, RECLASSIFY, SPLIT, MERGE, UPGRADE, or DOWNGRADE.

## 5. Candidate Document Types

D1 Exploratory  
D2 Descriptive/Current State  
D3 Concept Analysis  
D4 Relation/Impact Analysis  
D5 Mechanism/Process Analysis  
D6 Prediction  
D7 Evaluation  
D8 Literature/Evidence Synthesis  
D9 Integrated Synthesis

Document Type is a representation/output structure, not a truth state.

## 6. Evidence Mapping

Evidence roles:
- SUPPORT
- CONTRADICT
- CONTEXT
- ILLUSTRATE
- BACKGROUND

Source ≠ Evidence. Evidence ≠ Verification.

Evidence is mapped to claims or relations rather than automatically attached to an entire note.

## 7. Claim Transformation Traceability (가칭)

Integrated structures must be decomposed into truth-evaluable claims.

A Transformation Event records how an input becomes an output relevant to a claim.

Minimum fields:
- Transformation ID
- Input Reference(s)
- Transformation Type
- Output Reference(s)
- Target Claim(s)
- Evidence Role
- Validation State
- Provenance
- Revision Reference

Candidate transformation types:
ATTRIBUTE, MEASURE, ANALYZE, SYNTHESIZE, MODEL, GENERALIZE, INTERPRET, RECLASSIFY.

Transformation Event ≠ Evidence, Verification, Claim, Research Purpose, or Method.

## 8. SARA

SARA is:
Verification → Revision → Re-verification.

It is a verification/revision lifecycle, not approval and not agreement.

Claim state may move non-monotonically:
HYPOTHESIS → SUPPORTED
SUPPORTED → PARTIALLY_SUPPORTED
SUPPORTED → CONTRADICTED
HYPOTHESIS → UNVERIFIED

A state mutation requires an explicit Verification/Revision record.

## 9. Provenance

Interpretive provenance:
SOURCE/TEXT
→ AUTHORIAL REPRESENTATION
→ SCHOLARLY INTERPRETATION
→ PROJECT INTERPRETATION
→ HISTORICAL ATTRIBUTION
→ MODEL PROPOSAL

Empirical provenance:
SOURCE/PROTOCOL
→ MEASUREMENT
→ RAW DATA
→ ANALYSIS
→ RESULT
→ EVIDENCE
→ CLAIM

Synthesis provenance:
STUDY
→ STUDY RESULT
→ STUDY EVIDENCE
→ SYNTHESIS METHOD
→ SYNTHESIS RESULT
→ SYNTHESIS EVIDENCE
→ SYNTHESIS CLAIM

Model provenance:
MODEL SPECIFICATION
→ TRAINING DATA
→ FITTING
→ MODEL STATE
→ MODEL OUTPUT
→ VALIDATION
→ PREDICTIVE EVIDENCE
→ FORECAST CLAIM

## 10. Revision Lifecycle

Revision is non-destructive.

Version 1
→ Verification
→ Revision Event
→ Version 2
→ Re-verification
→ Current State

Previous states remain queryable.

Mutation may include:
- claim downgrade
- claim reformulation
- evidence remapping
- transformation invalidation
- relation qualification
- research-gap extraction
- document-type reclassification

## 11. Branch / Conflict / Merge

Parallel revisions are preserved as branches.

Conflict ≠ Error.

If branches are reconcilable:
Branch A + Branch B
→ Reconciliation Transformation
→ New Claim
→ Merge-level SARA

Merge does not inherit verification automatically.

If branches cannot be reconciled:
- preserve both
- record the appropriate relation
- preserve scope and conditions
- optionally create a new Research Object asking what explains the conflict

Branch ≠ Truth. Merge ≠ Agreement. Synthesis ≠ Consensus.

## 12. D9 Promotion

D9 Gate:
G1 Relation
G2 Higher-order Question
G3 Novel Structure
G4 Claim Decomposition
G5 Evidence Mapping
G6 Network-level SARA

D9 PROMOTED requires G1–G6 PASS.

D9 PROMOTED ≠ Model VERIFIED.

If G6 is partial, revision is required and promotion re-entry occurs after affected components are rechecked.

## 13. Human Final Agency

The human remains the final epistemic decision authority.

Automation must not:
- promote hypotheses to verified claims
- choose a winning branch solely by model preference
- infer missing evidence
- treat agreement as verification
- silently overwrite revision history

## 14. Core Invariants

MODE ≠ OPERATION  
MODE ≠ STATE  
CLAIM ≠ PREMISE  
STATE ≠ EVIDENCE  
EVIDENCE ≠ VERIFICATION  
VERIFICATION ≠ AGREEMENT  
AGREEMENT ≠ EVIDENCE  
SOURCE ≠ SIMULATION  
AUTHOR_CLAIM ≠ MODERN_INTERPRETATION  
HISTORICAL ≠ CONTEMPORARY  
CHECKPOINT ≠ EVIDENCE  
PURPOSE ≠ METHOD  
PURPOSE ≠ DOCUMENT TYPE  
QUESTION ≠ HYPOTHESIS  
CLAIM ≠ EVIDENCE  
RESEARCH NOTE ≠ EVIDENCE  
SYNTHESIS ≠ EVIDENCE  
TRANSFORMATION EVENT ≠ EVIDENCE  
TRANSFORMATION EVENT ≠ VERIFICATION  
TRANSFORMATION EVENT ≠ CLAIM  
OPERATION ≠ RESULT  
RESULT ≠ CLAIM  
CONFLICT ≠ ERROR  
REVISION ≠ REPLACEMENT  
BRANCH ≠ TRUTH  
MERGE ≠ AGREEMENT  
CONSENSUS ≠ VERIFICATION

## 15. Baseline Status

v0.4 is a **baseline candidate**, not a final standardized specification. T2–T13 provided structural stress-test evidence; external academic validity is a separate question.


## 15. AI Authorship / Provenance Disclosure Layer

AI authorship disclosure is a cross-cutting presentation/provenance layer of the Research Note Engine and One-Stop adapter. It is not a new epistemic entity.

Every generated/structured Research Note must expose:

**AI 작성·구조화 연구노트**

and retain generation provenance. The structured disclosure uses the existing `confession_report` representation where available.

Local attribution may distinguish:
- A1 AI-generated
- A2 AI-structured
- A3 Human-authored
- A4 Human-edited
- A5 Source-derived

These labels describe authorship/provenance, not epistemic state. Uncertain local attribution must remain unresolved rather than inferred.

## 16. Integrated Validation Status

T14–T50 established the current semantic, lifecycle, template, traceability, D9, and one-stop regression baseline. T51–T56 additionally established AI disclosure/provenance semantics and full-pipeline semantic integration for the tested scope.

Current status:
- semantic architecture: CLOSED FOR TESTED SCOPE
- template architecture: CLOSED FOR TESTED SCOPE
- lifecycle / branch / merge semantics: CLOSED FOR TESTED SCOPE
- D9 network-level semantics: CLOSED FOR TESTED SCOPE
- one-stop orchestration semantics: CLOSED FOR TESTED SCOPE
- AI disclosure integration: CLOSED FOR TESTED SCOPE
- live persistence verification: OPEN / CAPABILITY-BOUND
- empirical generation validation: OPEN

These are project-level validation states, not claims of external academic validation.
