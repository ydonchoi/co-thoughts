# T26 — Query Workload Decision Gate v0.1

Status: GATE DEFINED / EXECUTION DEFERRED

## 1. Purpose

Freeze the decision procedure for determining whether the collapsed Notion representation is sufficient, without introducing schema expansion merely because query access is temporarily unavailable.

## 2. Inputs

- T16 query usability test
- T24 Notion representation mapping
- T25 minimal schema correction test
- Research Note Engine v0.4 baseline

## 3. Decision matrix

### Gate A — Q2-Q5 all pass
Decision: RETAIN COLLAPSED REPRESENTATION.

Action:
- keep current single Research Note data source;
- apply only confirmed minimal semantic corrections;
- proceed to broader metadata migration/reproducibility.

### Gate B — one or more queries fail because of representation limitations
Decision: MINIMAL SCHEMA EXTENSION.

Action:
- identify the exact failed workload;
- add only the smallest structured field/object needed;
- rerun the failed query and regression tests;
- do not introduce a full normalized graph automatically.

### Gate C — queries fail only because of connector/entitlement limits
Decision: NO ARCHITECTURE CHANGE.

Action:
- retain the current schema decision;
- mark operational verification as blocked;
- resume when query access is available.

## 4. Current classification

T25 establishes that the present blocker is Gate C: Query Data Source usage limit.

No evidence currently demonstrates that the collapsed representation is semantically or operationally insufficient.

Therefore no Claim/Evidence/Transformation data sources are justified at this stage.

## 5. D9 correction gate

The canonical semantic state remains:
- NOT_APPLICABLE
- CANDIDATE
- PROMOTED

The current Notion HOLD option is stale/operational and must not be treated as a canonical promotion state.

This is a schema correction issue, but mutation is deferred until write capability exists.

## 6. Required future execution

When Query Data Source access is available, execute:
- Q2 D9 candidate + revision-required
- Q3 traceability completeness
- Q4 lifecycle lineage
- Q5 taxonomy consistency
- Q6 claim-state separation

Record actual returned rows/results. Do not infer results from schema inspection.

## 7. Closure rule

Implementation closure requires:
1. semantic baseline PASS;
2. sample migration/reproducibility PASS;
3. Q2-Q5 executed;
4. collapsed-vs-extended representation decision supported by query evidence;
5. broader population reproducibility completed.

Until these conditions are met, implementation status remains CONDITIONAL.

## 8. Safety invariants

- Query unavailable ≠ query failed.
- Schema expressiveness ≠ operational query success.
- Missing query result ≠ evidence of schema insufficiency.
- No schema expansion without demonstrated workload need.
- No D9 promotion from candidate state.
- No epistemic upgrade from metadata migration.

Next: T27 — broader population migration/reproducibility preparation, while T26 Q2-Q6 remains pending until query access is restored.
