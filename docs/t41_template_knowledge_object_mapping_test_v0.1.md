# T41 — Template ↔ Knowledge Object Mapping Test v0.1

Status: **PASS — SEMANTIC MAPPING VALIDATED WITH CONDITIONAL AREAS**

## 1. Purpose

T41 tests whether D1–D9 template sections can represent the Research Note Engine's logical objects without semantic inflation or object conflation.

Tested logical layers:

- Research Object
- Claim
- Evidence
- Transformation Event
- Verification
- Relation
- Provenance
- Version / Revision
- D9 Gate

The test evaluates mapping semantics, not Notion queryability.

## 2. Mapping Principle

A document section is a **rendering location**, not automatically a knowledge object.

Therefore:

Section
≠
Research Object / Claim / Evidence / Verification / Transformation / Relation

A section may render one or more referenced objects, but the underlying object identity must remain explicit.

## 3. Mapping Classes

### M1 — DIRECT

The section has a clear dominant logical object.

Examples:
- D1.01 대상 → Research Object
- D4.12 검증 상태 → Verification / epistemic-state rendering
- D9.01 대상 note → Research Object / Research Note references

### M2 — COMPOSITE

The section intentionally renders multiple object types.

Examples:
- D5.10 근거 → Evidence mapped to mechanism Claims
- D8.07 근거 비교 → Evidence + Claims + Transformation
- D9.08 통합 가능한 구조 → Relation + Transformation + candidate Claim

Composite sections must preserve object-level distinctions.

### M3 — DERIVED / TRANSFORMATIVE

The section primarily represents an output produced through a Transformation Event.

Examples:
- D1.06 잠정 구조
- D1.09 생성 가설/모델
- D6.12 예측 결과
- D8.12 종합
- D9.09 통합 설명/모델

These outputs are not automatically Evidence or Verification.

### M4 — CONTEXT / CONTROL

The section provides scope, boundary, process, or state control.

Examples:
- Scope / Boundary
- D8.02 포함 기준
- D6.10 불확실성
- D7.03 평가기준

These may affect Claims and transformations but are not themselves automatically Claims or Evidence.

## 4. Cross-Type Mapping Matrix

| Template area | Dominant object | Secondary object(s) | Mapping class |
|---|---|---|---|
| Target / 대상 | Research Object | Research Note | M1 |
| Research Question | Research Object / Question | Claim context | M1 |
| Scope / Boundary | Research Object | Claim / Evidence conditions | M4 |
| Current Knowledge | Claims | Evidence / Provenance | M2 |
| Phenomenon / Problem | Research Object | Claims / Evidence | M2 |
| Pattern / Clue | Evidence-derived result | Claim / Transformation | M3 |
| Provisional Structure | Transformation output | Relation / Claim | M3 |
| Definition | Claim / attributed representation | Provenance | M2 |
| Relation Structure | Relation | Claims / Evidence | M2 |
| Process | Transformation / Result representation | Claims / Relations | M3 |
| Mechanism | Claim / Model | Evidence / Transformation | M3 |
| Evidence | Evidence | Target Claims / Relations | M1 |
| Counter-evidence | Evidence | Contradicted Claims | M1 |
| Verification State | Verification / Epistemic State | Claim | M1 |
| Prediction | Claim / Model output | Evidence / Conditions | M3 |
| Evaluation Criteria | Evaluation structure | Evidence / Claim | M4 |
| Evaluation Judgment | Claim | Criteria / Evidence / Verification | M2 |
| Literature Synthesis | Transformation result | Claims / Evidence | M3 |
| Integrated Structure | Transformation result | Relations / Claims | M3 |
| Provenance | Provenance | all referenced objects | M1 |
| Revision History | Version / Revision Event | Claim / Evidence / Transformation changes | M1 |
| D9 Gate | D9 Gate | Claims / Relations / Evidence / SARA | M1 |

## 5. Critical Semantic Tests

### C1. Evidence Inflation — PASS

A section named “근거” is not itself Evidence.

Evidence identity must remain separately identifiable.

### C2. Claim Inflation — PASS

A generated section such as “종합”, “예측 결과”, or “판단” does not automatically become VERIFIED Claim.

Claim state remains separately represented.

### C3. Transformation Inflation — PASS

A process section or synthesis section may represent a Transformation Event/result, but the operation and result remain distinct.

### C4. Verification Inflation — PASS

A “검증 상태” display is a rendering of Verification / epistemic state. It does not create a Verification record merely by being present.

### C5. Relation Inflation — PASS

A section such as “공통점” or “관계 구조” may render Relations, but textual similarity alone does not create a typed Relation without an explicit relation basis.

### C6. Provenance Preservation — PASS

Definitions, literature claims, historical statements, and interpretations can retain source/attribution provenance without being collapsed into a single claim source.

### C7. D9 Promotion Inflation — PASS

D9 template rendering does not imply D9 PROMOTED.

D9 Gate remains a separate promotion mechanism.

### C8. Revision Inflation — PASS

A revised section does not overwrite the previous epistemic state. Revision remains a Version / Revision Event.

## 6. Type-Specific Risk Areas

### D1

“패턴/단서” can become unsupported pattern inference if evidence is not explicit.

Control: require identifiable evidence/observation and label generated structure as provisional.

### D3

“채택 개념화” can be mistaken for universally correct definition.

Control: preserve attribution and mark project-adopted conceptualization as a working representation.

### D4

“영향” and “인과 해석” can inflate association into causality.

Control: causal language must track evidence and verification.

### D5

“잠정 메커니즘” can become a fabricated explanatory mechanism.

Control: require evidence/analysis basis and preserve provisional status.

### D6

“예측 결과” can be mistaken for future fact.

Control: retain assumptions, horizon, uncertainty, and update conditions.

### D7

“판단” can conceal normative criteria or unsupported recommendations.

Control: criteria and evidence linkage must be explicit.

### D8

“합의” can erase heterogeneity and disagreement.

Control: preserve study-level claims, contradictory evidence, methodology differences, and scope.

### D9

“통합 가능한 구조” can be mistaken for a verified new theory/model.

Control: represent it as transformation output/candidate claim and apply D9 Gate separately.

## 7. Coverage Result

All nine Document Types have at least one valid mapping path to the core logical layers.

No Document Type requires a new logical entity.

No mapping requires treating Document Type as epistemic state.

No mapping requires treating Research Note as Evidence.

## 8. Conditional Findings

The mapping is semantically valid, but three areas require explicit implementation rules in later tests:

1. **Composite sections** need object-level anchors when multiple Claims/Evidence items are rendered.
2. **Derived sections** need Transformation Event references when the derivation materially matters.
3. **Verification displays** need a distinction between a display of state and an underlying Verification record.

These are implementation requirements, not reasons to expand the core data model.

## 9. Decision

**T41 = PASS**

D1–D9 template sections can be mapped to the Research Note Engine's logical objects without semantic inflation, provided object-level references and transformation/provenance links are preserved where applicable.

Architecture expansion is not justified.

## 10. Next Test

**T42 — Template Generation Rules / Conditional Rendering Test**

T42 should specify when sections are rendered, omitted, marked unresolved, or escalated for human decision, and should test whether generation rules prevent unsupported content from filling template slots.

## 11. Boundary

This is a project-level semantic mapping test. It does not claim that the template architecture is an established academic standard.

Human remains final epistemic decision authority.
