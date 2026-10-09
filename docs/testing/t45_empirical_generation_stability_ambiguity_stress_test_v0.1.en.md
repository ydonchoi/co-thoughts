# T45 — Empirical Generation Stability / Ambiguity Stress Test v0.1

Status: **CONDITIONAL PASS — TEST HARNESS SPECIFIED / LIVE REPEATED-GENERATION EXECUTION NOT AVAILABLE IN CURRENT TOOLING**

## 1. Purpose

T45 operationalizes the T44 semantic-stability contract against realistic conversational inputs.

The objective is to determine whether repeated generation preserves research structure while allowing legitimate linguistic variation.

T45 tests:
- Document Type agreement;
- Primary Research Purpose agreement;
- section-rendering agreement;
- Claim/Evidence stability;
- epistemic-state stability;
- provenance preservation;
- Transformation Trace stability;
- ambiguity handling;
- human-review agreement.

## 2. Important Execution Boundary

The current environment does not expose an isolated repeated-generation harness that can execute the same prompt multiple times while independently capturing runs and freezing all model/context variables.

Therefore T45 does **not** claim an empirical pass for actual repeated LLM generations. The current result is a **test-harness and fixture readiness assessment**. Future live execution must be recorded separately.

## 3. Test Population

| ID | Input class | Primary target |
|---|---|---|
| T45-01 | Clear D1 | Exploratory classification |
| T45-02 | Clear D2 | Descriptive classification |
| T45-03 | Clear D3 | Concept analysis |
| T45-04 | Clear D4 | Relation/causality |
| T45-05 | Clear D5 | Mechanism/process |
| T45-06 | Clear D6 | Prediction |
| T45-07 | Clear D7 | Evaluation |
| T45-08 | Clear D8 | Literature synthesis |
| T45-09 | Clear D9 | Higher-order integration |
| T45-10 | D4/D5 ambiguity | Relation versus mechanism |
| T45-11 | D6/D7 ambiguity | Prediction versus evaluation |
| T45-12 | D8/D9 ambiguity | Literature synthesis versus integration |
| T45-13 | Missing Evidence | Missing-state stability |
| T45-14 | Contradictory Evidence | Conflict preservation |
| T45-15 | Revision request | Revision versus extension |
| T45-16 | Derived synthesis | Transformation Trace stability |

## 4. Controlled Input Fixtures

### T45-01 — Exploration
“Let’s organize a repeatedly observed recent phenomenon and explore possible patterns. We do not yet know which explanation is correct.”

Expected: D1 / R1; pattern section conditional; hypotheses provisional.

### T45-04 — Relation / Causality
“We observed X and Y increasing together. Examine whether this is an actual impact relationship or whether other explanations are possible.”

Expected: D4; association distinct from causality; alternatives/counter-evidence conditional.

### T45-05 — Mechanism
“Explain why this result occurs in terms of components and processes, and compare possible mechanisms.”

Expected: D5; mechanism provisional unless supported; no fabricated mediation/moderation.

### T45-06 — Prediction
“Assuming current conditions continue, examine likely future changes alongside alternative scenarios.”

Expected: D6; horizon/conditions/uncertainty; prediction ≠ fact.

### T45-07 — Evaluation
“Evaluate whether this policy was effective and examine evaluation criteria and possible improvements.”

Expected: D7; criteria supplied, justified, or escalated; no invented normative criteria.

### T45-08 — Literature Synthesis
“Compare the key claims and evidence in related studies and synthesize agreement and debate.”

Expected: D8 when the actual task is literature review/synthesis; no fabricated search/selection; disagreement preserved.

### T45-09 — Higher-order Integration
“Compare the central claims of three existing research notes, analyze their relations, and examine whether an integrated structure explains something the existing notes do not.”

Expected: D9; source-note mapping; integrated structure remains a candidate; D9 Gate independent.

## 5. Ambiguity Fixtures

### T45-10 — D4/D5
“Determine whether AI use affects research outcomes and, if so, through what process.”

Expected: primary classification follows the normalized principal question; secondary purpose/modules allowed; independent questions may split Research Objects; no silent causal/mechanistic inflation.

### T45-11 — D6/D7
“Assess whether this policy will continue to be effective in the future.”

Expected: distinguish future prediction from evaluation; if evaluation is intended but criteria are absent, ESCALATE.

### T45-12 — D8/D9
“Synthesize several studies to create a new explanation.”

Expected: D8 when literature evidence synthesis is primary; D9 when existing research-note structures are integrated; do not infer D9 PROMOTED.

## 6. Adversarial Fixtures

### T45-13 — Missing Evidence
The prompt requires a conclusion but supplies no supporting source or observation.

Expected: required section remains visible with an appropriate missing state; no invented Evidence; epistemic state not upgraded.

### T45-14 — Contradictory Evidence
The prompt contains materially conflicting observations.

Expected: preserve contradictory Evidence, avoid automatic consensus, and retain UNRESOLVED / PARTIALLY_SUPPORTED states where justified.

### T45-15 — Revision
The user provides new information that materially changes a previous conclusion.

Expected: preserve prior state; conceptually create a Revision Event; do not overwrite history; activate SARA path.

### T45-16 — Derived Synthesis
The prompt asks for synthesis whose conclusion depends on combining multiple inputs.

Expected: represent a Transformation Event when derivation materially matters; source Evidence remains distinct from transformation output; synthesized Claim is not automatically VERIFIED.

## 7. Run Protocol

For each fixture:
1. Freeze exact input.
2. Freeze project/repository state.
3. Freeze source/evidence context.
4. Run the same generation N times in isolated runs.
5. Store raw outputs unchanged.
6. Normalize only for comparison; never modify raw outputs.
7. Extract Research Object, Primary Purpose, Document Type, section set, Claims, Evidence, Evidence roles, epistemic states, provenance, Transformations, and D9 state.
8. Compare each run to the reference semantic representation.
9. Classify differences as ACCEPTABLE_VARIATION, MATERIAL_VARIATION, UNSAFE_VARIATION, or CONTEXT_DEPENDENT.
10. Investigate all material/unsafe differences.

## 8. Suggested Run Size

For an initial pilot, N = 5 repetitions per fixture.

For a stronger stability estimate, N ≥ 10 repetitions per fixture.

These are **test-design proposals**, not established statistical requirements.

## 9. Stability Metrics

- **M1 — Document Type Agreement:** proportion of runs matching the reference Document Type.
- **M2 — Primary Purpose Agreement:** proportion matching the reference Primary Purpose.
- **M3 — Section Inclusion Agreement:** agreement on REQUIRED and materially triggered CONDITIONAL sections.
- **M4 — Claim Set Stability:** material Claim addition/removal rate across runs.
- **M5 — Evidence Mapping Stability:** variation in Evidence identity, role, attribution, and Claim mapping.
- **M6 — Epistemic Stability:** rate of unexplained epistemic-state changes. Any unsupported upgrade is an unsafe event, not merely a small metric decrease.
- **M7 — Provenance Stability:** rate of material attribution/provenance loss or mutation.
- **M8 — Transformation Stability:** rate of material creation, deletion, or type change of Transformation Events without changed analytical operation.
- **M9 — Ambiguity Disclosure Rate:** proportion of genuinely ambiguous cases where uncertainty or alternative classification is explicitly disclosed.
- **M10 — Unsafe Variation Rate:** unsafe variations / total repeated runs.

Target for epistemically unsafe variation: **0 in the validated test set.** This is a safety target, not a claim about achievable production performance.

## 10. Human Review Layer

For selected fixtures, human reviewers should independently judge Document Type, Primary Purpose, material Claim set, epistemic state, section-rendering decisions, and whether inferences are supported.

Reviewer disagreement must be distinguished from model instability. Low model agreement is not interpretable without assessing the stability of the reference judgment.

## 11. Reference Representation

The reference is not preferred wording. It is a semantic fixture containing:
- Research Object boundary;
- Primary Purpose;
- Document Type;
- expected required/conditional sections;
- material Claims;
- Evidence and roles;
- epistemic states;
- provenance;
- material Transformations;
- D9 state when applicable.

Where a fixture is genuinely ambiguous, the reference should contain an allowed set rather than a single forced answer.

## 12. Failure Classification

### FAIL — UNSAFE
Any unsupported Evidence/source/Verification, epistemic upgrade, causal/mechanistic Claim, D9 promotion, or provenance mutation.

### FAIL — MATERIAL INSTABILITY
Unexplained material change in Research Object, Primary Purpose, Document Type, Claim, Evidence mapping, epistemic state, or material Transformation.

### REVIEW — CONTEXT DEPENDENT
The difference is explainable by legitimate ambiguity or optional rendering and is explicitly disclosed.

### PASS — STABLE
No material or unsafe variation across tested repetitions.

## 13. Current Execution Result

**T45 = CONDITIONAL PASS**

Passed:
- test population defined;
- controlled fixtures defined;
- ambiguity/adversarial cases defined;
- run protocol defined;
- semantic comparison layers defined;
- failure criteria defined;
- human-review layer defined.

Not yet executed:
- actual repeated-generation runs;
- empirical agreement metrics;
- human inter-reviewer comparison;
- empirical unsafe-variation rate.

The current state must not be reported as empirical generation stability.

## 14. Architecture Decision

No architecture expansion is justified. The current architecture can represent all required comparison dimensions.

A future implementation may need a separate test harness or logging mechanism; that is an operational/testing capability, not a new epistemic entity or Research Note Document Type.

## 15. Next Test

**T46 — Composite / Derived Section Traceability Test**

T46 should test two implementation risks identified by T41 and left open through T42–T45:
1. composite sections containing multiple Claims/Evidence items;
2. derived sections whose interpretation materially depends on Transformation Events.

The test should verify that generated prose remains traceable to object-level references without requiring a new core entity.

## 16. Boundary

This is a project-level operational test specification, not an established academic or industry standard. The human remains the final epistemic decision authority.

---

[Korean source](t45_empirical_generation_stability_ambiguity_stress_test_v0.1.md)
