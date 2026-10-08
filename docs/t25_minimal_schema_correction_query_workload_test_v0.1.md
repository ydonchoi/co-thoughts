# T25 — Minimal Schema Correction / Query Workload Test v0.1

Status: CONDITIONAL / QUERY EXECUTION BLOCKED

## 1. Objective

Determine whether the current collapsed Notion representation is sufficient for the intended Research Note workload before introducing separate Claim/Evidence/Transformation data sources.

## 2. Current schema decision

Do not introduce separate data sources at this stage.

Rationale:
- v0.4 permits collapsed implementation when semantics and provenance remain explicit.
- Current schema already contains Research Object ID, Claim ID, Evidence Mapping, Transformation Trace, Revision Type, Branch ID and related metadata.
- Introducing additional data sources before workload evidence would be premature normalization.

## 3. Minimum correction path

### Correction A — D9 applicability/state

Canonical semantic vocabulary from T19:
- NOT_APPLICABLE
- CANDIDATE
- PROMOTED

Current Notion select:
- HOLD
- CANDIDATE
- PROMOTED

Required implementation correction:
- add NOT_APPLICABLE;
- retain HOLD only if explicitly marked as legacy/operational, or remove it when write capability is available;
- never reinterpret HOLD as the canonical D9 state.

No mutation performed.

### Correction B — Claim-level state

Do not add a separate Claim-state property to the Research Note database yet.

Instead:
- Claim ID remains the object reference;
- Claim text and Claim-level epistemic state remain in the Claim representation/body;
- note-level 인식론적 상태 continues to represent the central Research Note proposition/integrated thesis only.

Promote to a separate Claim data source only if required queries cannot be executed reliably with the collapsed representation.

### Correction C — Evidence / Transformation / Relation

Retain current text-based fields provisionally:
- Evidence Mapping
- Transformation Trace
- 연구노트 관계
- 관련 연구노트

Do not treat their presence as proof of structured graph queryability.

Separate data sources become justified only when the required query workload demonstrates that text representation is operationally insufficient.

## 4. Required query workload

Q2 — D9 candidate + revision-required state
Expected semantic target: D9 = CANDIDATE and G6 = PARTIAL PASS / REVISION REQUIRED.

Q3 — traceability completeness
Find notes with Claim ID present, Evidence Mapping present, Transformation Trace present, and identify partial/missing combinations.

Q4 — lifecycle lineage
Find notes with Revision Type and/or Branch ID and Previous Research Note, and reconstruct non-destructive lineage.

Q5 — taxonomy consistency
Find notes where Research Purpose and Document Type are inconsistent with the adopted mapping.

Q6 — claim-state separation
Demonstrate that note-level epistemic state can differ from individual Claim states without semantic collision.

## 5. Execution result

Q2-Q5 could not be executed because Notion Query Data Source usage limit was reached.

The attempted query had no side effects and was not executed.

Therefore:
- Query expressiveness: schema-level PASS
- Query execution: NOT VERIFIED
- Collapsed representation sufficiency: NOT VERIFIED
- Need for separate data sources: NOT ESTABLISHED

## 6. Decision

T25 = CONDITIONAL.

No schema expansion is justified yet.

The correct next step is to resume Q2-Q5 when Query Data Source access becomes available, then decide between:

Path A — retain collapsed representation, if workload passes.

Path B — introduce minimal dedicated Claim/Evidence/Transformation structures, only for demonstrated workload failures.

## 7. Safety constraints

- No schema mutation.
- No reinterpretation of HOLD as canonical.
- No Claim/Evidence object fabrication.
- No inference from unavailable query results.
- No D9 promotion.
- Preserve existing v0.4 semantics.

Next: T26 — workload execution and decision gate when Notion Query Data Source becomes available.
