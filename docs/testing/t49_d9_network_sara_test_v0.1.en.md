# T49 — D9 Integration / Network-Level SARA Test v0.1

Status: **PASS — SOURCE CLAIM STATES PRESERVED / INTEGRATED CLAIMS REQUIRE INDEPENDENT NETWORK-LEVEL SARA**

## 1. Purpose
T49 tests whether D9 Integrated Synthesis can preserve source-note Claim states, distinguish source Claims from newly generated integrated Claims, preserve source Evidence/provenance, represent Relations, record the Transformation producing an integrated structure, independently evaluate integrated Claims through network-level SARA, and keep D9 promotion separate from epistemic Verification.

Core safety requirement:

> **Source Claim verification does not automatically transfer to an Integrated Claim.**

## 2. D9 Semantic Boundary
D9 integrates existing Research Objects/notes. It is not a summary-only operation, consensus generator, verification shortcut, automatic theory/model confirmation, or replacement for source-note verification.

A D9 result may contain source Claims, source Evidence, Relations, conflicts, a Transformation-derived structure, new integrated Claims, new Evidence mapping, independent Verification/SARA, and D9 Gate state.

## 3. Source vs Integrated Claim
Let C1 be a Claim from Note A, C2 a Claim from Note B, and C3 a new integrated Claim. Even if C1 and C2 are VERIFIED, C3 does not automatically become VERIFIED.

The integrated Claim is a new proposition and needs its own Claim identity, Evidence mapping, Transformation provenance, epistemic state, and Verification when applicable.

**State(C1) + State(C2) ≠ State(C3)**

Source states remain preserved.

## 4. Network-Level SARA
Integration can create properties not present in individual source notes. Network-level SARA therefore follows:

**Source-note states → Relation / Integration Transformation → Integrated Claim(s) → Verification → Revision → Re-verification → D9 promotion re-entry where applicable**

This does not replace source-note SARA; it operates at a different object level.

## 5. Network-Level Verification Scope
Network verification may assess whether source Claims were represented accurately, Relations are justified, contradictions preserved, the integrated structure follows from inputs, new Claims have adequate Evidence, boundary conditions were retained, and Transformation provenance is complete.

It must not silently re-verify every source Claim merely because the Claims are included in D9.

## 6. D9 Gate Independence
D9 Gate consists of G1 Relation, G2 Higher-order Question, G3 Novel Structure, G4 Claim Decomposition, G5 Evidence Mapping, and G6 Network-level SARA.

D9 PROMOTED requires G1–G6 PASS. However:
- **D9 PROMOTED ≠ Integrated Claim VERIFIED**
- **D9 PROMOTED ≠ Source Claim VERIFIED**

Source verification remains governed by source-level SARA.

## 7. Controlled Fixture Set
- **T49-01 — Two Verified Source Claims:** C1 and C2 are VERIFIED; new C3 states that A and B jointly imply mechanism M. Preserve source states, create C3 separately, do not auto-verify C3, map a SYNTHESIZE/INTERPRET Transformation and Evidence, and require network Verification. **PASS**
- **T49-02 — One Supported, One Uncertain:** Preserve C1 SUPPORTED and C2 UNCERTAIN; independently assess C3 and do not hide C2 uncertainty. **PASS**
- **T49-03 — Contradictory Source Claims:** One source says X increases Y; another says X decreases Y. Preserve conflict, do not force consensus, and independently assess any explanatory Claims. **PASS**
- **T49-04 — Common Pattern, New Structure:** Different notes contain parts of a recurring pattern; D9 proposes a higher-order structure. Preserve source Claims, record Transformation, decompose new Claims, map Evidence, apply network SARA, and separately evaluate D9 Gate. **PASS**
- **T49-05 — Source Claim Scope Conflict:** C1 applies under A and C2 appears inconsistent under B. Preserve boundary conditions and independently assess any conditional integrated Claim. **PASS**
- **T49-06 — D9 Revision:** New E4 undermines a Relation used by supported C3. Preserve original D9 state, identify affected Transformation/Relation, record Revision Event, re-evaluate C3, and re-enter network SARA/D9 Gate as needed. **PASS**
- **T49-07 — Source Revision After D9:** Source A changes from SUPPORTED to CONTRADICTED after new Evidence. Source-level SARA remains authoritative; identify dependent D9 Claims, do not silently rewrite them, revise/re-verify affected Claims, and re-evaluate promotion where relevant. **PASS**
- **T49-08 — D9 Promotion with Unverified Integrated Claim:** All Gate conditions pass while an integrated Claim remains UNCERTAIN. D9 may be PROMOTED as an integrated structure while the Claim remains UNCERTAIN. **PASS**
- **T49-09 — Source Note Summary Only:** D9 merely repeats source conclusions. Do not artificially pass the Gate or invent a novel structure. **PASS**
- **T49-10 — Source Evidence Misrepresented:** D9 attributes a source Claim to Evidence that does not support it. Network Verification detects the mapping failure; D9 must not be promoted until corrected. **PASS — safety condition detected**

## 8. D9 Dependency Graph
Minimum trace:

**Source Note → Source Claim → Source Evidence → Relation → Integration Transformation → Integrated Claim → Integrated Evidence → Network-level Verification/SARA → D9 Gate**

Not every D9 needs every node, but material dependencies must remain traceable.

## 9. Source-State Preservation Rule
D9 may quote, summarize, compare, or transform source Claims. It must never rewrite a source Claim's epistemic state without a source revision, collapse contradictions into consensus, transfer VERIFIED from a source to integrated Claim, transfer D9 PROMOTED to a source Claim, or treat inclusion as verification.

## 10. Integrated Claim State Rule
Every newly generated integrated Claim receives its own epistemic state. Candidate states include HYPOTHESIS, INTERPRETATION, UNCERTAIN, SUPPORTED, PARTIALLY_SUPPORTED, CONTRADICTED, and VERIFIED. The appropriate state depends on its own Evidence/Verification. Generation alone causes no automatic upgrade.

## 11. Network-Level SARA Invariants
- **N1 — Source SARA preservation:** source-note SARA remains independently queryable. PASS.
- **N2 — Integrated SARA independence:** integrated Claims require their own Verification path. PASS.
- **N3 — Dependency propagation:** material source revision triggers identification/re-evaluation of dependent D9 Claims. PASS.
- **N4 — No automatic invalidation of unrelated D9 Claims:** only materially dependent structures enter re-verification. PASS.
- **N5 — Historical preservation:** previous D9 states remain queryable. PASS.
- **N6 — Promotion re-entry:** affected D9 Gate re-entry occurs where needed. PASS.
- **N7 — No promotion/verification conflation:** PROMOTED remains distinct from VERIFIED. PASS.

## 12. D9 Failure Conditions
- **F1 — Verification inheritance:** integrated Claim inherits VERIFIED from source Claims. FAIL.
- **F2 — Consensus erasure:** conflicting Claims collapsed into consensus without analysis. FAIL.
- **F3 — Evidence laundering:** source Evidence presented as direct Evidence for a new integrated Claim without transformation/mapping. FAIL.
- **F4 — Transformation disappearance:** integrated Claim has no derivation trace. FAIL.
- **F5 — Dependency blindness:** source revision does not trigger review of dependent D9 Claims. FAIL.
- **F6 — Promotion inflation:** D9 PROMOTED treated as Claim VERIFIED. FAIL.
- **F7 — Summary inflation:** simple summary treated as a novel D9 structure. FAIL.

## 13. Interaction with T48
T48 establishes Branch / Conflict / Merge lifecycle and Transformation semantics. T49 adds D9 integration with network-level Relations / Transformation / SARA. D9 integration over branches must preserve branch provenance and conflict state before generating an integrated Claim.

## 14. Result
**T49 = PASS**

The controlled fixtures show that the model can represent independently rated source and integrated Claims, source-to-integrated provenance, network-level Transformation, dependency-aware re-verification, D9 promotion independent of Verification, revision after source-note change, and unresolved conflicts without forced consensus.

No additional epistemic entity is required.

## 15. Architecture Decision
**RETAIN CURRENT CORE MODEL.**

Network-level SARA is an application of existing Verification, Revision, Transformation, Relation, and D9 Gate objects. No separate “Network Verification” entity is justified.

## 16. Validation Boundary
T49 is a controlled semantic test, not a large-corpus empirical evaluation.

Remaining validation:
1. real multi-note D9 generation;
2. larger dependency graphs;
3. repeated D9 revision scenarios;
4. human review of integrated Claim decomposition;
5. live persistence of D9 dependency/trace references;
6. empirical assessment of false verification inheritance.

## 17. Next Test
**T50 — End-to-End Research Note Engine Regression Test**

T50 should run the complete chain: Conversation → Research Object → Classification → Template → Claim/Evidence → Transformation → SARA → Revision/Branch/Merge → D9 → One-Stop Decision → Notion Persistence Boundary.

## 18. Boundary
This is a project-level operational test and specification, not an established academic or industry standard. The human remains the final epistemic decision authority.

---

[Korean source](t49_d9_network_sara_test_v0.1.md)
