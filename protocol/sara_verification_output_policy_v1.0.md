# SARA Verification Output Policy v1.0

> Co-thoughts v2.0의 SARA 검증 결과를 대화형 출력에 적용하기 위한 출력·노출 정책.

## 1. Purpose

SARA 검증은 답변의 마지막에 부가적으로 붙는 사후 평가가 아니라, Claim/Evidence/Reasoning의 검증과 필요 시 Revision/Re-verification을 포함하는 품질관리 루프의 일부로 동작한다.

SARA는 별도의 사용자-facing 검증 체계를 하나 더 만드는 것이 아니라, 프로젝트의 기존 검증 출력이 의미 있게 동작하도록 하는 **검증 엔진 / 검증 레이어**다.

검증의 깊이와 사용자에게 노출되는 정보량은 분리한다.

> **Always-on verification, progressive disclosure.**

## 2. Core Principle

- 검증은 필요한 범위에서 수행한다.
- 사용자-facing 기본 검증 출력은 기존 프로젝트의 `☑️ 검증 결과`를 canonical summary로 사용한다.
- SARA는 `☑️ 검증 결과`의 내부 검증 로직과 상태를 담당한다.
- 별도의 `🛡️ SARA Verification` 섹션을 기본 출력에 병렬로 추가하지 않는다.
- 상세 검증은 사용자가 요청하거나 중요한 검증 문제가 발견된 경우 제공한다.
- 검증 상태는 Evidence와 분리하여 관리한다.
- Agreement는 Verification을 상승시키지 않는다.
- Human Agency를 보존한다.
- 내부 추론 과정(chain-of-thought)은 출력하지 않는다. 대신 Claim → Evidence → Verification → Revision의 감사 가능한 요약을 제공한다.

## 3. Integrated Default Output

일반적인 답변에서는 SARA 결과를 별도 섹션으로 중복 표시하지 않고 기존 `☑️ 검증 결과`에 통합한다.

권장 기본 형태:

~~~text
☑️ 검증 결과 — SARA Summary
상태: 🟢 양호
핵심 주장 N · 근거 연결 M/N · 주요 문제 0
불확실성: 낮음
상세 검증 보기 ▸
~~~

조건부 검증:

~~~text
☑️ 검증 결과 — SARA Summary
상태: 🟡 조건부 검증
핵심 주장 N · 근거 연결 M/N
⚠️ 주의 필요 K
불확실성: 중간
상세 검증 보기 ▸
~~~

검증 필요:

~~~text
☑️ 검증 결과 — SARA Summary
상태: 🔴 검증 필요
핵심 주장 N · 미검증 K
⚠️ 근거보다 강한 주장 또는 핵심 근거 부족
상세 검증 보기 ▸
~~~

정상적인 저위험 답변에서는 검증 UI가 대화의 흐름을 방해하지 않도록 최소화한다.

기존 프로젝트의 별도 메타평가 항목이 존재하는 경우, 해당 항목은 SARA Verification Summary와 혼합하지 않고 **메타평가 / 실행 안정성 정보**로 구분한다. 특히 통계적 의미가 없는 Accuracy / Recall / Confidence 등의 값을 SARA의 검증 정확도로 해석하지 않는다.

## 4. Progressive Disclosure

### Level 0 — Inline Summary

답변에 필요한 경우 기존 `☑️ 검증 결과` 안에서 다음 상태를 짧게 표시한다.

- Verified / 양호
- Conditionally Verified / 조건부 검증
- Verification Required / 검증 필요

### Level 1 — Verification Summary

사용자가 상세 검증을 요청하거나 요약을 확장하면:

- Claim 수
- Evidence-linked Claim 수
- Verification Coverage
- 주요 문제 수
- Uncertainty 수준
- Human Judgment Required 여부

를 제공한다.

### Level 2 — Full Audit

사용자가 추가로 요청한 경우 다음을 제공할 수 있다.

- Claim별 상태
- Evidence mapping
- Evidence의 직접/간접 지지 여부
- Reasoning integrity 점검
- Uncertainty 및 미해결 항목
- Revision 및 Re-verification 결과
- Provenance / Audit Trail

## 5. Verification Loop

검증은 다음 상태 전이를 따른다.

~~~text
Claim Identification
→ Evidence Alignment
→ Verification
→ Issue Detection
→ Revision (필요 시)
→ Re-verification
→ Epistemic State Update
→ Integrated Output (☑️ 검증 결과)
~~~

검증 결과에 문제가 없으면 불필요한 Revision을 수행하지 않는다.

## 6. Epistemic Classification

검증 결과는 다음 축을 혼동하지 않는다.

### Epistemic Type

FACT / INTERPRETATION / INFERENCE / HYPOTHESIS / SIMULATION

### Verification State

VERIFIED / PARTIALLY VERIFIED / UNVERIFIED / CONTRADICTED

### Attribution

AUTHOR_EXPLICIT / AUTHOR_SUPPORTED / SOURCE_INFERRED / MODERN_INTERPRETATION / SPECULATIVE / UNKNOWN

### Temporal

HISTORICAL / POST_PUBLICATION / CONTEMPORARY

## 7. Metrics

기존의 정성적 메타평가를 통계적 성능지표처럼 표현하지 않는다.

권장 SARA 검증 지표:

- **Evidence Coverage**: 주요 Claim 중 Evidence가 연결된 비율.
- **Verification Coverage**: 검증 대상으로 식별된 Claim 중 실제 검증된 비율.
- **Inference Ratio**: 전체 Claim 중 해석·추론에 의존하는 Claim의 비율.
- **Replication Stability**: 동일 조건의 반복 실행에서 결과 상태가 유지되는 정도. 통계적 recall로 부르지 않는다.
- **Model Agreement**: 여러 모델의 판단이 일치하는 정도. Truth나 Evidence의 대체물로 취급하지 않는다.

**Accuracy**는 객관적 Ground Truth가 정의되고 비교 가능한 경우에만 통계적 의미로 사용한다.

## 8. Critical Findings

다음과 같은 경우 기본 `☑️ 검증 결과` 요약에서도 경고를 표시한다.

- 핵심 Claim에 Evidence가 없음
- Evidence보다 결론의 강도가 큼
- 중요한 출처 간 충돌
- 핵심 Premise가 취약하거나 미검증
- 중요한 Attribution / Temporal 오류
- 답변의 결론이 Unverified 상태에 과도하게 의존
- Human Judgment가 필수적인 사안을 확정적으로 표현

## 9. Human Judgment Boundary

SARA는 인간의 최종 판단을 대체하지 않는다.

AI가 검증 가능한 사실·근거·논리적 연결을 평가하더라도 다음은 별도로 표시할 수 있다.

- 가치 판단
- 규범적 결론
- 책임 귀속
- 사회적 적용 가능성
- 증거만으로 결정할 수 없는 이론적 해석

## 10. Output Invariant

~~~text
VERIFICATION ≠ AGREEMENT
VERIFICATION ≠ TRUTH
MODEL AGREEMENT ≠ EVIDENCE
STATE ≠ EVIDENCE
CHECKPOINT ≠ EVIDENCE
SUMMARY ≠ FULL AUDIT
SARA ≠ SECONDARY DUPLICATE OUTPUT
~~~

기본 출력이 간결하다는 이유로 중요한 검증 문제를 숨기지 않는다.

## 11. Relationship to v2.0

이 정책은 v2.0의 다음 구조를 확장한다.

- SARA Knowledge Gate / Thought Gate
- Epistemic State
- Provenance
- Non-Monotonic Revision
- Human Agency
- Project Adapter Interface

v2.0의 canonical architecture를 변경하지 않고, SARA 결과를 기존 `☑️ 검증 결과`에 통합하여 사용자에게 노출하는 방식을 정의한다.

## 12. Status

Version: v1.0
Status: PROPOSED / PROJECT INTEGRATION

이 정책은 실제 대화 및 테스트 결과를 통해 검증한 후 다음 버전에서 확정한다.
