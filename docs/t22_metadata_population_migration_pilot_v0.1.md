# T22 — Metadata Population / Migration Pilot v0.1

Status: PASS for migration-boundary definition; no Notion records mutated.

## 1. Objective
Determine which canonical metadata can be populated from explicit stored content without introducing new epistemic claims or silently changing existing state.

## 2. Non-inference rule
Populate only when the source page explicitly supplies the value or an existing canonical record already establishes it.
Do not derive a new Claim, Evidence, Transformation Event, Revision Type, Branch, or Research Object merely because prose suggests one.

## 3. Pilot samples

### RN-40 — D1 exploratory
Safe population:
- D9 = NOT_APPLICABLE
- Note epistemic state = HYPOTHESIS
- Existing Research Purpose = R1
- Existing Document Type = D1

Do not auto-populate:
- Claim ID
- Research Object ID
- Evidence Mapping
- Transformation Trace
- Branch ID
- Revision Type
Reason: page explicitly identifies hypotheses and observations, but no canonical Claim/Event identifiers exist.

### RN-44 — D7 evaluation
Safe population:
- D9 = NOT_APPLICABLE
- Note epistemic state = SUPPORTED
- Existing Research Purpose = R5
- Existing Document Type = D7
- SARA = verified

Do not auto-populate Claim/Evidence/Transformation identifiers solely from the narrative. The page contains explicit evidence descriptions, but mapping them into canonical Evidence objects requires object-level identification and provenance references not currently encoded.

### RN-50 — D9 candidate
Safe population:
- D9 = CANDIDATE
- Note epistemic state = HYPOTHESIS
- Existing Research Purpose = R3
- Existing Document Type = D9
- G1-G4 = PASS
- G5 = PARTIAL
- G6 = PARTIAL PASS / REVISION REQUIRED

Potential structured population, but only with explicit provenance:
- C1-C6 / IC1 are already explicitly named in the body.
- Their individual epistemic states are explicitly stated.
- Existing source/evidence descriptions can be linked only if the underlying Evidence objects and source references are separately identifiable.
- Transformation Events should not be invented from arrows in the prose unless the input/output objects and operation are explicit.

## 4. Boundary result

Three migration classes:

A. DIRECT — exact existing metadata or explicitly stated canonical state.
B. STRUCTURABLE — explicit body content can be mapped to an object only after assigning an identifier and preserving provenance.
C. INFERENTIAL — requires model interpretation and must not be auto-populated.

RN-50 contains the strongest STRUCTURABLE material.
RN-40 contains mainly INFERENTIAL material for the new traceability layer.
RN-44 contains evidence-rich prose but still requires object-level provenance mapping.

## 5. Migration safety invariants
- Existing body is not rewritten.
- Existing epistemic state is not upgraded.
- Missing evidence is not invented.
- Claim creation does not imply verification.
- Evidence mapping does not imply support strength.
- Transformation Event does not imply truth.
- D9 CANDIDATE does not become PROMOTED.
- Revision history is preserved.
- Human remains final epistemic authority.

## 6. Decision
T22 = PASS for migration-boundary specification / DRY-RUN.

No Notion mutation was performed because the available Notion connection exposes fetch/search but not page-property update capability. Therefore this test does not claim successful live metadata migration.

Next: T23 — controlled live population of the safest DIRECT fields if write capability is available; otherwise maintain the dry-run artifact and prepare an explicit migration manifest.
