# T27 — Population Migration / Reproducibility Preparation v0.1

Status: PASS — PRE-MIGRATION SPECIFICATION

## 1. Objective

Prepare a population-level migration and reproducibility protocol without mutating Notion records while write capability and Query Data Source access remain unavailable.

## 2. Population selection

Use a stratified sample rather than a convenience-only sample.

Minimum strata:
- D1 exploratory
- D3 conceptual analysis
- D5 mechanism/process analysis
- D7 evaluation
- D9 integrated synthesis

Current known pilot representatives:
- RN-40: D1
- RN-41: D3
- RN-30: D5
- RN-44: D7
- RN-50: D9

These five notes form the current reproducibility anchor set. They do not establish population-level representativeness by themselves.

## 3. Migration classification

Every candidate metadata field must be classified independently:

A. DIRECT
Exact stored metadata or explicitly established canonical state. Safe for controlled population.

B. STRUCTURABLE
Explicit source content can be represented as an object, but identifier issuance and provenance registration are required. Requires review before live write.

C. INFERENTIAL
Requires model interpretation. Do not auto-populate.

## 4. Field-level migration policy

DIRECT candidates:
- existing Research Purpose
- existing Document Type
- existing note-level epistemic state
- existing evidence state
- existing SARA state
- existing D9 state where already canonical
- existing version/lineage values

STRUCTURABLE candidates:
- explicit Claim labels and states
- explicit Research Object references
- explicit relation records
- explicit revision records
- explicit transformation records with identifiable inputs/outputs/operation

INFERENTIAL by default:
- new Claim extraction from prose without explicit claim boundary
- Evidence IDs inferred only from narrative
- Transformation Events inferred only from conceptual arrows
- Branch IDs inferred from ordinary revisions
- secondary Research Purpose inferred from topical overlap
- verification status inferred from agreement or confidence language

## 5. Pre-migration snapshot

For every target note, capture before-state:
- page identifier
- title
- all relevant properties
- page body hash or equivalent stable content reference where available
- current epistemic state
- current evidence state
- current SARA state
- current D9 state
- revision/lineage metadata

The before-state is the reproducibility baseline. No migration result may overwrite it.

## 6. Post-migration verification

For each mutated field:
1. compare against manifest;
2. verify unrelated fields unchanged;
3. verify body unchanged;
4. verify epistemic state not upgraded;
5. verify D9 state not promoted;
6. verify no unsupported Claim/Evidence/Transformation object was introduced;
7. record migration outcome.

## 7. Reproducibility criteria

A migration is reproducible only if an independent rerun can reconstruct:
- why the field was populated;
- which source content justified it;
- which migration class applied;
- what value was written;
- what fields were intentionally left empty;
- whether the epistemic state changed;
- whether any revision event was created.

## 8. Failure taxonomy

MIGRATION_DATA_LOSS
MIGRATION_EPISTEMIC_INFLATION
MIGRATION_UNSUPPORTED_INFERENCE
MIGRATION_PROVENANCE_GAP
MIGRATION_ID_COLLISION
MIGRATION_BODY_MUTATION
MIGRATION_LINEAGE_BREAK
MIGRATION_STATE_DRIFT

These labels are operational test labels, not established academic terminology.

## 9. Current execution boundary

No Notion records were mutated.

Current connector limitations:
- page-property write action is unavailable;
- Query Data Source usage is currently exhausted.

Therefore T27 establishes the population protocol only.

## 10. Decision

T27 = PASS for pre-migration specification.

Live population remains blocked pending write capability.
Population-level query/reproducibility verification remains open pending Query Data Source access.

Next: T28 — population migration manifest and change-set design, without live mutation.
