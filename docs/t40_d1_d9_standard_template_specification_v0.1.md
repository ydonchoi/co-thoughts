# T40 — D1–D9 Standard Template Specification v0.1

Status: **PASS — INITIAL OPERATIONAL TEMPLATE SPECIFICATION**

## 1. Purpose

T40 converts the existing D1–D9 document structures into contract-compliant standard templates using T39.

This specification defines section IDs, status, purpose, primary inputs, output intent, omission conditions, and inference constraints.

It does not redefine Research Purpose, Claim, Evidence, Verification, Transformation Event, Relation, or D9 semantics.

## 2. Common Template Rules

All D1–D9 templates inherit:

- Common Metadata
- Common Framing
- Claim/Evidence/Verification separation
- provenance preservation
- uncertainty disclosure
- non-destructive revision
- SARA rendering rules
- missing-information safety

Section statuses:
- REQUIRED
- CONDITIONAL
- OPTIONAL

A REQUIRED section may report NOT_AVAILABLE / NOT_ESTABLISHED / REQUIRES_VERIFICATION / UNRESOLVED rather than fabricate content.

## 3. D1 — 탐색 연구노트

Primary function: structure an inquiry space before the object is sufficiently understood.

| ID | Section | Status | Purpose |
|---|---|---|---|
| D1.01 | 대상/목적 | REQUIRED | define inquiry target and purpose |
| D1.02 | 현재 지식 | REQUIRED | establish known state and starting evidence |
| D1.03 | 범위 | REQUIRED | define inquiry boundary |
| D1.04 | 현상/문제 | REQUIRED | describe observed phenomenon/problem |
| D1.05 | 패턴/단서 | CONDITIONAL | identify evidence-supported signals |
| D1.06 | 잠정 구조 | CONDITIONAL | formulate provisional organization/model |
| D1.07 | 경쟁 해석 | CONDITIONAL | compare plausible explanations |
| D1.08 | 탐색 결과 | REQUIRED | summarize what exploration established |
| D1.09 | 생성 가설/모델 | CONDITIONAL | record newly generated hypotheses/models |
| D1.10 | 미지 영역 | REQUIRED | identify unresolved knowledge |
| D1.11 | 후속 질문 | REQUIRED | derive next research questions |

Constraints:
- D1 may generate hypotheses but must not upgrade them to verified claims.
- Pattern detection requires identifiable input evidence or explicit observation.
- Competitive interpretations must not be invented merely to create balance.

## 4. D2 — 기술·현황 연구노트

Primary function: describe characteristics, composition, distribution, and change.

| ID | Section | Status | Purpose |
|---|---|---|---|
| D2.01 | 대상/목적/범위 | REQUIRED | define descriptive boundary |
| D2.02 | 관찰·분류 기준 | REQUIRED | state observation/classification basis |
| D2.03 | 특성 | REQUIRED | describe observed attributes |
| D2.04 | 구성/유형 | CONDITIONAL | describe categories/components |
| D2.05 | 분포 | CONDITIONAL | describe distribution when data exist |
| D2.06 | 변화 | CONDITIONAL | describe temporal/change patterns |
| D2.07 | 패턴/예외 | CONDITIONAL | identify recurring patterns or exceptions |
| D2.08 | 요약 | REQUIRED | synthesize descriptive findings |
| D2.09 | 한계/미지 | REQUIRED | state coverage and unknowns |

Constraints:
- Description must not be silently converted into causal explanation.
- Absence of observed variation does not prove absence of variation.
- Classification criteria must be explicit where classification affects conclusions.

## 5. D3 — 개념 분석 연구노트

Primary function: analyze meaning, structure, boundaries, dimensions, and competing conceptualizations.

| ID | Section | Status | Purpose |
|---|---|---|---|
| D3.01 | 개념/질문 | REQUIRED | define focal concept and question |
| D3.02 | 배경 | CONDITIONAL | establish historical/theoretical context |
| D3.03 | 주요 정의 | REQUIRED | represent relevant definitions |
| D3.04 | 정의 차이 | CONDITIONAL | compare definitional variation |
| D3.05 | 핵심 속성 | REQUIRED | identify defining/central attributes |
| D3.06 | 경계 | REQUIRED | distinguish inclusion/exclusion |
| D3.07 | 인접 개념 | CONDITIONAL | distinguish related concepts |
| D3.08 | 구성/차원 | CONDITIONAL | structure concept dimensions |
| D3.09 | 개념 관계 | CONDITIONAL | map relations to other concepts |
| D3.10 | 경쟁적 개념화 | CONDITIONAL | compare competing conceptualizations |
| D3.11 | 채택 개념화 | REQUIRED | state adopted working conceptualization |
| D3.12 | 범위/한계 | REQUIRED | state applicability and limitations |
| D3.13 | 후속 질문 | REQUIRED | identify unresolved conceptual questions |

Constraints:
- Definitions must preserve attribution/provenance.
- Project interpretation must not be presented as authorial definition.
- A selected conceptualization is not automatically empirically verified.

## 6. D4 — 관계·영향 분석 연구노트

Primary function: analyze relations, associations, effects, and competing causal interpretations.

| ID | Section | Status | Purpose |
|---|---|---|---|
| D4.01 | 질문 | REQUIRED | define relation/impact question |
| D4.02 | 대상/변수/개념 | REQUIRED | define relational units |
| D4.03 | 기존 설명 | REQUIRED | represent prior explanations |
| D4.04 | 관계 구조 | REQUIRED | map relationships |
| D4.05 | 방향/형태 | CONDITIONAL | characterize direction/form |
| D4.06 | 비교/차이 | CONDITIONAL | compare groups/conditions |
| D4.07 | 영향 가능성 | CONDITIONAL | assess possible effects |
| D4.08 | 인과 해석 | CONDITIONAL | state causal interpretation only when warranted |
| D4.09 | 대안 설명 | CONDITIONAL | identify competing explanations |
| D4.10 | 반증/반대근거 | CONDITIONAL | represent contradictory evidence |
| D4.11 | 경계조건 | REQUIRED | specify conditions/limits |
| D4.12 | 검증 상태 | REQUIRED | expose relevant verification states |
| D4.13 | 결론 | REQUIRED | state current relational conclusion |

Constraints:
- Association must not be rendered as causation without adequate support.
- Causal language must track evidence and verification state.
- Alternative explanations must be evidence-grounded or explicitly marked as hypotheses.

## 7. D5 — 메커니즘·과정 분석 연구노트

Primary function: explain how a system or phenomenon operates through processes and mechanisms.

| ID | Section | Status | Purpose |
|---|---|---|---|
| D5.01 | 질문 | REQUIRED | define mechanism/process question |
| D5.02 | 대상 | REQUIRED | define system/process boundary |
| D5.03 | 기존 설명 | REQUIRED | represent existing mechanisms/explanations |
| D5.04 | 구성요소 | REQUIRED | identify relevant components |
| D5.05 | 관계 구조 | REQUIRED | map component relations |
| D5.06 | 과정 | REQUIRED | represent temporal/functional sequence |
| D5.07 | 잠정 메커니즘 | CONDITIONAL | formulate mechanism when supported |
| D5.08 | 매개/조절/피드백 | CONDITIONAL | represent higher-order process relations |
| D5.09 | 대안 | CONDITIONAL | compare competing mechanisms |
| D5.10 | 근거 | REQUIRED | map evidence to mechanism claims |
| D5.11 | 반대근거 | CONDITIONAL | represent contradictory evidence |
| D5.12 | 경계 | REQUIRED | define mechanism applicability |
| D5.13 | 검증 상태 | REQUIRED | expose verification state |
| D5.14 | 결론/후속 | REQUIRED | state current mechanism and next questions |

Constraints:
- Mechanisms must not be fabricated to fill a structural slot.
- A plausible process description is not automatically a verified mechanism.
- Mediation/moderation/feedback terminology requires corresponding analytical support.

## 8. D6 — 예측 연구노트

Primary function: generate and evaluate conditional forecasts.

| ID | Section | Status | Purpose |
|---|---|---|---|
| D6.01 | 예측 질문 | REQUIRED | define forecast target |
| D6.02 | 대상/기간 | REQUIRED | define target and horizon |
| D6.03 | 현재 상태 | REQUIRED | establish forecast baseline |
| D6.04 | 근거 | REQUIRED | map forecast evidence |
| D6.05 | 변수/조건 | REQUIRED | identify predictive factors and conditions |
| D6.06 | 모델/논리 | REQUIRED | state forecasting model/logic |
| D6.07 | 기준 시나리오 | REQUIRED | define baseline scenario |
| D6.08 | 대안 시나리오 | CONDITIONAL | define materially distinct alternatives |
| D6.09 | 임계조건 | CONDITIONAL | identify thresholds/trigger conditions |
| D6.10 | 불확실성 | REQUIRED | expose forecast uncertainty |
| D6.11 | 검증/반증 조건 | REQUIRED | define future evaluation criteria |
| D6.12 | 결과 | REQUIRED | state forecast |
| D6.13 | 업데이트 조건 | REQUIRED | specify evidence that should update forecast |

Constraints:
- Forecast output is not current fact.
- Scenarios must retain their assumptions.
- Future verification conditions must be explicit where possible.

## 9. D7 — 평가 연구노트

Primary function: evaluate an object against explicit criteria and support decision-making.

| ID | Section | Status | Purpose |
|---|---|---|---|
| D7.01 | 대상 | REQUIRED | define evaluation object |
| D7.02 | 목적 | REQUIRED | define evaluation purpose |
| D7.03 | 평가기준 | REQUIRED | state criteria |
| D7.04 | 기준 근거 | REQUIRED | justify criteria |
| D7.05 | 현재 상태 | REQUIRED | establish baseline |
| D7.06 | 효과/성과/영향 | CONDITIONAL | evaluate relevant outcomes |
| D7.07 | 과정 | CONDITIONAL | evaluate implementation/process |
| D7.08 | 대안 | CONDITIONAL | compare alternatives |
| D7.09 | 긍정/부정 결과 | REQUIRED | balance findings |
| D7.10 | 불확실성/한계 | REQUIRED | expose evaluation limitations |
| D7.11 | 판단 | REQUIRED | state evidence-based judgment |
| D7.12 | 개선/의사결정 함의 | CONDITIONAL | derive actionable implications |

Constraints:
- Evaluation criteria must not be invented merely to reach a judgment.
- Judgment must remain traceable to criteria and evidence.
- Recommendation is distinct from evidence and verification.

## 10. D8 — 문헌·근거 종합 연구노트

Primary function: systematically or transparently synthesize literature/evidence.

| ID | Section | Status | Purpose |
|---|---|---|---|
| D8.01 | 검토 질문 | REQUIRED | define synthesis question |
| D8.02 | 범위/포함 기준 | REQUIRED | define evidence boundary |
| D8.03 | 검색/선별 | REQUIRED | document retrieval/selection process when applicable |
| D8.04 | 개념 | CONDITIONAL | normalize relevant concepts |
| D8.05 | 연구 흐름 | CONDITIONAL | describe literature development |
| D8.06 | 주장 | REQUIRED | extract/structure study claims |
| D8.07 | 근거 비교 | REQUIRED | compare evidence |
| D8.08 | 합의 | CONDITIONAL | identify supported convergence |
| D8.09 | 불일치/논쟁 | CONDITIONAL | preserve disagreement |
| D8.10 | 방법론 차이 | CONDITIONAL | account for methodological heterogeneity |
| D8.11 | 근거 강도/한계 | REQUIRED | assess evidence limitations |
| D8.12 | 종합 | REQUIRED | produce synthesis result |
| D8.13 | 연구 공백 | CONDITIONAL | identify supported gaps |
| D8.14 | 후속 질문 | REQUIRED | derive future research questions |

Review Type is metadata, not a claim of methodological rigor by itself:
Narrative Review, Systematic Review, Scoping Review, Integrative Review, Meta-analysis, Qualitative Synthesis, Other.

Constraints:
- “Consensus” must not erase disagreement.
- Synthesis is a transformation operation/result, not Evidence by itself.
- Literature absence must not automatically be interpreted as research absence.

## 11. D9 — 통합·종합 연구노트

Primary function: construct a new, traceable integration across existing Research Notes/Objects.

| ID | Section | Status | Purpose |
|---|---|---|---|
| D9.01 | 대상 note | REQUIRED | identify integrated source notes/objects |
| D9.02 | 통합 질문 | REQUIRED | define higher-order question |
| D9.03 | 각 note 핵심 주장 | REQUIRED | represent source claims |
| D9.04 | 공통점 | CONDITIONAL | identify shared structure |
| D9.05 | 긴장/차이 | CONDITIONAL | preserve meaningful differences |
| D9.06 | support relations | CONDITIONAL | map supporting relations |
| D9.07 | conflict | CONDITIONAL | map contradictions/conflicts |
| D9.08 | 통합 가능한 구조 | REQUIRED | identify candidate higher-order structure |
| D9.09 | 통합 설명/모델 | CONDITIONAL | formulate integrated explanation/model |
| D9.10 | 통합 근거 | REQUIRED | map evidence to integration claims |
| D9.11 | 한계 | REQUIRED | state integration limits |
| D9.12 | 미해결 문제 | REQUIRED | preserve unresolved tensions |
| D9.13 | 새 질문 | REQUIRED | generate higher-order follow-up questions |

D9-specific controls:
- D9 is not a summary-only format.
- New integration claims require Claim decomposition and Evidence Mapping.
- D9 Gate G1–G6 remains independent of the template.
- D9 CANDIDATE and PROMOTED must be displayed separately.
- PROMOTED does not mean VERIFIED.
- Source-note epistemic states must not be overwritten by integration.

## 12. Cross-Type Conditional Modules

The following modules may be attached to any compatible template:

- Evidence Mapping
- Claim Decomposition
- Counter-evidence
- Competing Explanation
- Comparison
- Scenario Analysis
- Evaluation Criteria
- Literature Screening
- SARA
- Revision
- Relation Mapping
- D9 Gate

Modules are invoked by conditions, not by a requirement to fill every section.

## 13. Cross-Type Generation Rules

1. Select Document Type only after provisional classification and evidence-aware reclassification.
2. Use the minimum template sufficient for the selected type.
3. Render REQUIRED sections even when they contain an explicit missing/unresolved state.
4. Render CONDITIONAL sections only when trigger conditions are satisfied.
5. Never fabricate missing Claims, Evidence, Verification, Relations, mechanisms, variables, criteria, or literature findings.
6. Preserve attribution and temporal context.
7. Preserve Claim-level epistemic states.
8. Preserve revision history and provenance.
9. Treat synthesis as a Transformation Event/result unless independently supported as Evidence.
10. Persistence never changes epistemic state.
11. Human remains final epistemic decision authority.

## 14. Decision

**T40 = PASS**

The existing D1–D9 structures have been converted into an initial executable template specification.

This remains a **project-level template proposal**, not an established academic standard.

No new Document Type is introduced.
No new logical entity is introduced.
No Notion schema expansion is required.

## 15. Next Test

**T41 — Template ↔ Knowledge Object Mapping Test**

T41 should test whether each template section can be mapped without semantic inflation to Research Object, Claim, Evidence, Transformation Event, Verification, Relation, and Provenance.

## 16. Known Limitations

T40 defines structure and safety constraints but does not yet prove:

- complete object-to-section coverage;
- absence of redundant sections;
- generation consistency across real conversations;
- rendering quality;
- queryability of template-level metadata.

Those require subsequent tests.


## Cross-Type AI Disclosure Rule

All D1–D9 templates inherit a common artifact-level disclosure requirement:

**AI 작성·구조화 연구노트**

The marker is rendered outside the type-specific body and therefore survives changes in Document Type. The provenance block should retain generation system, AI participation, human-review status, and generation provenance.

D1–D9 must not reinterpret the marker as:
- Evidence;
- Verification;
- a Claim state;
- D9 promotion;
- source authorship.

Human edits and source-derived material remain separately attributable where provenance supports the distinction.
