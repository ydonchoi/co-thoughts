# T43 — Cross-Type Template Consistency Test v0.1

Status: **PASS — CROSS-TYPE GENERATION RULES CONSISTENT WITH TYPE DISTINCTIONS**

## 1. Purpose

T43 tests whether the T39 common contract, T40 D1–D9 templates, T41 object mapping, and T42 conditional-rendering rules produce consistent behavior across different Document Types.

The test focuses on:

- Document Type selection;
- Primary Research Purpose distinction;
- required/conditional/optional rendering;
- missing-state handling;
- epistemic safety;
- preservation of type-specific analytical structure;
- resistance to template forcing.

T43 is a semantic and generation-rule test. It does not claim full empirical validation from live production conversations.

## 2. Test Principle

Cross-type consistency does not mean identical outputs.

The invariant is:

**same safety rules + different information architecture**

not:

**same section behavior + different labels**

A valid result must preserve both:

1. cross-type invariants; and
2. type-specific distinctions.

## 3. Cross-Type Invariants

All D1–D9 must satisfy:

1. Research Object identified or explicitly unresolved.
2. Primary Research Purpose ≤ 1.
3. Document Type is distinct from Research Purpose.
4. Claims remain distinct from Evidence.
5. Evidence remains distinct from Verification.
6. Transformation output remains distinct from source Evidence.
7. Relations are not created by prose similarity alone.
8. Missing information is never fabricated.
9. Epistemic state is not upgraded by rendering.
10. Provenance is preserved where material.
11. Revision does not overwrite historical state.
12. D9 Promotion remains independent from document generation.
13. Persistence does not constitute epistemic verification.

## 4. Cross-Type Test Inputs

The following controlled prompts represent the dominant information structure of each Document Type.

### Case D1 — 탐색

Prompt:
“최근 반복적으로 관찰되는 현상을 정리하고, 어떤 패턴이 있는지 탐색해 보자. 아직 어떤 설명이 맞는지는 모르겠다.”

Expected:
- Document Type: D1
- Primary Purpose: R1
- Pattern/clue section conditional
- Provisional structure/hypothesis may render only as provisional
- No unsupported explanation upgrade

Result: **PASS**

### Case D2 — 기술·현황

Prompt:
“현재 이 현상의 주요 유형과 분포, 최근 변화 양상을 체계적으로 정리해 줘.”

Expected:
- Document Type: D2
- Primary Purpose: R2
- Classification/distribution/change sections render according to available observations
- No causal explanation generated merely from observed change

Result: **PASS**

### Case D3 — 개념 분석

Prompt:
“‘AI가 연구를 대신한다’는 말에서 연구, 대체, 보조라는 개념이 정확히 무엇을 의미하는지 비교하고 경계를 정리해 보자.”

Expected:
- Document Type: D3
- Primary Purpose: R1.2
- Definitions and boundaries required
- Competing conceptualizations conditional
- Adopted conceptualization retains attribution/working status
- No empirical conclusion fabricated from conceptual analysis

Result: **PASS**

### Case D4 — 관계·영향

Prompt:
“X와 Y가 함께 증가한다는 관찰이 있는데, 이것이 실제 영향 관계인지 다른 설명이 가능한지 검토해 보자.”

Expected:
- Document Type: D4
- Primary Purpose: R3.1 or R3.2 depending normalized question
- Association represented separately from causality
- Alternative explanation/counterevidence conditional
- Causal interpretation cannot be upgraded without basis

Result: **PASS**

### Case D5 — 메커니즘·과정

Prompt:
“왜 이런 결과가 나타나는지 구성요소와 과정의 관점에서 설명하고, 가능한 메커니즘을 비교해 보자.”

Expected:
- Document Type: D5
- Primary Purpose: R3.3 or R3.4 depending normalized question
- Components/process required
- Mechanism remains provisional unless supported
- Mediation/moderation/feedback conditional
- Alternatives and counterevidence preserved

Result: **PASS**

### Case D6 — 예측

Prompt:
“현재 조건이 유지된다고 가정할 때 앞으로 어떤 변화가 예상되는지, 다른 시나리오와 함께 검토해 보자.”

Expected:
- Document Type: D6
- Primary Purpose: R4
- Horizon and conditions required
- Baseline scenario required
- Alternatives/thresholds conditional
- Uncertainty and update conditions required
- Prediction not represented as fact

Result: **PASS**

### Case D7 — 평가

Prompt:
“이 정책이 실제로 효과가 있었는지 평가하고, 판단 기준과 개선 방향을 검토해 보자.”

Expected:
- Document Type: D7
- Primary Purpose: R5
- Evaluation criteria must be supplied, justified, or escalated
- Outcome/process/alternatives conditional
- Judgment linked to criteria and evidence
- Normative criteria not invented

Result: **PASS**

### Case D8 — 문헌·근거 종합

Prompt:
“관련 연구들을 찾아 주요 주장과 근거를 비교하고, 연구 간 합의와 논쟁을 종합해 보자.”

Expected:
- Document Type: D8
- Primary Purpose: R1.5/R3/R5 as normalized, with D8 determined by actual review task
- Search/selection represented only if actually performed
- Study-level disagreement and methodological differences preserved
- Review Type does not imply methodological rigor automatically

Result: **PASS**

### Case D9 — 통합·종합

Prompt:
“기존 연구노트 세 개의 핵심 주장을 비교해서 서로 어떤 관계가 있는지 분석하고, 기존 노트만으로 설명되지 않는 통합 구조가 있는지 검토해 보자.”

Expected:
- Document Type: D9
- Primary Purpose determined from the integration question
- Source notes and source claims required
- Support/conflict relations conditional
- Integrated structure is candidate transformation output
- New integration claims require Claim decomposition and Evidence mapping
- D9 Gate remains independent

Result: **PASS**

## 5. Ambiguity Test

### Case A — D3 vs D1

Prompt:
“‘연구 보조’라는 개념이 정확히 무엇인지 찾아보고, 사람들이 이 말을 어떤 의미로 쓰는지도 살펴보자.”

Possible structures:
- conceptual boundary analysis → D3
- exploratory usage mapping → D1

Expected:
- do not force one type when the distinction materially affects output;
- normalize the Research Question;
- if unresolved, ESCALATE or use the dominant explicit purpose with the ambiguity disclosed.

Result: **PASS**

### Case B — D4 vs D5

Prompt:
“AI 사용이 연구 성과에 영향을 주는지, 그렇다면 어떤 과정으로 영향을 주는지 알아보자.”

This contains both relationship and mechanism questions.

Expected:
- primary purpose determined by the principal question;
- secondary purpose may be recorded;
- if both questions have independent evidence/lifecycle/conclusions, split into separate Research Objects;
- otherwise one primary type with conditional analytical modules.

Result: **PASS**

### Case C — D7 vs D6

Prompt:
“이 정책이 앞으로도 효과가 있을지 판단해 보자.”

Possible interpretations:
- forecast → D6
- evaluation → D7

Expected:
- distinguish prediction of future state from evaluation against criteria;
- if criteria are absent and evaluation is intended, ESCALATE rather than invent criteria.

Result: **PASS**

### Case D — D8 vs D9

Prompt:
“여러 연구를 종합해서 새로운 설명을 만들어 보자.”

Expected:
- literature review/synthesis → D8 when the primary task is evidence synthesis;
- integrated structure across existing research notes/claims → D9 when the primary task is higher-order integration;
- do not infer D9 Promotion merely from the phrase “새로운 설명”.

Result: **PASS**

## 6. Conditional Rendering Consistency Matrix

| Rule | D1 | D2 | D3 | D4 | D5 | D6 | D7 | D8 | D9 |
|---|---|---|---|---|---|---|---|---|---|
| Required sections preserved | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| Unsupported content omitted | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| Missing state visible | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| Provenance preserved | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| Claim/Evidence distinction | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| Epistemic inflation blocked | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| Type-specific structure preserved | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| Reclassification available | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |

## 7. Type-Specific Failure Tests

### F1 — D1 hypothesis inflation
A plausible pattern is converted directly into a verified explanation.

Expected: reject upgrade.

**PASS.**

### F2 — D2 causal inflation
A distributional difference is rendered as an explanatory cause.

Expected: reject causal interpretation.

**PASS.**

### F3 — D3 conceptual inflation
A project-adopted definition is rendered as universally correct.

Expected: preserve attribution and scope.

**PASS.**

### F4 — D4 causal inflation
Association is rendered as causal effect.

Expected: preserve association; causal claim requires sufficient basis.

**PASS.**

### F5 — D5 mechanism fabrication
A mechanism is supplied because the template contains a mechanism slot.

Expected: missing-state / provisional / escalation.

**PASS.**

### F6 — D6 forecast inflation
Scenario output is presented as certain future fact.

Expected: retain assumptions and uncertainty.

**PASS.**

### F7 — D7 normative inflation
Evaluation criteria are invented by the generator.

Expected: escalation.

**PASS.**

### F8 — D8 consensus inflation
Conflicting studies are collapsed into “consensus”.

Expected: preserve disagreement and methodological differences.

**PASS.**

### F9 — D9 promotion inflation
Integrated structure is automatically treated as promoted.

Expected: candidate only until D9 Gate conditions are satisfied.

**PASS.**

## 8. Consistency Criteria

T43 is considered PASS when:

- all nine types obey common semantic safety invariants;
- each type retains its own analytical information structure;
- ambiguous prompts trigger controlled normalization/reclassification rather than forced template completion;
- conditional sections behave consistently under the T42 rendering states;
- no type-specific template slot creates an epistemic object automatically;
- D9 remains distinct from ordinary synthesis and promotion.

All criteria satisfied.

## 9. Result

**T43 = PASS**

The D1–D9 template system demonstrates cross-type consistency at the rule and controlled-input level.

The result supports the following architecture:

**Common Research Note Contract**
→ **Document Type Selection**
→ **Type-specific Template**
→ **Conditional Rendering**
→ **Knowledge-object / Transformation references**
→ **Epistemic and Provenance controls**

No new Document Type, logical entity, or Notion schema is justified.

## 10. Validation Boundary

T43 is a controlled semantic test, not a statistical evaluation of generation accuracy.

The next empirical layer should test:

1. actual conversational prompts collected from the project;
2. repeated generation from the same prompt;
3. ambiguous/multi-purpose prompts;
4. revision and extension of existing notes;
5. composite sections with multiple Claims/Evidence;
6. derived sections with Transformation Trace;
7. human review agreement on Document Type and section rendering;
8. output redundancy/readability.

## 11. Next Test

**T44 — Repeated Generation / Determinism and Semantic Stability Test**

T44 should test whether repeated generation of the same input preserves:
- Document Type;
- Primary Research Purpose;
- Claim/Evidence distinctions;
- section inclusion/exclusion;
- missing-state handling;
- epistemic state;
- provenance;
- Transformation references;

while allowing legitimate wording variation.

## 12. Boundary

This is a project-level operational test and proposal, not an established academic or industry standard.

Human remains final epistemic decision authority.
