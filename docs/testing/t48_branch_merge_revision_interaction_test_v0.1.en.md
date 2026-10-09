# T48 — Branch / Merge / Revision Decision Interaction Test v0.1

Status: **PASS — BRANCH / MERGE / REVISION SEMANTICS CONSISTENT WITH LIFECYCLE MODEL**

## 1. Purpose
T48 tests whether the one-stop decision states NO_CHANGE, REVISION, EXTENSION, NEW, and BLOCKED remain coherent when a Research Object has parallel revisions, divergent Claims/interpretations, unresolved conflicts, reconciliation, merge-level synthesis, or later re-verification.

The primary risk is collapsing Branch, Merge, Revision, and Verification into one operation.

## 2. Governing Distinctions
Mandatory invariants:
- Branch ≠ Truth
- Branch ≠ Error
- Conflict ≠ Error
- Revision ≠ Replacement
- Merge ≠ Agreement
- Merge ≠ Verification
- Reconciliation ≠ Verification
- Synthesis ≠ Consensus
- Consensus ≠ Verification
- D9 Promotion ≠ Verification

A Branch records a distinct lifecycle path. A Merge records a new transformation/reconciliation path. Neither operation determines epistemic truth by itself.

## 3. Branch Semantics
A Branch is appropriate when parallel analyses of the same Research Object must be preserved independently: different interpretations of the same Evidence, competing mechanism models, alternative causal explanations, independent revisions based on different evidence subsets, or unresolved methodological choices.

A Branch must preserve:
- parent/reference state;
- branch identifier;
- branch-specific Claims;
- branch-specific Evidence mappings;
- branch-specific Transformations;
- provenance;
- epistemic states;
- revision history.

A branch must not be labeled “the correct answer” merely because it was generated later or preferred by the model.

## 4. Branch and Decision States
Branch creation does not automatically imply NEW. If branches address the same Research Object and lifecycle, the branch belongs to that object's revision structure.

If a branch develops an independently answerable question, evidence structure, conclusion, and lifecycle, it may require a NEW Research Object.

**Branch identity alone is insufficient to determine NEW vs REVISION.** Research Object identity remains controlling.

## 5. Conflict Semantics
Conflict may exist between Claims, Evidence interpretations, Relations, Transformations, taxonomy classifications, boundary conditions, or model specifications. Represent conflict explicitly.

Do not resolve conflict merely by selecting the newest branch, majority view, model-preferred interpretation, averaging incompatible Claims, or deleting the weaker branch.

Conflict resolution requires an explicit reconciliation operation when reconciliation is actually justified.

## 6. Merge Semantics
A Merge is not silent replacement.

When Branch A and Branch B can be reconciled:

**Branch A + Branch B → Reconciliation Transformation → New Claim(s)/Result(s) → Merge-level SARA**

The merge result is a new derived state. Source branch states remain historically queryable. Verification does not transfer automatically from either branch to the merged result.

## 7. Merge Outcomes

### M1 — Full Reconciliation
Branches are compatible within an explicitly stated scope/condition.

Expected: reconciliation Transformation; new integrated Claim/Result; provenance from both branches; independently assessed verification status.

Decision: **REVISION** of the Research Object if the merge changes current state.

### M2 — Conditional Reconciliation
Branches differ only due to identifiable conditions.

Expected: preserve both branch Claims; add boundary/condition structure; optionally create an integrated Claim; do not force consensus.

Decision: **EXTENSION** if the original state remains valid and conditional structure is additive; **REVISION** if original Claim scope/state changes.

### M3 — Irreconcilable Conflict
No justified reconciliation is available.

Expected: preserve both branches; record conflict; retain separate epistemic states; optionally create a NEW Research Object asking what explains the conflict.

Decision: **NO_CHANGE** if branches are already preserved and no synthesis is requested; **EXTENSION** if conflict analysis adds bounded material; **NEW** if the explanatory question has an independent lifecycle.

### M4 — False Merge
A model combines incompatible Claims without a valid reconciliation basis.

Expected: **BLOCKED / FAIL**. Do not persist the merge as a resolved state.

## 8. Controlled Fixture Set
- **T48-01 — Parallel Interpretations:** Branch A interprets E1 as supporting M1; Branch B regards the same E1 as consistent with M2. Expected: same Research Object, two branches, conflict preserved, no automatic NEW or Verification. **PASS.**
- **T48-02 — Branch-Specific Evidence:** Branch A adds E2; Branch B adds E3; both address Q1. Expected: preserve branch-specific Evidence/Claims, no evidence collapse, no automatic merge. **PASS.**
- **T48-03 — Reconcilable Branches:** C1 holds under A; C2 under B; conditions are compatible. Expected: reconciliation Transformation and integrated conditional C3 with both provenances and independent verification. EXTENSION if C1/C2 remain valid; REVISION if an unrestricted original Claim must be narrowed. **PASS.**
- **T48-04 — Irreconcilable Claims:** C1 says X increases Y; C2 says X decreases Y; no scope/method explanation resolves the conflict. Preserve both and explicit conflict; no synthetic compromise or automatic merge; optional NEW explanatory Research Object. **PASS.**
- **T48-05 — Merge Produces New Synthesis:** User asks to integrate two compatible analyses into a new explanation. Expected: synthesis Transformation, new Claim/Result, source branches retained, independent epistemic state; Merge ≠ Verification. Usually REVISION if it updates the same Research Object; NEW if the synthesis has an independent lifecycle. **PASS.**
- **T48-06 — New Evidence After Merge:** E4 contradicts previously supported merged C3. Expected: Revision Event; preserve merged state; re-evaluate C3; possibly new Transformation/C4; SARA re-entry. Decision: REVISION. **PASS.**
- **T48-07 — Branch Becomes Independent:** A branch that began as an alternative reading of Q1 later has independent Q2, Evidence structure, conclusion, and lifecycle. Expected: split into a NEW Research Object with provenance relation to parent. **PASS.**
- **T48-08 — Model Preference as False Reconciliation:** The model chooses Branch A as “more plausible” and silently discards B. Expected: FAIL / BLOCKED because model preference is not a reconciliation basis. **PASS — safety condition detected.**
- **T48-09 — Merge Confused with Verification:** Two branches agree on the same conclusion. Expected: merge/reconciliation may be recorded, but agreement creates no Verification and Claim state still depends on actual Verification. **PASS.**
- **T48-10 — D9 Interaction:** D9 integrates multiple notes while source branches contain unresolved conflicts. Expected: source conflicts/provenance remain visible; D9 Gate independent; PROMOTED does not make source Claims VERIFIED; integrated Claims retain their own Evidence/Transformation mapping. **PASS.**

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
T47 controls Research Object identity and mutation decision. T48 adds branch-aware interpretation:

**Research Object identity → Branch status → Conflict status → Reconciliation possibility → Lifecycle consequence → NO_CHANGE / REVISION / EXTENSION / NEW / BLOCKED**

Branch is not a sixth decision state; it is lifecycle structure informing the existing five decisions.

## 11. Traceability Requirements
Branch and merge operations preserve parent/branch references, branch-specific Claims, Evidence and roles, Transformations, Relations/conflicts, provenance, Verification state, Revision Events, merge/reconciliation Transformation, and SARA state.

For a merged Claim, reverse trace remains possible:

**Merged Claim ← Reconciliation/Synthesis Transformation ← Branch Claims ← Branch Evidence ← Original sources/inputs**

## 12. Safety Tests
- S1 No branch truth inflation: newer branch ≠ truer branch. **PASS.**
- S2 No conflict deletion: conflict cannot be removed only for cleaner prose. **PASS.**
- S3 No merge verification inflation: Merge ≠ Verification. **PASS.**
- S4 No consensus inflation: branch agreement ≠ proof. **PASS.**
- S5 No model-preference reconciliation. **PASS.**
- S6 Historical preservation: Merge cannot overwrite source branch history. **PASS.**
- S7 D9 independence: D9 promotion remains independent of source/merge verification. **PASS.**
- S8 New-object protection: independently answerable branch cannot be forced into the parent Research Object indefinitely. **PASS.**

## 13. Result
**T48 = PASS**

The current lifecycle model represents parallel branches, unresolved conflict, conditional/full reconciliation, merge-level synthesis, post-merge revision, and branch-to-new-object splitting without another epistemic entity.

> **Branch is lifecycle structure; Merge is a Transformation; Revision/Extension/New/Blocked are decision outcomes.**

This prevents Branch from becoming an implicit truth hierarchy or Merge from becoming implicit verification.

## 14. Validation Boundary
T48 is a controlled semantic test, not evidence of empirical performance across a large real-world corpus.

Remaining validation:
1. repeated real-conversation branch/merge cases;
2. human review of reconciliation decisions;
3. branch/merge persistence in writable Notion state;
4. larger D9 integration cases;
5. interaction with actual one-stop generation outputs.

## 15. Architecture Decision
**RETAIN CURRENT CORE MODEL.**

No new Branch entity or Merge Document Type is required beyond existing lifecycle/Transformation representation. Branch ID and Revision/Relation provenance remain lifecycle metadata/records.

## 16. Next Test
**T49 — D9 Integration / Network-Level SARA Test**

T49 should test whether D9 integration preserves source-note Claim states while independently evaluating integrated Claims and network-level verification/revision.

## 17. Boundary
This is a project-level operational test and specification, not an established academic or industry standard. The human remains the final epistemic decision authority.

---

[Korean source](t48_branch_merge_revision_interaction_test_v0.1.md)
