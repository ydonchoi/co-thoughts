# T28 — Population Migration Manifest / Change-set Design v0.1

Status: PASS — CHANGE-SET READY / NO LIVE MUTATION

## 1. Scope

Define the exact field-level change set for the five reproducibility anchor notes. This document is an execution manifest, not evidence that migration occurred.

## 2. Global rule

Only DIRECT fields enter the live write set automatically.
STRUCTURABLE fields remain review-gated.
INFERENTIAL fields remain excluded.

## 3. Change-set matrix

| Note | Direct write candidates | Structurable review | Excluded |
|---|---|---|---|
| RN-40 | preserve D1, R1, HYPOTHESIS, UNMAPPED, SARA revision-required; D9 NOT_APPLICABLE | none currently safe | Claim ID, RO ID, Evidence Mapping, Transformation Trace, Branch ID, Revision Type, Secondary Purpose |
| RN-41 | preserve D3, R1, INTERPRETATION, UNMAPPED, SARA not-yet-verified; D9 NOT_APPLICABLE | none currently safe | Claim ID, RO ID, Evidence Mapping, Transformation Trace, Branch ID, Revision Type, Secondary Purpose |
| RN-30 | preserve D5, R3, HYPOTHESIS, partial mapping, SARA revision-required; D9 NOT_APPLICABLE | explicit claims/relations only after object identification | new Claim/Evidence/Transformation IDs, Branch ID, Revision Type, Secondary Purpose |
| RN-44 | preserve D7, R5, SUPPORTED, core evidence, SARA verified; D9 NOT_APPLICABLE | evidence objects may be registered after source/provenance identification | inferred Claim IDs, inferred Evidence IDs, inferred Transformation Trace, Branch ID, Secondary Purpose |
| RN-50 | preserve D9, R3, HYPOTHESIS, partial mapping, SARA revision-required; D9 CANDIDATE | C1-C5/IC1, explicit relations, candidate synthesis transformation | inferred Evidence IDs, unsupported Transformation Events, Branch ID unless explicit, Secondary Purpose |

## 4. Important interpretation

The 'direct write candidates' above are principally a preservation/validation set. If the current Notion property already contains the correct value, the migration should perform no write for that field.

A migration write is justified only when:
1. the manifest specifies the exact target value;
2. the current value is absent or demonstrably stale;
3. the source basis is explicit;
4. the write will not overwrite unrelated content.

## 5. D9 handling

Canonical state:
- RN-40: NOT_APPLICABLE
- RN-41: NOT_APPLICABLE
- RN-30: NOT_APPLICABLE
- RN-44: NOT_APPLICABLE
- RN-50: CANDIDATE

However, current Notion schema lacks NOT_APPLICABLE and still contains HOLD. Therefore these values are change targets only after schema/write capability is available.

HOLD must not be used as a substitute for NOT_APPLICABLE.

## 6. RN-50 structured review set

Candidate objects already explicitly named in the source body:
- C1, C2, C3, C4, C5, IC1

Candidate relation:
- RN-50 SYNTHESIZES RN-15 / RN-16 / RN-30

Candidate transformation:
- Input: RN-15 / RN-16 / RN-30 claim/evidence structures
- Operation: SYNTHESIZE
- Output: integrated mechanism structure
- Target: IC1 and related synthesis claims
- Validation: PARTIAL; G5-G6 remain incomplete

These remain STRUCTURABLE candidates, not automatically writable metadata.

## 7. Pre-write validation checklist

Before any live mutation:
- confirm exact page identity;
- capture before-state;
- verify target property type;
- verify target option exists;
- verify manifest version;
- verify no concurrent revision has changed the page;
- verify body preservation strategy;
- verify D9 state semantics.

## 8. Post-write verification

For each write:
- fetch page again;
- compare mutated field with manifest;
- compare all unrelated fields against before-state;
- confirm body unchanged;
- confirm epistemic state unchanged unless explicitly approved by a separate verification record;
- confirm D9 not promoted;
- record outcome and timestamp.

## 9. Current execution boundary

No Notion records were mutated.

Live execution is blocked because page-property write capability is unavailable and the D9 schema still requires correction before NOT_APPLICABLE can be represented cleanly.

## 10. Decision

T28 = PASS for change-set design.

The five-note population now has an explicit, field-level migration boundary and a reproducible pre/post verification protocol.

Next: T29 — migration simulation / dry-run diff generation against the anchor set, without live mutation.
