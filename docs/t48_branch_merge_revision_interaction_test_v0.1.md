# T48 — Branch / Merge / Revision Decision Interaction Test v0.1

Status: **PASS — BRANCH / MERGE / REVISION SEMANTICS CONSISTENT WITH LIFECYCLE MODEL**

## 1. Purpose

T48 tests whether the one-stop decision states:

- NO_CHANGE
- REVISION
- EXTENSION
- NEW
- BLOCKED

remain semantically coherent when a Research Object has:

- parallel revisions;
- divergent Claims or interpretations;
- unresolved conflicts;
- reconciliation;
- merge-level synthesis;
- later re-verification.

The primary risk is collapsing Branch, Merge, Revision, and Verification into one operation.

## 2. Governing Distinctions

The following invariants are mandatory:

- **Branch ≠ Truth**
- **Branch ≠ Error**
- **Conflict ≠ Error**
- **Revision ≠ Replacement**
- **Merge ≠ Agreement**
- **Merge ≠ Verification**
- **Reconciliation ≠ Verification**
- **Synthesis ≠ Consensus**
- **Consensus ≠ Verification**
- **D9 Promotion ≠ Verification**

A branch records a distinct lifecycle path.

A merge records a new transformation/reconciliation path.

Neither operation determines epistemic truth by itself.

## 3. Branch Semantics

A Branch is appropriate when parallel analyses of the same Research Object must be preserved independently.

Examples:

- different interpretations of the same Evidence;
- competing mechanism models;
- alternative causal explanations;
- independent revisions made from different evidence subsets;
- unresolved methodological choices.

A Branch must preserve:

- parent/reference state;
- branch identifier;
- branch-specific Claims;
- branch-specific Evidence mappings;
- branch-specific Transformations;
- provenance;
- epistemic states;
- revision history.

A branch must not be labeled as “the correct answer” merely because it was generated later or preferred by the model.

## 4. Branch and Decision States

Branch creation does not automatically imply NEW.

If the branches address the same Research Object and lifecycle, the branch is part of that object's revision structure.

However, if a branch develops an independently answerable question, evidence structure, conclusion, and lifecycle, it may require a NEW Research Object.

Therefore:

**Branch identity is not sufficient to determine NEW vs REVISION.**

Research Object identity remains the controlling criterion.

## 5. Conflict Semantics

Conflict may exist between:

- Claims;
- Evidence interpretations;
- Relations;
- Transformations;
- taxonomy classifications;
- boundary conditions;
- model specifications.

Conflict should be represented explicitly.

Do not resolve conflict merely by:

- choosing the newest branch;
- choosing the majority view;
- choosing the model-preferred interpretation;
- averaging incompatible claims;
- deleting the weaker branch.

Conflict resolution requires an explicit reconciliation operation when reconciliation is actually possible.

## 6. Merge Semantics

A Merge is not a silent replacement.

When Branch A and Branch B are reconcilable:

**Branch A + Branch B**
→ **Reconciliation Transformation**
→ **New Claim(s)/Result(s)**
→ **Merge-level SARA**

The merge result is a new derived state.

The source branch states remain historically queryable.

Verification does not transfer automatically from either branch to the merged result.

## 7. Merge Outcomes

### M1 — Full Reconciliation

The branches are compatible under an explicitly stated scope/condition.

Expected:

- reconciliation Transformation;
- new integrated Claim/Result;
- provenance from both branches;
- verification status evaluated independently.

Decision:
**REVISION** of the Research Object if the merged result changes current state.

### M2 — Conditional Reconciliation

The branches differ only because of identifiable conditions.

Expected:

- preserve both branch Claims;
- add boundary/condition structure;
- optionally create an integrated Claim;
- no forced consensus.

Decision:
**EXTENSION** if the original state remains valid and the conditional structure is additive; **REVISION** if the original claim scope/state changes.

### M3 — Irreconcilable Conflict

No justified reconciliation is available.

Expected:

- preserve both branches;
- record conflict;
- retain separate epistemic states;
- optionally create a new Research Object asking what explains the conflict.

Decision:
**NO_CHANGE** to the existing state if the branches are already preserved and no new synthesis is requested; **EXTENSION** if the conflict analysis adds bounded material; **NEW** if the explanatory question has an independent lifecycle.

### M4 — False Merge

A model attempts to combine incompatible claims without a valid reconciliation basis.

Expected:
**BLOCKED / FAIL**

No merge should be persisted as a resolved state.

## 8. Controlled Fixture Set

### T48-01 — Parallel Interpretations

Branch A:
Evidence E1 interpreted as supporting mechanism M1.

Branch B:
The same E1 is interpreted as consistent with alternative mechanism M2.

Expected:

- same Research Object;
- two branches;
- conflict/alternative interpretation preserved;
- no automatic NEW;
- no automatic verification.

Result: **PASS**

### T48-02 — Branch-Specific Evidence

Branch A adds E2.

Branch B adds E3.

Both evaluate the same question Q1.

Expected:

- preserve branch-specific Evidence;
- branch-specific Claims;
- no evidence collapse;
- no automatic merge.

Result: **PASS**

### T48-03 — Reconciliable Branches

Branch A:
C1 holds under condition A.

Branch B:
C2 holds under condition B.

Conditions are explicitly compatible.

Expected:

- reconciliation Transformation;
- integrated conditional Claim C3;
- provenance from both branches;
- independent verification of C3.

Decision:
**EXTENSION** if C1/C2 remain valid; **REVISION** if prior unrestricted claim must be narrowed.

Result: **PASS**

### T48-04 — Irreconcilable Claims

Branch A:
C1 = X increases Y.

Branch B:
C2 = X decreases Y.

No scope or methodological explanation resolves the conflict.

Expected:

- preserve both;
- explicit conflict relation;
- no synthetic compromise claim;
- no automatic merge;
- optional NEW Research Object asking what explains the contradiction.

Result: **PASS**

### T48-05 — Merge Produces New Synthesis

Branches contain distinct but compatible structures.

User requests:
“두 분석을 통합해서 새로운 설명을 만들어 보자.”

Expected:

- synthesis Transformation;
- new Claim/Result;
- source branches preserved;
- integrated result receives its own epistemic state;
- merge is not verification.

Decision:
Usually **REVISION** if it updates the same Research Object; **NEW** if the synthesis has an independent Research Object/lifecycle.

Result: **PASS**

### T48-06 — New Evidence After Merge

Merged Claim C3 was supported at an earlier verification point.

New Evidence E4 contradicts C3.

Expected:

- create Revision Event;
- preserve merged state;
- re-evaluate C3;
- potentially create new Transformation and C4;
- SARA re-entry.

Decision:
**REVISION**

Result: **PASS**

### T48-07 — Branch Becomes Independent

A branch begins as an alternative interpretation of Q1 but later develops:

- independent question Q2;
- independent evidence structure;
- independent conclusion;
- independent lifecycle.

Expected:

- split from branch structure into a NEW Research Object;
- preserve provenance relation to parent.

Result: **PASS**

### T48-08 — Model Preference as False Reconciliation

The model chooses Branch A because it “looks more plausible” and silently discards Branch B.

Expected:
**FAIL / BLOCKED**

Reason:
Model preference is not a reconciliation basis.

Result: **PASS — safety condition detected.**

### T48-09 — Merge Confused with Verification

Two branches agree on the same conclusion.

Expected:

- merge/reconciliation may be recorded;
- agreement does not create Verification;
- Claim state remains dependent on actual Verification.

Result: **PASS**

### T48-10 — D9 Interaction

Multiple existing notes are integrated through D9 while some source branches contain unresolved conflicts.

Expected:

- source branch conflicts remain visible;
- D9 integrated structure does not erase branch provenance;
- D9 Gate evaluated independently;
- D9 PROMOTED does not make source Claims VERIFIED;
- integrated Claims receive their own Evidence/Transformation mapping.

Result: **PASS**

## 9. Decision Matrix

| Branch/Merge condition | Decision |
|---|---|
| Same object, parallel path | Branch within existing lifecycle |
| Same object, additive branch material | EXTENSION where state unchanged |
| Same object, merged result changes state | REVISION |
| Independent branch lifecycle | NEW Research Object |
| Unresolved conflict already represented | NO_CHANGE |
| New bounded conflict analysis | EXTENSION |
| Independent conflict-explanation question | NEW |
| Reconciliation basis unavailable | BLOCKED |
| Persistence target unavailable | BLOCKED persistence; no mutation |

## 10. Interaction with T47

T47 controls Research Object identity and mutation decision.

T48 adds branch-aware interpretation:

**Research Object identity**
→ **Branch status**
→ **Conflict status**
→ **Reconciliation possibility**
→ **Lifecycle consequence**
→ **NO_CHANGE / REVISION / EXTENSION / NEW / BLOCKED**

Therefore Branch is not itself a sixth decision state.

It is lifecycle structure that informs the existing five decisions.

## 11. Traceability Requirements

Branch and merge operations must preserve:

- parent/branch references;
- branch-specific Claims;
- Evidence and roles;
- Transformations;
- Relations/conflicts;
- provenance;
- Verification state;
- Revision Events;
- merge/reconciliation Transformation;
- SARA state.

For a merged Claim, reverse trace must remain possible:

**Merged Claim**
← **Reconciliation/Synthesis Transformation**
← **Branch Claims**
← **Branch Evidence**
← **Original sources/inputs**

## 12. Safety Tests

### S1 — No branch truth inflation

Later/newer branch ≠ truer branch.

PASS.

### S2 — No conflict deletion

Conflict cannot be removed solely for cleaner prose.

PASS.

### S3 — No merge verification inflation

Merge ≠ Verification.

PASS.

### S4 — No consensus inflation

Agreement between branches ≠ proof.

PASS.

### S5 — No model-preference reconciliation

Model preference cannot substitute for reconciliation evidence.

PASS.

### S6 — Historical preservation

Merge cannot overwrite source branch history.

PASS.

### S7 — D9 independence

D9 promotion remains independent of source/merge verification.

PASS.

### S8 — New-object protection

An independently answerable branch cannot be forced into the parent Research Object indefinitely.

PASS.

## 13. Result

**T48 = PASS**

The current lifecycle model can represent:

- parallel branches;
- unresolved conflict;
- conditional reconciliation;
- full reconciliation;
- merge-level synthesis;
- post-merge revision;
- branch-to-new-object splitting.

No additional epistemic entity is required.

The critical architectural conclusion is:

> **Branch is lifecycle structure; Merge is a Transformation; Revision/Extension/New/Blocked are decision outcomes.**

This prevents Branch from becoming an implicit truth hierarchy and prevents Merge from becoming implicit verification.

## 14. Validation Boundary

T48 is a controlled semantic test.

It does not establish empirical performance over a large real-world corpus.

Remaining validation:

1. repeated real-conversation branch/merge cases;
2. human review of reconciliation decisions;
3. branch/merge persistence in writable Notion state;
4. larger D9 integration cases;
5. interaction with actual one-stop generation outputs.

## 15. Architecture Decision

**RETAIN CURRENT CORE MODEL.**

No new Branch entity or Merge Document Type is required beyond the existing lifecycle/Transformation representation.

Branch ID and Revision/Relation provenance remain lifecycle metadata/records.

## 16. Next Test

**T49 — D9 Integration / Network-Level SARA Test**

T49 should test whether D9 integration can preserve source-note Claim states while independently evaluating integrated Claims and network-level verification/revision.

## 17. Boundary

This is a project-level operational test and specification. It is not an established academic or industry standard.

Human remains final epistemic decision authority.
