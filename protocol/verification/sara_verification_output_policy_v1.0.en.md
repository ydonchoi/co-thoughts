# SARA Verification Output Policy v1.0

> Output policy governing how SARA verification results are surfaced in co-thinking dialogue.

## 0. Purpose

SARA verification is not a post-hoc assessment attached to the end of an answer. It is part of a quality-control loop that assesses Claim, Evidence, and Reasoning states and prompts Revision and Re-verification when needed.

The depth of internal verification is separate from the amount of information exposed to the user by default.

**Core principle:** Verification should be performed as required, while output starts with the minimum sufficient information and expands into a detailed audit on request.

## 1. Scope

This policy applies to the following structures in Co-thoughts v2.0:
- SARA Knowledge Gate
- SARA Thought Gate
- Epistemic State
- Provenance
- Revision / Re-verification
- Project Adapter OUTPUT_SCHEMA

This document does not define SARA's decision algorithm. It defines how Co-thoughts represents and expands the verification state returned by SARA.

## 2. Verification Lifecycle

~~~text
CLAIM / EVIDENCE
      ↓
SARA VERIFICATION
      ↓
ISSUE DETECTION
      ↓
REVISION (when needed)
      ↓
RE-VERIFICATION
      ↓
EPISTEMIC STATE UPDATE
      ↓
OUTPUT
~~~

Verification is not merely a final score.

## 3. Epistemic Separation

Verification output must not conflate:
- EVIDENCE ≠ VERIFICATION
- VERIFICATION ≠ AGREEMENT
- MODEL AGREEMENT ≠ TRUTH
- REPLICATION STABILITY ≠ CORRECTNESS
- STATE ≠ EVIDENCE

Retain the epistemic classes FACT / INTERPRETATION / INFERENCE / HYPOTHESIS / SIMULATION.

## 4. Default Output

For ordinary answers, display only a concise verification summary.

Example:

~~~text
☑️ Verification Results
🟢 Good
Key claims: 8 · Evidence coverage: 8/8 · Major issues: 0

[View detailed verification]
~~~

The default output may include only:
- final Verification State;
- number of key Claims;
- number of Evidence-linked Claims;
- number of Critical Issues;
- unresolved Claims when relevant.

Do not automatically expose lengthy Claim/Evidence/audit details in ordinary responses.

## 5. Verification States

| State | User-facing meaning |
|---|---|
| VERIFIED | Core targets have been sufficiently confirmed |
| PARTIALLY VERIFIED | Only some targets have been confirmed |
| CONDITIONAL | Holds only under specified conditions or interpretive scope |
| UNRESOLVED | Available Evidence is insufficient to decide |
| CONTRADICTED | Contrary Evidence or a conflict has been identified |
| UNSUPPORTED | Current Evidence does not support the Claim |

Do not automatically collapse CONDITIONAL / UNRESOLVED / UNSUPPORTED into a single “error” category. They represent different epistemic states.

## 6. Automatic Escalation

Even without a user request for a detailed audit, show a summary-level warning when:
- a critical Claim is UNSUPPORTED;
- a material mismatch exists between a key Claim and Evidence;
- the conclusion is materially stronger than its Evidence;
- an important source conflict exists;
- a critical issue remains after Revision.

The purpose is to prevent material epistemic risk from being overlooked, not to reassure the user.

## 7. On-Demand Detailed Audit

When the user requests detailed verification, the verification process, or evidence checking, expand:

### 7.1 Claim Analysis
- Claim ID and content
- Epistemic class
- Verification state
- Attribution
- Temporal context

### 7.2 Evidence Mapping
- linked Evidence
- Evidence provenance
- direct or indirect support
- scope mismatch between Evidence and Claim
- counter-evidence/source conflict

### 7.3 Reasoning Integrity
- logical leaps
- overgeneralization
- overinterpretation of causality
- undefined key concepts
- conclusions stronger than Evidence
- self-contradiction

### 7.4 Uncertainty
- unresolved areas
- causes of uncertainty
- competing explanations
- additional Evidence required

### 7.5 Revision
- Claim to revise
- state before Revision
- state after Revision
- Re-verification result

### 7.6 Human Judgment
- issues that AI verification cannot decide
- areas requiring final human judgment

## 8. Audit Trail

Detailed audit must not expose raw internal reasoning text.

Instead, provide verifiable provenance:

~~~text
CLAIM
  ↓
EVIDENCE
  ↓
VERIFICATION FINDING
  ↓
REVISION
  ↓
RE-VERIFICATION
  ↓
FINAL STATE
~~~

The audit trail should make it possible to trace the basis for each assigned verification state.

## 9. Metrics

Do not present “accuracy / recall / reliability” as arbitrary probability values without evidence.

When useful, use defined measures:
- **Evidence Coverage**: proportion of key Claims in scope linked to Evidence
- **Verification Coverage**: proportion of identified Claims requiring verification for which verification was actually performed
- **Inference Ratio**: proportion of Claims that depend on model interpretation/inference
- **Replication Stability**: extent to which a state remains stable under repeated application of the same verification conditions
- **Model Agreement**: degree of agreement among multiple models

Model Agreement is not a proxy for Truth. Replication Stability is not a proxy for Correctness.

Use standard statistical Accuracy / Precision / Recall only when ground truth and an appropriate evaluation set exist.

## 10. Output Levels

- **Level 0 — Inline Summary:** display only the minimum state in ordinary answers.
- **Level 1 — Verification Summary:** provide key Claim/Evidence/Issue summaries when requested.
- **Level 2 — Full Audit:** expand Claim/Evidence/Reasoning/Uncertainty/Revision/Provenance when requested or required by a research/analysis context.

## 11. Human Agency

SARA does not replace the human's final judgment.

The following may remain matters for human judgment:
- normative judgments
- value judgments
- policy choices
- attribution of responsibility
- choice of definitions
- future predictions with insufficient Evidence

## 12. Integration with Co-thoughts v2.0

~~~text
COGNITIVE ROUTER
      ↓
VERIFY
      ↓
SARA DUAL GATE
      ↓
REVISION / RE-VERIFICATION
      ↓
EPISTEMIC STATE
      ↓
CHECKPOINT
      ↓
OUTPUT
      ├─ default: summary
      └─ requested: detailed audit
~~~

Verification-output detail is independent of the intensity of the Cognitive Operation.

**DEEP verification ≠ verbose default output**

## 13. Non-Goals

This policy does not aim to:
- disclose Chain-of-Thought;
- reduce verification to a single probability;
- treat model agreement as evidence of truth;
- append a long verification report to every answer automatically;
- replace Human Judgment with automated decisions.

## 14. Status

**Policy:** SARA Verification Output Policy v1.0  
**Applies to:** Co-thoughts v2.0  
**Status:** ACTIVE POLICY EXTENSION

---

[Korean source](sara_verification_output_policy_v1.0.md)
