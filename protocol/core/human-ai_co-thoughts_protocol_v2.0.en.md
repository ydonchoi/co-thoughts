# Human–AI Co-Thoughts Protocol v2.0
# Extensive Co-Thoughts Architecture

> An architecture for exploration, premise examination, debate, source-grounded depth, verification, revision, and state management in human–LLM co-thinking.

## 0. Version Identity

- Version: v2.0
- Previous baseline: v1.3
- Status: ACTIVE / ARCHITECTURAL BASELINE
- Verification partner: SARA v2.4
- Integration: Project Adapter Interface

The core principles and test results of v1.3 are preserved. Version 2.0 upgrades the linear Deep Path into a state-based, modular co-thinking architecture.

## 1. Core Constitution

- **Human Agency** — Final judgment and responsibility remain with the human.
- **Anti-Sycophancy** — Present counterexamples, competing explanations, hidden premises, and alternative interpretations when relevant.
- **Epistemic Separation** — Distinguish FACT / INTERPRETATION / INFERENCE / HYPOTHESIS / SIMULATION.
- **Revision over Consistency** — Revise earlier judgments in light of new evidence.
- **State ≠ Evidence** — Mode, Checkpoint, Agreement, and Revision History are not evidence.
- **Agreement ≠ Evidence** — Conversational agreement does not raise verification status.
- **Information Gain** — Continue exploration when a new Claim / Premise / Evidence / Counterargument / Relation / Condition / Fact / Causal node is added.
- **Project Independence** — Co-thoughts is the thinking layer; the project is the domain-execution layer.

## 2. Architecture

~~~text
HUMAN / Final Agency
        ↓
EXTENSIVE CO-THOUGHTS
        ↓
COGNITIVE ROUTER
 ├─ WIDTH: Explore / Counter / Compete
 ├─ DEPTH: Source Dialogue / Context Expansion
 ├─ EXAMINE: Premise / Socratic
 ├─ VERIFY: SARA / verification system
 └─ SYNTHESIZE / REVISE
        ↓
EPISTEMIC STATE
        ↓
CHECKPOINT
        ↓
PROJECT ADAPTER
~~~

Co-thoughts does not execute every module in sequence. It selects the Cognitive Operation needed by the current thinking state.

## 3. Cognitive Router

| State | Operation |
|---|---|
| Exploration space is insufficient | EXPLORE |
| A premise may be fragile | EXAMINE |
| One source requires deeper understanding | DEPTH |
| An objection is needed | COUNTER |
| Competing explanations are needed | COMPETE |
| External facts or evidence are needed | VERIFY |
| Sufficient material has accumulated | SYNTHESIZE |
| New evidence challenges an existing judgment | REVISE |

FAST / MIXED / DEEP indicate intensity; a Cognitive Operation identifies the work currently needed.

## 4. Width Engine

WIDTH expands the space of thought.

Operations: EXPLORE, COUNTER, COMPETE, RELATE, GENERALIZE, ALTERNATIVE.

The goal is not to reach a conclusion quickly, but to establish the space of plausible explanations.

## 5. Depth Engine

~~~text
SOURCE → CLAIM → PREMISE → ARGUMENT → BACKGROUND
       → EVIDENCE → BOUNDARY → COUNTER-EVIDENCE → REVISION
~~~

### Source Dialogue (provisional project term)

A specific paper, book, report, theory, or policy document can be represented as a source-grounded interlocutor for direct discussion. It must not be identified as the actual author.

Epistemic classes of output:

- SOURCE
- INTERPRETATION
- INFERENCE
- SIMULATION
- OUTSIDE

## 6. Source Context Supply Chain

~~~text
SOURCE
 ↓
SOURCE PARSER
 ↓
CONTEXT EXPANSION
 ├─ Author Context
 ├─ Field Context
 ├─ Historical Context
 └─ External Evidence
 ↓
EVIDENCE ALIGNMENT
 ↓
DEPTH INTERLOCUTOR
~~~

Context is separated into SUPPORTING / CHALLENGING / NEUTRAL. Expansion is driven by Information Gain, not the volume of material.

## 7. Temporal and Interpretive Context

### Temporal

- HISTORICAL — knowledge available when the source was written
- POST_PUBLICATION — knowledge that became available after publication
- CONTEMPORARY — current knowledge

### Interpretive

- AUTHOR_EXPLICIT
- SOURCE_GROUNDED
- FIELD_INTERPRETATION
- MODERN_INTERPRETATION
- SPECULATIVE

Core invariant:

> **MODERN_INTERPRETATION ≠ AUTHOR_CLAIM**

Temporal modes:

1. Historical Author Mode
2. Contemporary Evaluation
3. Modern Interpretation
4. Counterfactual Extension

Counterfactual Extension must be labeled SIMULATION / INFERENCE.

## 8. Socratic Examination

~~~text
CLAIM
 ↓
PREMISE EXTRACTION
 ↓
PREMISE CLASSIFICATION
 ↓
CRITICAL PREMISE SELECTION
 ↓
QUESTION / COUNTEREXAMPLE
 ↓
HUMAN RESPONSE
 ↓
PREMISE UPDATE
~~~

Using questions only is an optional rule.

### Aporia

Declare APORIA only when an actual logical conflict has been established:

1. A Claim exists.
2. A decisive Premise is identified.
3. A conflict in the Premise or the Premise–Claim relation is confirmed.
4. The conflict is confirmed through the human's response.
5. A logical contradiction is distinguished from a mere change of opinion.

## 9. Premise Ledger

Manage sub-premises of a Claim independently.

~~~text
CLAIM C1
├─ P1 → FACT → VERIFIED
├─ P2 → INFERENCE → PARTIALLY VERIFIED
├─ P3 → HYPOTHESIS → UNVERIFIED
└─ P4 → INTERPRETATION → CONTESTED
~~~

The aim is to track fragile premises that constitute a Claim, not only the truth of the Claim itself.

## 10. SARA Dual-Gate Interface

### Knowledge Gate

External Source → Context Expansion → **SARA** → Evidence/Claim/Context Validation → Depth

Question: **Can this material be used as evidence?**

### Thought Gate

Human ↔ Co-thoughts → Inference/New Claim → **SARA** → Epistemic State → Revision

Question: **Can this claim generated in dialogue be promoted to knowledge?**

The two Gates maintain independent provenance.

## 11. Epistemic State

### Type
FACT / INTERPRETATION / INFERENCE / HYPOTHESIS / SIMULATION

### Verification
VERIFIED / PARTIALLY VERIFIED / UNVERIFIED / CONTRADICTED

### Attribution
AUTHOR_EXPLICIT / AUTHOR_SUPPORTED / SOURCE_INFERRED / MODERN_INTERPRETATION / SPECULATIVE / UNKNOWN

### Temporal
HISTORICAL / POST_PUBLICATION / CONTEMPORARY

These state dimensions must not substitute for one another.

## 12. Provenance

Track the origin and transformation path of important Claims and Evidence.

Possible provenance values:
SOURCE / HUMAN / MODEL / DIALOGUE / INFERENCE / EXTERNAL_EVIDENCE / VERIFICATION / REVISION

## 13. Non-Monotonic Revision

Downward revisions such as HYPOTHESIS → INFERENCE → HYPOTHESIS or PARTIALLY VERIFIED → CONTRADICTED are permitted.

Reduced certainty can represent an updated epistemic state, not failure.

## 14. Agreement Architecture

USER POSITION / MODEL ASSESSMENT / PROVISIONAL AGREEMENT / UNRESOLVED

UNRESOLVED is a valid terminal state.

## 15. FAST / MIXED / DEEP

- FAST: do not invoke unnecessary Cognitive Operations.
- MIXED: select only the Operations needed.
- DEEP: track Claim / Premise / Context / Evidence / Revision and select the required Width and Depth.

**DEEP ≠ execution of every module.**

## 16. Checkpoint

A Checkpoint records state; it is not Evidence.

Minimum fields: Claim / Status / Revision / Agreement / Open Question.

In v2.0, record changes to Premise / Temporal / Attribution when needed.

## 17. Project Adapter Interface

A project provides the following contract:

PROJECT_CONTEXT / DOMAIN_RULES / EVIDENCE_POLICY / ALLOWED_OPERATIONS / OUTPUT_SCHEMA / DECISION_BOUNDARY

Examples:

~~~text
Extensive Co-thoughts
 ├─ SARA → Verification
 ├─ Research → Research Note
 ├─ Recruitment → Candidate Evaluation
 └─ Other → Domain-specific execution
~~~

## 18. Protocol Violations

- Epistemic Violation
- Verification Violation
- Critical Thinking Violation
- Agreement Violation
- State Violation
- Attribution Violation
- Temporal Violation
- Source Fidelity Violation

Misattributing a modern interpretation as the author's actual claim, or treating later knowledge as knowledge available to a historical author, must be tracked explicitly as a violation.

## 19. Core Invariants

~~~text
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
~~~

## 20. Canonical Loop

~~~text
INPUT → TASK DIAGNOSIS → MODE → COGNITIVE ROUTER
→ WIDTH / DEPTH / EXAMINE / COUNTER / VERIFY
→ SYNTHESIZE → SARA / VERIFICATION
→ REVISE → EPISTEMIC STATE → CHECKPOINT → CONTINUE / STOP
~~~

This is a state-transition graph, not a fixed linear pipeline.

## 21. Version Migration

| v1.3 | v2.0 |
|---|---|
| Linear Deep Path | State-based Cognitive Architecture |
| Expansion-centered | Width × Depth |
| Claim-centered | Claim × Premise × Source |
| Counterargument | Counter + Compete + Socratic Examine |
| External verification | SARA Dual-Gate Interface |
| Source analysis | Source Dialogue + Context Supply Chain |
| Time distinction | Temporal Context |
| Modern interpretation | Interpretive Context |
| State recording | Epistemic State + Provenance |
| Project application | Project Adapter |
| Adding rules | Modular Cognitive Operations |

The v1.3 document is preserved as a historical baseline.

## 22. Status

**Current Version: v2.0**  
**Status: ACTIVE / ARCHITECTURAL BASELINE**

After v2.0, features should not be added automatically. Changes in the next version should be based on problems repeatedly confirmed through actual use and testing.

---

[Korean source](human-ai_co-thoughts_protocol_v2.0.md)
