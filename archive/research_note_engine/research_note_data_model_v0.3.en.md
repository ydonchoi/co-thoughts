# Research Note Data Model v0.3 (provisional project term)

Status: HISTORICAL / RECONSTRUCTED / SUPERSEDED

> Reconstructed from recorded project architecture decisions; not a byte-for-byte historical snapshot.

## Main Changes
v0.3 introduced stronger provenance and traceability requirements following stress testing.

## Added / Formalized Layers
- Interpretation provenance: AUTHOR_CLAIM, SCHOLARLY_INTERPRETATION, PROJECT_INTERPRETATION, MODEL_PROPOSAL
- Measurement-to-Claim provenance control (provisional project term)
- Synthesis-to-Claim provenance control (provisional project term)
- Model-to-Claim provenance control (provisional project term)
- Claim Transformation Traceability (provisional project term) as an emerging cross-cutting concern
- lifecycle mutation and revision-preservation requirements
- D9 gate state distinct from epistemic truth state

## Provenance Chain
Source/Text/Data/Observation → Transformation/Analysis/Synthesis → Evidence → Claim → Verification → Epistemic State

The model explicitly rejected these equivalences:
- Source ≠ Evidence
- Evidence ≠ Verification
- Transformation ≠ Evidence
- Transformation ≠ Claim
- Claim ≠ Epistemic State
- Agreement ≠ Evidence

## Stress-Test Implication
A Research Note was treated as a representation layer, while Claims, Evidence, Transformations, Verification, Relations, and classification remained separable objects.

## Supersession
Superseded by v0.4, which formalized Transformation Event, Version/Revision, Branch, Provenance, and D9 Gate in the logical model.

---

[Korean source](research_note_data_model_v0.3.md)
