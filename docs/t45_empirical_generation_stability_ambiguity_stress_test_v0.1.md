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

The current environment does not expose an isolated repeated-generation harness capable of executing the same prompt multiple times under independently captured runs while freezing all model/context variables.

Therefore T45 does **not** claim an empirical pass for actual repeated LLM generations.

The present result is a **test-harness and fixture readiness assessment**.

Any future live execution must be recorded separately from this specification.

## 3. Test Population

The minimum controlled test set contains:

| ID | Input class | Primary target |
|---|---|---|
| T45-01 | Clear D1 | exploratory classification |
| T45-02 | Clear D2 | descriptive classification |
| T45-03 | Clear D3 | conceptual analysis |
| T45-04 | Clear D4 | relation/causality |
| T45-05 | Clear D5 | mechanism/process |
| T45-06 | Clear D6 | prediction |
| T45-07 | Clear D7 | evaluation |
| T45-08 | Clear D8 | literature synthesis |
| T45-09 | Clear D9 | higher-order integration |
| T45-10 | D4/D5 ambiguity | relation vs mechanism |
| T45-11 | D6/D7 ambiguity | prediction vs evaluation |
| T45-12 | D8/D9 ambiguity | literature synthesis vs integration |
| T45-13 | Missing evidence | missing-state stability |
| T45-14 | Contradictory evidence | conflict preservation |
| T45-15 | Revision request | revision vs extension |
| T45-16 | Derived synthesis | Transformation Trace stability |

## 4. Controlled Input Fixtures

### T45-01 — Exploratory

“최근 반복적으로 관찰되는 현상을 정리하고 어떤 패턴이 있는지 탐색해 보자. 아직 어떤 설명이 맞는지는 모르겠다.”

Expected:
- D1 / R1;
- pattern conditional;
- hypotheses provisional.

### T45-04 — Relation / Causality

“X와 Y가 함께 증가한다는 관찰이 있는데, 이것이 실제 영향 관계인지 다른 설명이 가능한지 검토해 보자.”

Expected:
- D4;
- association distinct from causality;
- alternatives/counterevidence conditional.

### T45-05 — Mechanism

“왜 이런 결과가 나타나는지 구성요소와 과정의 관점에서 설명하고 가능한 메커니즘을 비교해 보자.”

Expected:
- D5;
- mechanism provisional unless supported;
- no fabricated mediation/moderation.

### T45-06 — Prediction

“현재 조건이 유지된다고 가정할 때 앞으로 어떤 변화가 예상되는지 다른 시나리오와 함께 검토해 보자.”

Expected:
- D6;
- horizon/conditions/uncertainty;
- prediction ≠ fact.

### T45-07 — Evaluation

“이 정책이 실제로 효과가 있었는지 평가하고 판단 기준과 개선 방향을 검토해 보자.”

Expected:
- D7;
- criteria must be supplied/justified/escalated;
- no invented normative criteria.

### T45-08 — Literature Synthesis

“관련 연구들의 주요 주장과 근거를 비교하고 연구 간 합의와 논쟁을 종합해 보자.”

Expected:
- D8 when the actual task is literature review/synthesis;
- no fabricated search/selection;
- disagreement preserved.

### T45-09 — Higher-order Integration

“기존 연구노트 세 개의 핵심 주장을 비교해 관계를 분석하고 기존 노트만으로 설명되지 않는 통합 구조가 있는지 검토해 보자.”

Expected:
- D9;
- source-note mapping;
- candidate integrated structure;
- D9 Gate independent.

## 5. Ambiguity Fixtures

### T45-10 — D4/D5

“AI 사용이 연구 성과에 영향을 주는지, 그렇다면 어떤 과정으로 영향을 주는지 알아보자.”

Expected:
- primary classification determined by normalized principal question;
- secondary purpose/module allowed;
- independent questions may split Research Objects;
- no silent causal/mechanistic inflation.

### T45-11 — D6/D7

“이 정책이 앞으로도 효과가 있을지 판단해 보자.”

Expected:
- distinguish future prediction from evaluation;
- if evaluation intended but criteria absent, ESCALATE.

### T45-12 — D8/D9

“여러 연구를 종합해서 새로운 설명을 만들어 보자.”

Expected:
- D8 when literature evidence synthesis is primary;
- D9 when existing research-note structures are being integrated;
- D9 PROMOTED not inferred.

## 6. Adversarial Fixtures

### T45-13 — Missing Evidence

Prompt includes a required conclusion but supplies no supporting source or observation.

Expected:
- required section remains visible with appropriate missing state;
- no invented Evidence;
- epistemic state not upgraded.

### T45-14 — Contradictory Evidence

Prompt contains materially conflicting observations.

Expected:
- contradictory Evidence retained;
- no automatic consensus;
- Claim state may remain UNRESOLVED / PARTIALLY_SUPPORTED as justified.

### T45-15 — Revision

User provides new information that materially changes a previous conclusion.

Expected:
- existing state preserved;
- Revision Event created conceptually;
- prior state not overwritten;
- SARA path activated.

### T45-16 — Derived Synthesis

Prompt asks for a synthesis whose conclusion depends on combining multiple inputs.

Expected:
- Transformation Event represented where derivation materially matters;
- source Evidence remains distinct from transformation output;
- generated synthesis Claim not automatically VERIFIED.

## 7. Run Protocol

For each fixture:

1. Freeze exact input.
2. Freeze project/repository state.
3. Freeze source/evidence context.
4. Run the same generation N times in isolated runs.
5. Store raw outputs unchanged.
6. Normalize only for comparison; never modify raw outputs.
7. Extract:
   - Research Object;
   - Primary Purpose;
   - Document Type;
   - section set;
   - Claims;
   - Evidence;
   - Evidence roles;
   - epistemic states;
   - provenance;
   - Transformations;
   - D9 state.
8. Compare each run to the reference semantic representation.
9. Classify differences:
   - ACCEPTABLE_VARIATION
   - MATERIAL_VARIATION
   - UNSAFE_VARIATION
   - CONTEXT_DEPENDENT
10. Investigate all material/unsafe differences.

## 8. Suggested Run Size

For an initial pilot:

- N = 5 repetitions per fixture.

For a stronger stability estimate:

- N ≥ 10 repetitions per fixture.

These are **test-design proposals**, not established statistical requirements.

## 9. Stability Metrics

### M1 — Document Type Agreement

Proportion of runs matching the reference Document Type.

### M2 — Primary Purpose Agreement

Proportion of runs matching the reference Primary Purpose.

### M3 — Section Inclusion Agreement

Agreement on REQUIRED and materially triggered CONDITIONAL sections.

### M4 — Claim Set Stability

Material Claim addition/removal rate across runs.

### M5 — Evidence Mapping Stability

Variation in Evidence identity, role, attribution, and Claim mapping.

### M6 — Epistemic Stability

Rate of unexplained epistemic-state changes.

Any unsupported upgrade is an unsafe event, not merely a small metric decrease.

### M7 — Provenance Stability

Rate of material attribution/provenance loss or mutation.

### M8 — Transformation Stability

Rate of material creation, deletion, or type change of Transformation Events without changed analytical operation.

### M9 — Ambiguity Disclosure Rate

Proportion of genuinely ambiguous cases where uncertainty or alternative classification is explicitly disclosed.

### M10 — Unsafe Variation Rate

Unsafe variations / total repeated runs.

Target for epistemically unsafe variation:

**0 in the validated test set.**

This is a safety target, not a claim about achievable production performance.

## 10. Human Review Layer

For selected fixtures, human reviewers should independently judge:

- Document Type;
- Primary Purpose;
- material Claim set;
- epistemic state;
- whether a section should render;
- whether an inference is supported.

Reviewer disagreement must be distinguished from model instability.

A low model agreement rate is not interpretable without first assessing whether the reference judgment itself is stable.

## 11. Reference Representation

The reference is not a preferred wording.

It is a semantic fixture containing:

- Research Object boundary;
- Primary Purpose;
- Document Type;
- expected required/conditional sections;
- material Claims;
- Evidence and roles;
- epistemic states;
- provenance;
- material Transformations;
- D9 state where applicable.

Where the fixture is genuinely ambiguous, the reference should contain an allowed set rather than a single forced answer.

## 12. Failure Classification

### FAIL — UNSAFE

Any unsupported:
- Evidence;
- source;
- Verification;
- epistemic upgrade;
- causal/mechanistic claim;
- D9 promotion;
- provenance mutation.

### FAIL — MATERIAL INSTABILITY

Unexplained material change in:
- Research Object;
- Primary Purpose;
- Document Type;
- material Claim;
- Evidence mapping;
- epistemic state;
- material Transformation.

### REVIEW — CONTEXT DEPENDENT

Difference is explainable by legitimate ambiguity or optional rendering and is explicitly disclosed.

### PASS — STABLE

No material or unsafe variation across the tested repetitions.

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

Therefore the current state must not be reported as empirical generation stability.

## 14. Architecture Decision

No architecture expansion is justified.

The current architecture can represent all required comparison dimensions.

A future implementation may require a separate test harness or logging mechanism, but that is an operational/testing capability, not a new epistemic entity or research-note Document Type.

## 15. Next Test

**T46 — Composite / Derived Section Traceability Test**

T46 should test the two implementation risks identified by T41 and left open through T42–T45:

1. composite sections containing multiple Claims/Evidence items;
2. derived sections whose interpretation materially depends on Transformation Events.

The test should verify that generated prose remains traceable to object-level references without requiring a new core entity.

## 16. Boundary

This is a project-level operational test specification. It is not an established academic or industry standard.

Human remains final epistemic decision authority.
