# Research Note Generation Engine v0.4 (provisional project model)

Status: **BASELINE CANDIDATE**  
Scope: Research Note decomposition, classification, verification, traceability, revision, branch/merge, D9 synthesis promotion, and conversational one-stop execution through the Research Note adapter.

## 1. Purpose

The engine converts a conversation into independently identifiable Research Objects and, when justified, into Research Notes. A conversation is provenance, not itself a Research Note.

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

The engine is callable through the project-level Research Note one-stop adapter. Explicit triggers include `/연구노트` and `/변환`; equivalent natural-language requests are accepted when intent is unambiguous. The adapter orchestrates generation, existing-note consistency checking, Notion property mapping, persistence, and post-write verification. It does not change the engine's epistemic semantics.

Canonical operational contract: [Research Note One-Stop Pipeline v0.1](research_note_one_stop_pipeline_v0.1.md).

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

Split an object when it has an independent question, purpose, evidence structure, conclusion, or follow-up.

Do not force all conversation content into notes.

## 4. Classification

Primary Purpose: maximum 1. Secondary Purpose: zero or more.

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

- D1 Exploratory
- D2 Descriptive / Current State
- D3 Concept Analysis
- D4 Relation / Impact Analysis
- D5 Mechanism / Process Analysis
- D6 Prediction
- D7 Evaluation
- D8 Literature / Evidence Synthesis
- D9 Integrated Synthesis

Document Type is an output structure, not a truth state.

## 6. Evidence Mapping

Evidence roles:
- SUPPORT
- CONTRADICT
- CONTEXT
- ILLUSTRATE
- BACKGROUND

Do not fabricate Evidence. Preserve directness, source provenance, scope, and counter-evidence.

## 7. SARA and Epistemic Boundaries

Verification must remain independent from generation and persistence.

Mandatory distinctions:
- Source ≠ Evidence
- Claim ≠ Evidence
- Evidence ≠ Verification
- Research Note ≠ Evidence
- Transformation Event ≠ Claim / Evidence / Verification
- Revision ≠ Replacement
- Merge ≠ Agreement
- D9 Promotion ≠ Verification

Model agreement, checkpoint state, successful generation, or successful writing do not raise epistemic status by themselves.

## 8. Revision, Branch, and Merge

Revision preserves history and records what changed and why. Branches represent parallel revision states, not separate truth judgments. Merge integrates branches but does not imply agreement or verification.

## 9. D9 Promotion

A D9 candidate must pass relation, higher-order question, novel structure, claim decomposition, evidence mapping, and network-level SARA gates. D9 promotion does not mean every constituent Claim is verified.

## 10. AI Authorship / Provenance Disclosure

Every generated or structured Research Note must disclose AI participation at artifact level. Use the existing `confession_report` metadata where available. Human review/editing and source-derived content should be represented separately when known. Do not invent attribution precision.

## 11. Status and Closure

T51–T56 validate the AI-disclosure semantics and pipeline integration for the tested scope. Live durable Notion persistence, post-write verification, and broad empirical generation validation remain capability-bound or open. Do not report failed writes as saved.

---

[Korean source](research_note_generation_engine_v0.4.md)
