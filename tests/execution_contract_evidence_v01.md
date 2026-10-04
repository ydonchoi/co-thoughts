# Co-Thoughts Execution Contract Evidence Matrix v0.1

This matrix is a repository evidence record for the v1.3 protocol execution contract.

It is intentionally a **source/contract test matrix**, not a claim of automated runtime execution.

| ID | Contract property | v1.3 source basis | Expected result |
|---|---|---|---|
| CT-01 | Current task determines mode | Mode / Dynamic Mode Switching | Mode is task-local |
| CT-02 | FAST is protected from unnecessary deep procedure | Fast-Path Protected Zone | Simple tasks can terminate without deep protocol |
| CT-03 | DEEP permits exploration and counterargument | Exploration / Verification | Hypotheses and competing explanations remain allowed |
| CT-04 | Verification is distinct from exploration | Exploration vs Verification | Verification is a separate epistemic operation |
| CT-05 | Epistemic type is distinct from verification status | T10 / Claim & Epistemic Status | FACT/INFERENCE/HYPOTHESIS are not verification results |
| CT-06 | Agreement is not evidence | Agreement Control / T11 | Agreement cannot promote a claim to evidence |
| CT-07 | Checkpoint is not evidence | Checkpoint / T11 | State preservation cannot establish truth |
| CT-08 | Revision is non-monotonic | T10 / Revision | Claims may be revised back to another epistemic state |
| CT-09 | Continuation depends on information gain | Information Gain / Transition Gate | No meaningful gain permits termination |
| CT-10 | Checkpoints are sparse | Sparse Checkpoint | Only material state changes require checkpointing |
| CT-11 | Human remains final decision/owner | Project purpose | Protocol does not transfer final responsibility to LLM |
| CT-12 | Software runtime is not implied | Repository inspection | No runtime/API/CLI claim may be inferred from protocol text alone |

## Promotion Rule

A Research OS CognitiveAdapter MUST NOT be marked runtime-tested solely from this matrix.

Promotion beyond SOURCE-CONTRACT-IDENTIFIED requires a concrete executable implementation and an independent execution test.

## Current Verdict

- Protocol semantics: **SOURCE-BACKED**
- Execution contract: **DEFINED**
- Automated runtime: **UNVERIFIED**
- CognitiveAdapter runtime compatibility: **UNVERIFIED**
- Research verification capability: **NOT ESTABLISHED**

The evidence boundary is intentional: it prevents a protocol specification from being mistaken for an executable runtime or research verification system.
