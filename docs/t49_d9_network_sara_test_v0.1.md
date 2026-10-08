# T49 — D9 Integration / Network-Level SARA Test v0.1

Status: **PASS — SOURCE CLAIM STATES PRESERVED / INTEGRATED CLAIMS REQUIRE INDEPENDENT NETWORK-LEVEL SARA**

## 1. Purpose

T49 tests whether D9 Integrated Synthesis can:

1. preserve the epistemic state of source-note Claims;
2. distinguish source Claims from newly generated integrated Claims;
3. preserve source Evidence and provenance;
4. represent Relations among source Claims;
5. record the Transformation that produces an integrated structure;
6. independently evaluate integrated Claims through network-level SARA;
7. keep D9 promotion separate from epistemic Verification.

The central safety requirement is:

> **Source Claim verification does not automatically transfer to an Integrated Claim.**

## 2. D9 Semantic Boundary

D9 is an integration operation over existing Research Objects/notes.

It is not:

- a summary-only operation;
- a consensus generator;
- a verification shortcut;
- an automatic theory/model confirmation;
- a replacement for source-note verification.

A D9 result may contain:

- source Claims;
- source Evidence;
- Relations;
- conflicts;
- a Transformation-derived integrated structure;
- new integrated Claims;
- new Evidence mapping;
- independent Verification/SARA;
- D9 Gate state.

## 3. Source vs Integrated Claim

Let:

- C1 = Claim from Note A;
- C2 = Claim from Note B;
- C3 = newly generated integrated Claim.

Even if:

- C1 = VERIFIED;
- C2 = VERIFIED;

it does not follow that:

- C3 = VERIFIED.

The integrated Claim is a new proposition and requires its own:

- Claim identity;
- Evidence mapping;
- Transformation provenance;
- epistemic state;
- Verification when applicable.

Formally:

**State(C1) + State(C2) ≠ State(C3)**

The source states remain preserved.

## 4. Network-Level SARA

D9 introduces a higher-order verification problem because integration can create properties that were not present in any individual source note.

Network-level SARA therefore follows:

**Source-note states**
→ **Relation / Integration Transformation**
→ **Integrated Claim(s)**
→ **Verification**
→ **Revision**
→ **Re-verification**
→ **D9 promotion re-entry when applicable**

This does not replace source-note SARA.

It operates at a different object level.

## 5. Network-Level Verification Scope

Network-level verification may assess:

- whether source Claims were represented accurately;
- whether Relations are justified;
- whether contradictions were preserved;
- whether the integrated structure follows from inputs;
- whether new integrated Claims have adequate Evidence;
- whether boundary conditions were retained;
- whether Transformation provenance is complete.

It must not silently re-verify every source Claim simply because they are included in D9.

## 6. D9 Gate Independence

D9 Gate:

- G1 Relation
- G2 Higher-order Question
- G3 Novel Structure
- G4 Claim Decomposition
- G5 Evidence Mapping
- G6 Network-level SARA

D9 PROMOTED requires G1–G6 PASS.

However:

**D9 PROMOTED ≠ Integrated Claim VERIFIED**

and:

**D9 PROMOTED ≠ Source Claim VERIFIED**

Source verification remains governed by source-level SARA.

## 7. Controlled Fixture Set

### T49-01 — Two Verified Source Claims

Note A:
C1 = VERIFIED.

Note B:
C2 = VERIFIED.

Integration:
C3 = “A and B jointly imply mechanism M.”

Expected:

- C1 VERIFIED preserved;
- C2 VERIFIED preserved;
- C3 created separately;
- C3 not automatically VERIFIED;
- T1 = SYNTHESIZE/INTERPRET as appropriate;
- Evidence mapping for C3;
- network-level Verification required.

Result: **PASS**

### T49-02 — One Supported, One Uncertain

Note A:
C1 = SUPPORTED.

Note B:
C2 = UNCERTAIN.

Integration creates C3.

Expected:

- source states preserved;
- C3 state independently assessed;
- uncertainty in C2 not hidden;
- D9 cannot erase source uncertainty.

Result: **PASS**

### T49-03 — Contradictory Source Claims

Note A:
C1 = X increases Y.

Note B:
C2 = X decreases Y.

Integration asks:
“What explains the disagreement?”

Expected:

- conflict preserved;
- no forced consensus;
- integrated Research Object may focus on conditions/mechanisms explaining divergence;
- new Claim(s) independently assessed;
- D9 Gate independent.

Result: **PASS**

### T49-04 — Common Pattern, New Integrated Structure

Notes A/B/C each contain different pieces of a recurring pattern.

D9 identifies a higher-order structure not explicitly asserted in any source.

Expected:

- source Claims preserved;
- integrated structure represented through Transformation;
- new Claim decomposition;
- Evidence mapping;
- independent network-level SARA;
- D9 Gate evaluated separately.

Result: **PASS**

### T49-05 — Source Claim Scope Conflict

Note A:
C1 applies under condition A.

Note B:
C2 appears inconsistent but applies under condition B.

Expected:

- boundary conditions preserved;
- no false contradiction;
- integrated structure may express conditional relation;
- new integrated Claim independently evaluated.

Result: **PASS**

### T49-06 — D9 Revision

Existing D9:
C3 is SUPPORTED.

New source Evidence E4 undermines the relation used by C3.

Expected:

- original D9 state preserved;
- affected Transformation/Relation identified;
- Revision Event created;
- C3 re-evaluated;
- new/changed integrated Claim as necessary;
- network-level SARA;
- D9 Gate re-entry if affected.

Result: **PASS**

### T49-07 — Source Revision After D9

Source Note A changes from SUPPORTED to CONTRADICTED after new evidence.

Existing D9 depends on C1.

Expected:

- source-level SARA remains authoritative for C1;
- D9 dependency is identified;
- D9 is not silently rewritten;
- affected integrated Claims enter network-level revision/re-verification;
- D9 promotion is re-evaluated if applicable.

Result: **PASS**

### T49-08 — D9 Promotion with Unverified Integrated Claim

All G1–G6 are satisfied according to the D9 Gate criteria, but an integrated Claim remains epistemically UNCERTAIN because evidence is limited.

Expected:

- D9 may be PROMOTED as an integrated research structure;
- integrated Claim remains UNCERTAIN;
- PROMOTED does not upgrade Claim state.

Result: **PASS**

This fixture explicitly confirms that D9 promotion and Claim verification are orthogonal.

### T49-09 — Source Note Summary Only

D9 merely repeats source-note conclusions without creating a new integrated structure.

Expected:

- D9 Gate should not be artificially passed;
- classify as summary/synthesis only as appropriate;
- no fabricated “novel structure”;
- no promotion inflation.

Result: **PASS**

### T49-10 — Source Evidence Misrepresented

D9 rendering attributes a source Claim to evidence that does not support it.

Expected:
network-level verification detects provenance/evidence-mapping failure.

Result:
**FAIL condition detected — D9 must not be promoted until corrected.**

Fixture result: **PASS — safety condition detected.**

## 8. D9 Dependency Graph

The minimal D9 trace should support:

**Source Note**
→ **Source Claim**
→ **Source Evidence**
→ **Relation**
→ **Integration Transformation**
→ **Integrated Claim**
→ **Integrated Evidence**
→ **Network-level Verification/SARA**
→ **D9 Gate**

Not every D9 requires every node, but material dependencies must remain traceable.

## 9. Source-State Preservation Rule

D9 rendering may quote, summarize, compare, or transform source Claims.

It must never:

- rewrite the source Claim's epistemic state without recording a source revision;
- collapse contradictory states into one “consensus” state;
- transfer VERIFIED from source to integrated Claim;
- transfer PROMOTED from D9 to source Claim;
- treat inclusion as verification.

## 10. Integrated Claim State Rule

Every newly generated integrated Claim receives its own epistemic state.

Candidate states include:

- HYPOTHESIS
- INTERPRETATION
- UNCERTAIN
- SUPPORTED
- PARTIALLY_SUPPORTED
- CONTRADICTED
- VERIFIED

The appropriate state depends on its own Evidence/Verification.

Generation alone produces no automatic upgrade.

## 11. Network-Level SARA Invariants

### N1 — Source SARA preservation

Source-note SARA remains independently queryable.

PASS.

### N2 — Integrated SARA independence

Integrated Claims require their own Verification path.

PASS.

### N3 — Dependency propagation

A material source revision triggers identification/re-evaluation of dependent D9 Claims.

PASS.

### N4 — No automatic invalidation of unrelated D9 Claims

Only materially dependent integrated structures enter re-verification.

PASS.

### N5 — Historical preservation

Previous D9 states remain queryable.

PASS.

### N6 — Promotion re-entry

If affected by revision, D9 Gate re-entry occurs where required.

PASS.

### N7 — No promotion/verification conflation

PROMOTED remains distinct from VERIFIED.

PASS.

## 12. D9 Failure Conditions

### F1 — Verification inheritance

Integrated Claim inherits VERIFIED from source Claims.

FAIL.

### F2 — Consensus erasure

Conflicting source Claims are collapsed into one “consensus” statement without analysis.

FAIL.

### F3 — Evidence laundering

Source Evidence is presented as direct Evidence for a new integrated Claim without transformation/mapping.

FAIL.

### F4 — Transformation disappearance

Integrated Claim has no derivation trace.

FAIL.

### F5 — Dependency blindness

Source revision does not trigger review of dependent D9 Claims.

FAIL.

### F6 — Promotion inflation

D9 PROMOTED is treated as Claim VERIFIED.

FAIL.

### F7 — Summary inflation

Simple summary is treated as a novel D9 structure.

FAIL.

## 13. Interaction with T48

T48 establishes:

**Branch / Conflict / Merge**
→ lifecycle and Transformation semantics.

T49 adds:

**D9 Integration**
→ network-level Relations / Transformation / SARA.

Therefore a D9 integration over branches must preserve branch provenance and conflict state before generating any integrated Claim.

## 14. Result

**T49 = PASS**

The controlled fixtures establish that the existing model can represent:

- source-note Claims with independent epistemic states;
- integrated Claims with independent states;
- source-to-integrated provenance;
- network-level Transformation;
- dependency-aware re-verification;
- D9 promotion independent from Verification;
- D9 revision after source-note change;
- unresolved conflicts without forced consensus.

No additional epistemic entity is required.

## 15. Architecture Decision

**RETAIN CURRENT CORE MODEL.**

Network-level SARA is a lifecycle/application of existing Verification, Revision, Transformation, Relation, and D9 Gate objects.

No new “Network Verification” entity is justified.

## 16. Validation Boundary

T49 is a controlled semantic test, not empirical evaluation over a large corpus.

Remaining validation:

1. real multi-note D9 generation;
2. larger dependency graphs;
3. repeated D9 revision scenarios;
4. human review of integrated Claim decomposition;
5. live persistence of D9 dependency/trace references;
6. empirical assessment of false verification inheritance.

## 17. Next Test

**T50 — End-to-End Research Note Engine Regression Test**

T50 should run the complete chain:

Conversation
→ Research Object
→ Classification
→ Template
→ Claim/Evidence
→ Transformation
→ SARA
→ Revision/Branch/Merge
→ D9
→ One-Stop Decision
→ Notion Persistence Boundary

The purpose is regression closure across all major semantic and operational invariants established through T1–T49.

## 18. Boundary

This is a project-level operational test and specification. It is not an established academic or industry standard.

Human remains final epistemic decision authority.
