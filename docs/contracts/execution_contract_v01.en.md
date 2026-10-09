# Co-Thoughts Execution Contract v0.1

Status: **SOURCE-BACKED CONTRACT + REFERENCE HARNESS**  
Protocol baseline: v1.3  
Repository: `ydonchoi/co-thoughts`

## Purpose

This document records executable semantics supported by the v1.3 protocol source and the minimal reference harness in `execution.py`.

The harness implements the **execution boundary and invariant checks**. It does not implement an LLM reasoning model, external research search, or epistemic truth verification.

## Execution Boundary

A co-thoughts execution applies the protocol to a current task.

~~~text
Input: Current Task + available context
        ↓
Mode selection
        ↓
Claim identification
        ↓
Epistemic Type
        ↓
Exploration / counterargument / competing explanation
        ↓
Evidence search
        ↓
Verification
        ↓
Revision
        ↓
Information Gain / Transition Gate
        ↓
Provisional conclusion
        ↓
Sparse Checkpoint when material state changed
~~~

The reference harness accepts these execution-state components and preserves their distinctions. It does not invent missing reasoning results.

## Input Contract

A conforming execution MUST have:
1. A current task.
2. Sufficient conversational/contextual material to determine the task.
3. A selected cognitive mode: FAST, MIXED, or DEEP.

The protocol does not require every execution to traverse every stage.

## Mode Contract

- FAST: facts, definitions, calculations, and simple tasks.
- MIXED: a direct answer plus the analysis required.
- DEEP: exploration, counterargument, verification, conceptualization, and revision.

Mode is a property of the current task, not of the entire conversation.

## Claim Contract

When claim-level management is appropriate, claims may carry:
- FACT
- INTERPRETATION
- INFERENCE
- HYPOTHESIS
- UNKNOWN

Epistemic Type MUST NOT be treated as equivalent to Verification Status.

## Verification Boundary

The protocol identifies facts, numbers, statistics, causal claims, academic claims, current information, and real cases as candidates for external verification.

Normative distinctions:
- Agreement ≠ Evidence
- Checkpoint ≠ Evidence
- Previous Verification ≠ Current Verification
- Plausibility ≠ Fact

The reference harness therefore returns `verification_status=UNVERIFIED` unless a separate verifier supplies a result. It never converts execution success into research verification.

## Revision Contract

Execution MUST remain revision-capable. A claim may move between epistemic states; the protocol explicitly permits non-monotonic revision.

## Checkpoint Contract

A checkpoint records state rather than establishing evidence.

A sparse checkpoint may record:
- Claim
- Status
- Revision
- Agreement
- Open Question

It should be produced only for material state changes.

The reference harness rejects a checkpoint explicitly marked as evidence.

## Stop / Transition Contract

Continuation is justified when a next step can add information, verification, explanation, or another material relation/condition.

If no meaningful information gain is expected, the execution may terminate with a provisional conclusion.

The reference harness preserves the caller-supplied transition decision; it does not manufacture information gain.

## Output Contract

When applicable, distinguish:
- selected Mode
- Claim(s)
- Epistemic Type
- Evidence / evidence status
- Verification status
- Revision
- provisional conclusion
- checkpoint/state change

The protocol does not require exposing all internal state in the user-facing response.

## Current Reference Implementation

`execution.py` provides:
- `CoThoughtsExecutionRequest`: validated input boundary;
- `CoThoughtsReferenceExecutor.run()`: deterministic reference execution harness;
- mode validation for FAST/MIXED/DEEP;
- epistemic-type validation;
- checkpoint/evidence separation;
- explicit `execution_status` and `verification_status` separation.

`tests/test_execution.py` exercises these boundaries.

## Non-Claims

This contract MUST NOT be interpreted as evidence that co-thoughts currently has:
- an autonomous LLM reasoning engine;
- external research retrieval;
- an HTTP/API endpoint;
- a production execution service;
- automatic epistemic verification;
- scientific truth validation.

The reference harness is callable software, but execution success only means that the supplied protocol-state envelope passed the harness checks.

## Research OS Integration Boundary

For Research OS, co-thoughts can be treated as a **source-backed Cognitive/THINK protocol contract with a minimal callable reference harness**.

Research OS MUST NOT promote this harness into:
- ACT execution evidence;
- research-verification evidence;
- scientific truth;
- evidence merely because it returned `SUCCEEDED`.

A future production CognitiveAdapter still requires an explicit LLM/runtime execution strategy, real dialogue execution fixtures, provenance mapping, and independent integration/adversarial tests.

## Evidence Basis

The contract is derived from the repository's README at the v1.3 baseline, including project purpose, human/LLM role separation, FAST/MIXED/DEEP modes, exploration and verification, Verification Gate, Information Gain and Stop Condition, Transition Gate, Claim/Epistemic Status, Agreement Control, Checkpoint and Sparse Checkpoint, protocol violations, execution flow, and separation rules such as STATE ≠ EVIDENCE and AGREEMENT ≠ EVIDENCE.

Implementation details are additionally supported by `execution.py` and `tests/test_execution.py`.

This document is a provenance-preserving interpretation of those source rules, not a replacement for them.

---

[Korean source](execution_contract_v01.md)
