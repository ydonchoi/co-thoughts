# Co-Thoughts Execution Contract v0.1

Status: SOURCE-BACKED CONTRACT EVIDENCE
Protocol baseline: v1.3
Repository: ydonchoi/co-thoughts

## Purpose

This document records the executable semantics that can be supported by the v1.3 protocol source.

It does **not** claim that co-thoughts currently provides a software runtime, CLI, API, or callable execution service. Such a runtime was not identified in the repository evidence inspected for this contract.

## Execution Boundary

A co-thoughts execution is a protocol application to a current task.

```text
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
```

## Input Contract

A conforming execution MUST have:

1. A current task.
2. Sufficient conversational/contextual material to determine the task.
3. A selected cognitive mode: FAST, MIXED, or DEEP.

The protocol does not require every execution to traverse every stage.

## Mode Contract

- FAST: facts, definitions, calculations, simple tasks.
- MIXED: direct answer plus required analysis.
- DEEP: exploration, counterargument, verification, conceptualization, revision.

Mode is a property of the current task, not of the whole conversation.

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

The following distinctions are normative:

- Agreement ≠ Evidence
- Checkpoint ≠ Evidence
- Previous Verification ≠ Current Verification
- Plausibility ≠ Fact

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

## Stop / Transition Contract

Continuation is justified when a next step can add information, verification, explanation, or another material relation/condition.

If no meaningful information gain is expected, the execution may terminate with a provisional conclusion.

## Output Contract

A protocol execution should make the following distinguishable when applicable:

- selected Mode
- Claim(s)
- Epistemic Type
- Evidence / evidence status
- Verification status
- Revision
- provisional conclusion
- checkpoint/state change

The protocol does not require exposing all internal state to the human-facing response.

## Non-Claims

This contract MUST NOT be interpreted as evidence that co-thoughts currently has:

- a Python/TypeScript runtime;
- a CLI;
- an HTTP/API endpoint;
- a machine-readable request/response schema;
- an automated protocol executor;
- CI-based execution tests.

Those capabilities require separate repository evidence.

## Research OS Integration Boundary

For Research OS, co-thoughts can therefore be treated as a **source-backed Cognitive/THINK protocol contract**.

Research OS MUST NOT promote this contract into:

- ACT execution evidence;
- research verification evidence;
- scientific truth;
- a software execution success record.

A future CognitiveAdapter requires a concrete callable runtime or an explicitly implemented execution harness before it can be promoted beyond source-contract status.

## Evidence Basis

The contract is derived from the repository's README.md at the v1.3 baseline, including:

- project purpose and human/LLM role separation;
- FAST/MIXED/DEEP mode definitions;
- exploration and verification sections;
- Verification Gate;
- Information Gain and Stop Condition;
- Transition Gate;
- Claim & Epistemic Status;
- Agreement Control;
- Checkpoint and Sparse Checkpoint;
- protocol violation rules;
- v1.3 execution flow;
- core separation rules such as STATE ≠ EVIDENCE and AGREEMENT ≠ EVIDENCE.

This document is a provenance-preserving interpretation of those source rules, not a replacement for them.
