# SARA Verification Output Policy v1.0

> SARA 검증 결과를 공동사고 대화에 노출하는 방식에 대한 출력 정책

## 0. Purpose

SARA의 검증은 답변의 마지막에 부착되는 사후 평가가 아니라, Claim/Evidence/Reasoning의 상태를 확인하고 필요하면 Revision과 Re-verification을 유도하는 품질관리 루프의 일부로 취급한다.

단, 검증의 내부 깊이와 사용자에게 기본적으로 노출하는 정보량은 분리한다.

**Core principle**

> **검증은 항상 수행하되, 출력은 최소 충분 정보로 시작하고 상세 Audit은 요청 시 확장한다.**

## 1. Scope

이 정책은 Co-thoughts v2.0의 다음 구조에 적용한다.

- SARA Knowledge Gate
- SARA Thought Gate
- Epistemic State
- Provenance
- Revision / Re-verification
- Project Adapter의 OUTPUT_SCHEMA

이 문서는 SARA 자체의 판정 알고리즘을 정의하지 않는다. SARA가 반환한 검증 상태를 Co-thoughts가 어떻게 표현하고 확장할지를 정의한다.

## 2. Verification Lifecycle

검증은 다음 폐쇄 루프의 일부다.

~~~text
CLAIM / EVIDENCE
      ↓
SARA VERIFICATION
      ↓
ISSUE DETECTION
      ↓
REVISION (필요한 경우)
      ↓
RE-VERIFICATION
      ↓
EPISTEMIC STATE UPDATE
      ↓
OUTPUT
~~~

따라서 Verification은 단순한 최종 점수 산출이 아니다.

## 3. Epistemic Separation

검증 출력은 다음을 혼동하지 않는다.

- EVIDENCE ≠ VERIFICATION
- VERIFICATION ≠ AGREEMENT
- MODEL AGREEMENT ≠ TRUTH
- REPLICATION STABILITY ≠ CORRECTNESS
- STATE ≠ EVIDENCE

또한 FACT / INTERPRETATION / INFERENCE / HYPOTHESIS / SIMULATION의 epistemic class를 유지한다.

## 4. Default Output

일반적인 답변에서는 검증 결과를 핵심 요약만 표시한다.

예:

~~~text
🛡️ SARA Verification
🟢 양호
핵심 주장 8 · 근거 8/8 · 주요 문제 0

[상세 검증 보기]
~~~

기본 출력에는 다음 정보만 포함할 수 있다.

- 최종 Verification State
- 핵심 Claim 수
- Evidence-linked Claim 수
- Critical Issue 수
- 필요한 경우 Unresolved Claim 수

정상적인 답변에는 긴 Claim/Evidence/Audit 내용을 자동으로 노출하지 않는다.

## 5. Verification States

표시 상태는 Epistemic State의 Verification 축을 사용자에게 압축해 표현한다.

| State | UI 의미 |
|---|---|
| 🟢 VERIFIED | 핵심 검증 대상이 충분히 확인됨 |
| 🟢 PARTIALLY VERIFIED | 일부만 확인됨 |
| 🟡 CONDITIONAL | 조건 또는 해석 범위에 따라 성립 |
| 🟡 UNRESOLVED | 현재 근거만으로 판단할 수 없음 |
| 🔴 CONTRADICTED | 반대 근거 또는 충돌이 확인됨 |
| 🔴 UNSUPPORTED | 현재 Evidence로 지지되지 않음 |

CONDITIONAL / UNRESOLVED / UNSUPPORTED를 자동으로 하나의 '오류'로 취급하지 않는다. 이는 서로 다른 epistemic state다.

## 6. Automatic Escalation

사용자가 상세 검증을 요청하지 않았더라도 다음 경우에는 요약 수준의 경고를 표시한다.

- Critical Claim이 UNSUPPORTED인 경우
- 핵심 Claim과 Evidence 사이에 중대한 불일치가 있는 경우
- 결론의 강도가 Evidence보다 현저히 강한 경우
- 중요한 Source Conflict가 존재하는 경우
- Revision 후에도 핵심 문제가 남는 경우

예:

~~~text
🛡️ SARA Verification
🔴 검증 필요
핵심 주장 8 · 미검증 2
⚠️ 근거보다 강한 결론이 1건 발견됨

[상세 검증 보기]
~~~

목적은 사용자를 안심시키는 것이 아니라 중요한 epistemic risk를 놓치지 않게 하는 것이다.

## 7. On-demand Detailed Audit

사용자가 '상세 검증', '검증 과정', '근거 확인' 등을 요청하면 다음 정보를 확장한다.

### 7.1 Claim Analysis
- Claim ID
- Claim 내용
- Epistemic class
- Verification state
- Attribution
- Temporal context

### 7.2 Evidence Mapping
- 연결된 Evidence
- Evidence provenance
- 직접/간접 지지 여부
- Evidence와 Claim 사이의 범위 차이
- Counter-evidence / Source conflict

### 7.3 Reasoning Integrity
- 논리적 비약
- 과잉 일반화
- 인과관계 과잉 해석
- 정의되지 않은 핵심 개념
- Evidence보다 강한 결론
- 자기모순

### 7.4 Uncertainty
- 미확정 영역
- 불확실성 원인
- 경쟁 설명
- 필요한 추가 Evidence

### 7.5 Revision
- 수정 대상 Claim
- 수정 전 상태
- 수정 후 상태
- Re-verification 결과

### 7.6 Human Judgment
- AI 검증으로 결정할 수 없는 문제
- 인간의 최종 판단이 필요한 영역

## 8. Audit Trail

상세 Audit은 내부 사고과정의 원문을 공개하지 않는다.

대신 다음의 검증 가능한 provenance를 제공한다.

~~~text
CLAIM
  ↓
EVIDENCE
  ↓
VERIFICATION FINDING
  ↓
REVISION
  ↓
RE-VERIFICATION
  ↓
FINAL STATE
~~~

Audit trail은 무엇을 근거로 어떤 검증 상태가 부여되었는지를 추적할 수 있어야 한다.

## 9. Metrics

기존의 '정확도 / 재현율 / 신뢰도'를 근거 없이 임의의 확률값으로 표시하지 않는다.

필요한 경우 다음과 같이 정의된 측정값을 사용한다.

- **Evidence Coverage**: 검증 대상 핵심 Claim 중 Evidence가 연결된 비율
- **Verification Coverage**: 검증 대상으로 식별된 Claim 중 실제 검증이 수행된 비율
- **Inference Ratio**: 전체 Claim 중 Interpretation / Inference 등 모델 추론에 의존하는 Claim의 비율
- **Replication Stability**: 동일한 검증 조건을 반복 적용했을 때 상태가 유지되는 정도
- **Model Agreement**: 복수 모델의 판단 일치 정도

Model Agreement는 Truth의 대리 지표가 아니다.
Replication Stability는 Correctness의 대리 지표가 아니다.

Ground Truth가 존재하고 적절한 평가셋이 있는 경우에만 통계적 Accuracy / Precision / Recall 등의 표준 지표를 별도로 사용한다.

## 10. Output Levels

### Level 0 — Inline Summary
모든 일반 답변에서 최소 상태만 표시한다.

### Level 1 — Verification Summary
사용자가 검증 결과를 요청하면 핵심 Claim/Evidence/Issue 요약을 제공한다.

### Level 2 — Full Audit
사용자가 상세 검증을 요청하거나 연구·분석 맥락에서 요구하는 경우 Claim/Evidence/Reasoning/Uncertainty/Revision/Provenance를 확장한다.

## 11. Human Agency

SARA의 검증 결과는 인간의 최종 판단을 대체하지 않는다.

특히 다음은 별도 Human Judgment 영역으로 남길 수 있다.

- 규범적 판단
- 가치 판단
- 정책적 선택
- 책임 귀속
- 정의의 선택
- 증거가 부족한 미래 예측

## 12. Integration with Co-thoughts v2.0

이 정책은 다음 v2.0 구조와 연결된다.

~~~text
COGNITIVE ROUTER
      ↓
VERIFY
      ↓
SARA DUAL GATE
      ↓
REVISION / RE-VERIFICATION
      ↓
EPISTEMIC STATE
      ↓
CHECKPOINT
      ↓
OUTPUT
      ├─ default: summary
      └─ requested: detailed audit
~~~

검증 출력의 상세도는 Cognitive Operation의 강도와 별개다.

**DEEP verification ≠ verbose default output**

## 13. Non-goals

이 정책은 다음을 목표로 하지 않는다.

- Chain-of-Thought 공개
- 검증 상태를 단일 확률값으로 환원
- 모델 간 합의를 진실성의 증거로 사용
- 모든 답변에 장문의 검증 보고서 자동 첨부
- Human Judgment를 자동 판정으로 대체

## 14. Status

**Policy:** SARA Verification Output Policy v1.0
**Applies to:** Co-thoughts v2.0
**Status:** ACTIVE POLICY EXTENSION
