# T17 — Reproducibility Test v0.1

Status: PASS (sample-level)

## Baseline
Research Note Engine v0.4 — Baseline Consolidation.

## Method
Independently re-apply the current v0.4 classification, evidence, transformation, SARA, and D9 rules to stored source pages without treating existing metadata as authoritative evidence. Compare reconstructed outputs with stored state.

## Sample A — RN-40
Reconstructed: R1 / D1 / HYPOTHESIS / evidence UNMAPPED / SARA revision required / D9 NOT_APPLICABLE.  
Stored: R1 / D1 / HYPOTHESIS / evidence UNMAPPED / SARA revision required / D9 NOT_APPLICABLE.  
Match: PASS.

## Sample B — RN-50
Reconstructed: R3 / D9 / HYPOTHESIS; G1 PASS, G2 PASS, G3 PASS, G4 PASS, G5 PARTIAL, G6 PARTIAL PASS / REVISION REQUIRED; D9 state CANDIDATE; D9 PROMOTED withheld.  
Stored: same classification, epistemic state, gate results, revision loop, and promotion decision.  
Match: PASS.

## Reproducibility Invariants
- Current metadata is not treated as evidence for reconstruction.
- Missing evidence is not invented.
- Existing verification is not upgraded by reproduction.
- D9 promotion requires G1–G6 PASS.
- Historical/revision state is preserved.

## Conclusion
PASS for sample-level reproducibility. Full population-level reproducibility is not yet established; broader sampling and the blocked T16 query set remain future work.

---

[Korean source](t17_reproducibility_test_v0.1.md)
