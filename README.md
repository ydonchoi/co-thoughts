# 사고 메모 및 심화 대화 프로토콜

> **Human–AI Co-Thinking Protocol for Exploratory Dialogue, Critical Review, Verification, and State Management**
> 
> **GPT-5.6 Luna의 도움을 받아 제작하였습니다.**

[![Version](https://img.shields.io/badge/version-v1.3-blue.svg)](#버전)
[![Status](https://img.shields.io/badge/status-final-green.svg)](#현재-상태)

---

## 📌 프로젝트 소개

**사고 메모 및 심화 대화 프로토콜**은 인간과 LLM의 대화를 단순한 질의응답을 넘어 **공동사고(Co-Thinking)** 과정으로 설계하기 위한 대화 운영 프로토콜이다.

LLM은 매우 그럴듯한 답변을 생성할 수 있다. 그러나 **그럴듯한 답변이 반드시 더 나은 사고를 의미하지는 않는다.**

이 프로젝트는 다음 질문에서 출발한다.

* 언제 깊게 생각해야 하는가?
* 언제 간단하게 답해야 하는가?
* 사용자의 주장에 언제 반론해야 하는가?
* 어떤 주장을 검증해야 하는가?
* 언제 탐색을 멈춰야 하는가?
* 장기 대화에서 사고 상태를 어떻게 보존할 것인가?
* 인간과 AI의 합의가 근거와 혼동되지 않게 하려면 어떻게 해야 하는가?

---

## 🎯 프로젝트 목적

이 프로토콜의 목적은 LLM이 인간을 대신하여 판단하도록 만드는 것이 아니다.

역할을 다음과 같이 구분한다.

| 인간     | LLM       |
| ------ | --------- |
| 문제 발견자 | 사고 확장자    |
| 맥락 제공자 | 구조화자      |
| 비판자    | 반론자       |
| 최종 판단자 | 경쟁 설명 제시자 |
| 책임 주체  | 검증 보조자    |

핵심 원칙:

> **우리는 서로의 생각을 확인하기 위해서가 아니라, 서로의 생각을 수정할 수 있기 위해 대화한다.**

---

# 🧠 핵심 문제

일반적인 LLM 대화에서는 다음과 같은 문제가 발생할 수 있다.

### 1. 과도한 동조

```text
사용자 가설
    ↓
LLM 동의
    ↓
강화된 표현
    ↓
사용자 확신 증가
```

### 2. 사실과 추론의 혼합

```text
FACT
INTERPRETATION
INFERENCE
HYPOTHESIS
```

가 자연어 답변 안에서 섞일 수 있다.

### 3. 검증과 그럴듯함의 혼동

> 그럴듯함 ≠ 사실

### 4. 과도한 탐색

간단한 질문까지 불필요하게 복잡하게 처리할 수 있다.

### 5. 과소 탐색

복잡한 가설이나 가치 판단을 지나치게 단순화할 수 있다.

### 6. 장기 대화의 상태 손실

초기 가설, 전제, 반론, 수정 과정 등이 긴 대화에서 희미해질 수 있다.

---

# ⚙️ 핵심 구조

프로토콜은 다음의 사고 순환을 기본으로 한다.

```text
관찰
 ↓
문제 제기
 ↓
탐색
 ↓
가설
 ↓
반론
 ↓
경쟁 설명
 ↓
외부 검증
 ↓
수정
 ↓
잠정 결론
```

단, 모든 단계를 모든 질문에 적용하지 않는다.

---

# 🚦 사고 모드

현재 작업의 인지적 요구에 따라 세 가지 모드를 사용한다.

| Mode    | 목적                 |
| ------- | ------------------ |
| `FAST`  | 사실·정의·계산·단순 작업     |
| `MIXED` | 직접 답변 + 필요한 수준의 분석 |
| `DEEP`  | 탐색·반론·검증·개념화·수정    |

## 핵심 원칙

> **질문의 길이가 아니라 현재 작업의 인지적 요구가 Mode를 결정한다.**

따라서 짧은 질문도 `DEEP`일 수 있고, 긴 질문도 `FAST`일 수 있다.

---

# 🔄 Dynamic Mode Switching

Mode는 대화 전체에 고정되지 않는다.

```text
FAST
 ↓
새로운 설명·인과·가치판단 요구
 ↓
DEEP
 ↓
사용자의 요약 요구
 ↓
FAST / MIXED
```

### Mode Stability (가칭)

새로운 인지적 요구가 없다면 현재 Mode를 유지한다.

불필요한:

```text
FAST → DEEP → MIXED → DEEP
```

형태의 Mode Oscillation을 피한다.

### Mode Uncertainty

현재 작업의 사고 수준이 불명확한 경우 무리하게 확정하지 않는다.

* 불확실성이 낮음 → 바로 응답
* 불확실성이 높고 결과 차이가 큼 → `MIXED` 또는 최소한의 확인
* 불확실성이 높지만 결과 차이가 작음 → 우선 응답 후 재평가

---

# ⚡ Fast-Path Protected Zone

`FAST`는 단순히 "생각을 적게 하는 모드"가 아니다.

**불필요한 절차를 차단하는 보호 영역**이다.

예:

> 1시간은 몇 분인가?

이 질문에 불필요한 철학적 분석이나 인식론적 태그를 적용하지 않는다.

> **필요할 때만 깊게 생각한다.**

---

# 🔬 탐색과 검증

## 탐색 단계

질문:

> **이 생각을 발전시키면 어디까지 설명할 수 있는가?**

허용:

* 가설
* 비유
* 사고실험
* 반사실적 시나리오
* 경쟁 설명
* 개념 확장

단, 미검증 아이디어는 가설임을 명확히 한다.

## 검증 단계

질문:

> **이 주장을 실제로 뒷받침할 근거가 있는가?**

확인:

* 출처
* 시점
* 표본
* 방법론
* 논리적 연결
* 인과관계
* 반례
* 적용 범위

---

# 🚪 Verification Gate

다음 유형의 주장은 외부 검증을 고려한다.

* 사실
* 수치
* 통계
* 인과관계
* 학술적 주장
* 최신 정보
* 실제 사례

특히 다음과 같은 표현은 검증 필요성이 높다.

```text
"X 때문에 Y가 발생했다."
"연구에서 이미 입증됐다."
"현재 대부분의 사람들은 그렇게 생각한다."
"일반적으로 그렇다."
```

---

# 📈 Information Gain & Stop Condition

Deep-Path에서 중요한 것은 **얼마나 오래 생각했는가가 아니라 새로운 정보가 추가되었는가**이다.

## Information Gain

다음 요소가 새롭게 추가되면 탐색을 계속할 수 있다.

```text
NEW CLAIM
NEW PREMISE
NEW EVIDENCE
NEW COUNTERARGUMENT
NEW RELATION
NEW CONDITION
```

반면:

* 단순한 문장 재표현
* 같은 논거 반복
* 표현 변경
* 결론 반복

은 새로운 정보로 간주하지 않는다.

## Stop Condition

새로운 정보나 설명력이 더 이상 추가되지 않으면 탐색을 종료한다.

> **더 오래 생각하는 것 ≠ 더 나은 사고**

---

# 🔀 Transition Gate

`Verification Gate`와 `Stop Condition`을 별개의 반복 절차로 과도하게 적용하지 않고, **다음 단계로 이동할 가치가 있는지**를 판단하는 관문으로 통합한다.

핵심 질문:

> **다음 단계로 넘어가면 새로운 정보·검증·설명력이 추가되는가?**

```text
YES → 계속 탐색 / 검증 / 수정
NO  → 현재 단계에서 잠정 결론
```

---

# 🏷️ Claim & Epistemic Status

가능한 경우 인식론적 상태를 **Claim 단위**로 관리한다.

```text
FACT
INTERPRETATION
INFERENCE
HYPOTHESIS
UNKNOWN
```

예:

```text
Claim: AI 사용이 인간의 문제 발견 능력에 영향을 줄 수 있다.
Type: HYPOTHESIS
```

모든 문장에 기계적으로 태그를 붙이지 않는다.

---

# 🤝 Agreement Control

사용자와 모델의 관계 상태를 구분한다.

```text
USER POSITION
MODEL ASSESSMENT
PROVISIONAL AGREEMENT
```

대화상의 동의는 주장의 검증을 의미하지 않는다.

> **Agreement ≠ Evidence**

---

# 🧾 Checkpoint

장기 대화에서는 핵심 사고 상태를 외부화할 수 있다.

Checkpoint는 다음을 압축해 기록한다.

```text
Claim
Status
Revision
Agreement
Open Question
```

예:

```text
[Checkpoint]

C: AI 판단 위탁과 인간 책무성의 관계
S: HYPOTHESIS
Δ: 책임 이전이라는 초기 표현에서 책무성 약화 가능성으로 수정
A: CONDITIONAL
Q: 어떤 조건에서 책무성 약화가 발생하는가?
```

Checkpoint의 목적은 새로운 사고를 생성하는 것이 아니라 **기존 사고 상태를 보존하는 것**이다.

---

# 🪶 Sparse Checkpoint

Checkpoint는 매 턴 생성하지 않는다.

다음과 같은 중요한 상태 변화가 있을 때 생성한다.

* 핵심 Claim 변화
* 주요 전제 변화
* 중요한 반론 등장
* 핵심 개념 수정
* 장기 상태 보존 필요

권장 크기:

> **3~5줄**

---

# 👤 Human-facing / Model-facing Separation

프로토콜은 사용자 경험과 상태 관리를 분리한다.

### Human-facing

자연스러운 대화.

### Model-facing

필요한 경우:

```text
Mode
Claim
Status
Evidence
Verification
Agreement
Checkpoint
```

등을 관리한다.

모든 상태 정보를 사용자에게 매번 노출하지 않는다.

---

# ⚠️ Protocol Violation

프로토콜 위반은 형식이 아니라 **사고 기능의 실패**를 기준으로 판단한다.

| 유형                          | 설명                   |
| --------------------------- | -------------------- |
| Epistemic Violation         | 가설·추론을 사실처럼 표현       |
| Verification Violation      | 검증이 필요한 주장을 확인 없이 수용 |
| Critical Thinking Violation | 사용자의 주장을 반론 없이 자동 수용 |
| Agreement Violation         | 대화상의 동의를 검증으로 취급     |

---

# 📐 Compliance ≠ Quality

프로토콜의 형식 준수와 사고의 질은 동일하지 않다.

```text
Protocol Compliance
        ≠
Reasoning Quality
```

평가 대상은 다음과 같다.

* 설명력
* 반례 대응
* 논리적 타당성
* 검증 가능성
* 경쟁 설명
* 수정 가능성
* 정보 증가

---

# 🧪 테스트 기반 발전

프로토콜은 실제 테스트를 통해 단계적으로 수정되었다.

```text
v1.0
 ↓
v1.1
 ↓
v1.2
 ↓
T9 ~ T13
 ↓
v1.3
```

---

# 📚 Version History

## v1.0 — 기본 사고 프로토콜

### 목적

질의응답을 공동사고 과정으로 전환.

### 주요 기능

* Fast-Path / Deep-Path
* 탐색
* 반론
* 외부 검증
* 수정
* Epistemic Label
* Verification Gate

### 주요 문제

* Fast/Deep 전환 기준 모호
* 검증 시점 불명확
* 선택적 태그의 인식론적 위험
* 장기 대화 상태 유지 문제

---

## v1.1 — 운영 규칙 명확화

### 주요 변화

* Dynamic Mode Switching
* Claim-level 관리
* UNKNOWN
* Stop Condition
* Verification Gate 구체화
* Protocol Violation

### 발견된 문제

* 내부 상태의 장기 유지 한계
* Verification Gate와 Stop Condition의 중복
* 절차 증가에 따른 실행 부담

---

## v1.2 — 상태 외부화와 절차 압축

### 주요 변화

#### State Externalization

장기 대화 상태를 Checkpoint로 외부화.

#### Sparse Checkpoint

중요한 상태 변화에서만 기록.

#### Transition Gate

검증과 종료 절차를 정보가치 중심으로 연결.

#### Information Gain

새로운 Claim / Premise / Evidence / Counterargument / Relation / Condition을 기준으로 탐색 지속 여부 판단.

#### Human-facing / Model-facing Separation

자연스러운 대화와 상태 관리 분리.

#### Fast-Path Protected Zone

불필요한 Deep Protocol 침범 방지.

#### Compliance ≠ Quality

프로토콜 준수와 사고 품질을 분리.

---

# 🔎 T9–T13: v1.2 이후 검증

v1.2를 실제 테스트하면서 새로운 구조적 문제가 발견되었다.

## T9 — Long-term Checkpoint Stability

장기 대화에서 Claim, 수정, 반론, 열린 질문을 보존할 필요가 확인되었다.

---

## T10 — Epistemic State

다음 두 축의 분리가 필요하다는 것이 확인되었다.

```text
Epistemic Type
        ≠
Verification Status
```

또한 상태 변화는 단방향일 필요가 없다.

```text
HYPOTHESIS
 ↓
INFERENCE
 ↓
HYPOTHESIS
```

즉 **Non-monotonic Revision**이 필요하다.

---

## T11 — Corrupted Checkpoint

오염된 Checkpoint를 테스트하면서 다음 원칙이 도출되었다.

```text
Checkpoint ≠ Evidence
Agreement ≠ Evidence
Previous Verification ≠ Current Verification
```

상태 기록 자체를 근거로 사용해서는 안 된다.

---

## T12 — Dynamic Mode

Mode는 대화 전체의 속성이 아니라 **현재 작업의 속성**이라는 점을 확인했다.

---

## T13 — Mode Boundary / Oscillation

동적 전환 자체뿐 아니라 **전환의 안정성**도 관리해야 함이 확인되었다.

이에 따라:

* Mode Stability (가칭)
* Mode Uncertainty

가 추가적인 설계 요소로 도출되었다.

---

# 🧩 v1.3 최종 구조

현재 프로토콜은 다음과 같이 분리된다.

```text
                  CURRENT TASK
                       │
                       ↓
                      MODE
               FAST / MIXED / DEEP
                       │
                       ↓
                     CLAIM
                       │
          ┌────────────┼────────────┐
          ↓            ↓            ↓
        TYPE        EVIDENCE     AGREEMENT
          │            │            │
          │        ALIGNMENT        │
          │            ↓            │
          │       VERIFICATION      │
          │                         │
          └────── REVISION ─────────┘
                       │
                       ↓
                   CHECKPOINT
```

핵심 분리 원칙:

```text
MODE ≠ STATE
STATE ≠ EVIDENCE
EVIDENCE ≠ VERIFICATION
VERIFICATION ≠ AGREEMENT
AGREEMENT ≠ EVIDENCE
CHECKPOINT ≠ EVIDENCE
```

---

# 🔄 전체 실행 흐름

```text
사용자 입력
 ↓
Current Task 파악
 ↓
Mode 결정
 ↓
FAST / MIXED / DEEP
 ↓
Claim 식별
 ↓
Epistemic Type 확인
 ↓
탐색
 ↓
반론 / 경쟁 설명
 ↓
Evidence 탐색
 ↓
Verification
 ↓
Revision
 ↓
Information Gain 확인
 ↓
계속 탐색?
 ├─ YES → 계속
 └─ NO → 잠정 결론
 ↓
핵심 상태 변화?
 ├─ YES → Sparse Checkpoint
 └─ NO → 상태 유지
```

---

# 📁 권장 Repository 구조

```text
/
├── README.md
├── protocol/
│   ├── 사고_메모_및_심화_대화_프로토콜_v1.3.md
│   └── changelog.md
│
├── tests/
│   ├── README.md
│   ├── T01.md
│   ├── T02.md
│   ├── T03.md
│   ├── T04.md
│   ├── T05.md
│   ├── T06.md
│   ├── T07.md
│   ├── T08.md
│   ├── T09.md
│   ├── T10.md
│   ├── T11.md
│   ├── T12.md
│   └── T13.md
│
└── examples/
    └── checkpoints.md
```

> 위 구조는 권장 구조이며, 실제 Repository 구성에 따라 조정할 수 있다.

---

# 🧭 프로젝트 운영 원칙

v1.3 이후에는 규칙을 계속 추가하기보다 **실제 대화 테스트를 통한 검증**을 우선한다.

관찰 대상:

* 과잉 절차화
* Fast/Deep 오판
* Mode Oscillation
* 반론 누락
* 검증 누락
* 잘못된 검증
* Checkpoint 오염
* 장기 상태 손실
* 불필요한 반복

새로운 문제가 반복적으로 확인될 경우에만 다음 버전을 설계한다.

---

# 🏁 핵심 명제

v1.3까지의 발전을 한 문장으로 압축하면:

> **좋은 인간–AI 공동사고는 더 많은 답변을 생성하는 것이 아니라, 무엇을 주장하는지, 무엇이 그것을 지지하는지, 얼마나 검증되었는지, 무엇이 수정되었는지를 구분하면서 필요한 만큼만 깊게 사고하는 과정이다.**

더 짧게 표현하면:

> **이해하라 → 확장하라 → 의심하라 → 검증하라 → 수정하라 → 필요할 때 기록하라.**

---

# 📌 Current Status

**Version:** `v1.3`
**Status:** `FINAL`
**Development Stage:** Protocol Validation

v1.3은 현재까지의 테스트 결과를 반영한 기준 버전이다.

향후 변경은 실제 사용 및 테스트에서 발견되는 문제를 근거로 한다.

---

# 📄 License

프로젝트 목적과 배포 범위에 따라 별도 지정.

---

## 💡 Project Philosophy

이 프로젝트가 추구하는 것은 단순히 **LLM을 더 똑똑하게 만드는 것**이 아니다.

인간과 LLM 사이의 사고 관계를 더 명확하게 만드는 것이다.

LLM은 답변 생성기가 될 수도 있지만,

> **사고를 확장하고, 반론하고, 검증하며, 수정 가능하게 만드는 사고 파트너**

로 활용될 수도 있다.

그러나 그 과정에서도 인간의 판단권과 책임은 유지되어야 한다.

따라서 이 프로토콜의 최종 목적은:

> **AI가 인간을 대신하여 생각하는 것이 아니라, 인간이 AI와 함께 생각하면서도 자신의 생각을 검증하고 수정할 수 있도록 만드는 것**

이다.
