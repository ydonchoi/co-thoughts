# Research Note Generation Engine v0.3 (가칭)

Status: HISTORICAL / SUPERSEDED

## Additions
- Primary Purpose maximum 1; Secondary Purpose 0+.
- Secondary purpose becomes a separate Research Object when it has an independent question, evidence structure, and conclusion.
- Interpretation provenance:
  AUTHOR_CLAIM
  SCHOLARLY_INTERPRETATION
  PROJECT_INTERPRETATION
  MODEL_PROPOSAL
- D8 remains one document type; Review Type is metadata.
- Taxonomy Provenance ledger expanded.
- Axis Audit introduced.
- Evidence-driven reclassification explicitly allowed.
- Network-level re-verification added.

## Stress-Test Findings
T4: provenance gate must be conditional for empirical research.
T5: measurement→data→analysis→result→evidence→claim provenance is required.
T6: study evidence and synthesis evidence must remain distinct.
T7: model output and observation must remain distinct.
T8: adversarial transformation failures require traceability.
T9: end-to-end integrity passed.
T10: minimum traceability schema passed.

## Transition to v0.4
T11 lifecycle mutation, T12 branch/merge, and T13 architecture audit established the need for explicit Version/Revision/Branch semantics and a cross-cutting Transformation Event layer.
