# 적응형 설명 형식 라우터 연동 설계 v0.1

> 상태: PARTIALLY IMPLEMENTED / PR #2 OPEN (CI: PR #2 체크 참조)
> 대상: co-thoughts v2.0 Cognitive Router 및 Adaptive Explanation Format Protocol v0.1
> 범위: 인지 작업 계획에서 사용자에게 제시할 설명 형식 계획을 분리·연결하는 인터페이스 설계

## 1. 목적

Cognitive Router가 선택한 인지 연산과 작업 맥락을 입력으로 받아, Adaptive Explanation Format Protocol에 따라 적합한 설명 형식의 잠정 계획을 생성한다.

이 기능은 **무엇을 사고할지**와 **그 결과를 어떻게 설명할지**를 분리한다. 설명 형식 선택은 인지 연산, 근거의 품질, 검증 상태 또는 결론의 진위를 변경하지 않는다.

## 2. 현행 구현과 설계 경계

현재 확인된 구현은 다음과 같다.

- `CognitiveRouter.route()`는 FAST/MIXED/DEEP 모드와 인지 연산을 선택한다.
- `route_verification_domains()`는 키워드 기반 검증 분야 힌트를 제공한다. 의미 이해, 주장 자동 추출 또는 검증을 수행하지 않는다.
- `route_workflow_natural_language()`는 지정된 문제 해결 워크플로우를 선택한다.
- `CognitiveRuntime`은 백엔드 응답을 검증하고 인식론적 상태 승격을 차단한다.
- Adaptive Explanation Format Protocol v0.1은 설계 지침이며 런타임 매체 선택기는 아니다.

현재 구현에서는 별도 규칙 기반 planner와 Cognitive Router 연결이 추가되었다. 실제 렌더링, 매체 생성, 사용자 인터페이스 통합은 완료되지 않았다. 구현은 PR #2에서 검토 중이다. CI 상태는 PR #2의 GitHub Actions 체크에서 확인하며, 커밋 추가 시 문서가 낡지 않도록 본 문서에는 기록하지 않는다.

## 3. 권장 아키텍처

```text
REQUEST
  |
  v
COGNITIVE ROUTER
  |-- mode / operations / reasons
  |-- workflow routing
  |-- verification-domain hints
  |
  +------------------------------+
  |                              |
  v                              v
COGNITIVE PLAN             EXPLANATION FORMAT ROUTER
                                  ^
                                  |
                         task + context + output intent
                                  |
                                  v
                         FORMAT PLAN (provisional)
                                  |
                                  v
                         PROJECT ADAPTER / HOST
                                  |
                                  v
                         TEXT / DIAGRAM / IMAGE /
                         INTERACTIVE / VIDEO / SIMULATION
```

설명 형식 라우터는 Cognitive Router의 하위 인지 연산이 아니다. 두 계획은 동일 요청을 바탕으로 병렬 산출되며, 최종 출력 단계에서 결합한다.

## 4. 모듈 책임

### 4.1 Cognitive Router

- 현재 작업의 모드와 인지 연산을 선택한다.
- 선택 이유와 기존 워크플로우·검증 분야 라우팅 결과를 보존한다.
- 설명 형식 선택을 이유로 인지 연산을 추가하거나 제거하지 않는다.

### 4.2 Explanation Format Router (구현됨: 규칙 기반 planner)

- v0.1 구현은 명시적 매체 요청, 제한된 작업 키워드, 사전에 정의된 불리언 context 신호, 호스트 capability 선언을 평가한다.
- 사용자 숙련도·세부 수준·위험도·데이터 품질을 의미적으로 평가하지 않는다. 해당 기능은 후속 평가 및 개선 대상이다.
- 가장 낮은 복잡도로 목적을 달성하는 기본 형식을 선택한다.
- 필요할 때만 보조 형식을 추가한다.
- 지원되지 않거나 실행 능력이 확인되지 않은 형식은 생성 완료로 표시하지 않는다.
- 선택 이유, 배제 이유, 가정, 불확실성 및 대체 형식을 반환한다.

### 4.3 Project Adapter / Host

- 프로젝트별 `OUTPUT_SCHEMA`, 도메인 규칙, 사용자 요청 및 플랫폼 능력을 적용한다.
- 실제 렌더러·이미지·영상·웹 실행 기능을 호출할 수 있는지 확인한다.
- 생성, 렌더링, 기능 시험, 출처 검증 상태를 별도로 기록한다.

## 5. 입력 계약 (구현 기준)

```python
{
    "task": str,                       # required
    "mode": "FAST" | "MIXED" | "DEEP",
    "operations": list[str],           # Cognitive Router output
    "context": Mapping[str, Any],
    "output_intent": {
        "requested_format": str | None,
        "audience": str | None,      # reserved; not used by planner v0.1
        "detail_level": str | None   # reserved; not used by planner v0.1
    },
    "capabilities": {
        "text": bool,
        "diagram": bool,
        "image": bool,
        "interactive": bool,
        "animation": bool,
        "video": bool,
        "simulation": bool
    }
}
```

필수 입력은 작업(task)이다. 누락된 선택 입력은 임의로 사실처럼 채우지 않고 기본값 또는 UNKNOWN으로 처리한다. 사용자 지정 매체가 지원되지 않으면 제한을 알리고 대안을 제시한다.

## 6. 출력 계약 (구현 기준)

```python
{
    "format_plan": {
        "primary": "TEXT",
        "secondary": [],
        "rationale": [],
        "excluded_formats": [],
        "assumptions": [],
        "uncertainties": [],
        "fallback": "TEXT",
        "selection_status": "SELECTED"
    },
    "capability_status": {
        "requested": [],
        "available": [],
        "unavailable": []
    },
    "execution_status": "NOT_RUN",
    "render_status": "NOT_RUN",
    "functional_test_status": "NOT_RUN",
    "verification_status": "UNVERIFIED",
    "is_evidence": False
}
```

형식 식별자: TEXT, DIAGRAM, IMAGE, INTERACTIVE, ANIMATION, VIDEO, SIMULATION. 구현은 비텍스트 기능을 호스트가 명시적으로 선언한 경우에만 사용 가능하다고 취급한다. 기능 맵이 없으면 TEXT만 사용 가능하다고 가정한다.

## 7. 선택 규칙

| 조건 | 기본 형식 | 보조 형식 |
|---|---|---|
| 정의·짧은 설명·정밀 조건 | TEXT | 표 |
| 정적 구성·관계 | TEXT 또는 DIAGRAM | 설명 문장 |
| 절차·분기·상태 전이 | DIAGRAM | 단계별 텍스트 |
| 주장·근거·경쟁 가설 비교 | TEXT + DIAGRAM | 근거 표 |
| 공간·외관·형태 | TEXT + IMAGE | 주석 도해 |
| 시간에 따른 동작 | TEXT + ANIMATION/VIDEO | 대본 |
| 변수 조작·조건별 탐색 | TEXT + INTERACTIVE | 정적 결과표 |
| 가정 기반 결과 비교 | TEXT + SIMULATION | 민감도 표 |

선택 우선순위:

1. 사용자가 명시한 출력 형식과 접근성 요구
2. 프로젝트 어댑터의 출력 스키마와 도메인 제약
3. 과제에 필요한 정보 구조
4. 호스트에서 실제 사용할 수 있는 기능
5. 제작 비용과 복잡도

단순 질의는 TEXT를 기본으로 한다. 시각 자료가 이해나 판단에 실질적인 이득을 주지 않으면 추가하지 않는다.

## 8. 핵심 불변식 및 안전장치

1. **Format ≠ Cognition:** 설명 형식은 인지 연산을 대체하지 않는다.
2. **Format ≠ Evidence:** 도식·이미지·영상·시뮬레이션은 그 자체로 근거가 아니다.
3. **Rendering ≠ Verification:** 렌더링 성공은 사실 검증 성공이 아니다.
4. **Selection ≠ Generation:** 매체 선택은 매체 생성 완료를 뜻하지 않는다.
5. **Generation ≠ Functional Test:** 파일 생성은 상호작용·작동 검증이 아니다.
6. **Agreement ≠ Evidence:** 사용자 동의나 표현의 설득력은 검증 상태를 올리지 않는다.
7. **Epistemic State Preservation:** FACT/INTERPRETATION/INFERENCE/HYPOTHESIS/SIMULATION 및 VERIFIED/PARTIALLY VERIFIED/UNVERIFIED/CONTRADICTED의 의미를 변경하지 않는다.
8. **Human Agency:** 최종 해석과 결정 권한은 인간에게 있다.
9. **Capability Honesty:** 사용할 수 없는 기능을 사용할 수 있다고 표시하지 않는다.
10. **Progressive Disclosure:** 핵심 결과를 먼저 제시하고 세부 근거와 원자료를 확장 가능하게 한다.

## 9. 오류·대체 동작

- 입력 불충분: TEXT + 명시적 가정 또는 필요한 최소 질문
- 매체 미지원: TEXT fallback 및 미지원 사유
- 렌더링 실패: 선택 결과는 보존하되 render_status=FAILED
- 기능 시험 미실시: functional_test_status=NOT_RUN
- 출처 불명 데이터: 출처 미확인 표시, 시각적 권위 부여 금지
- 고위험 판단: 시각화 단독 결론 금지, 근거·불확실성·전문가 검토 필요성 표시
- 형식 계획 입력 오류(불리언이 아닌 context 신호, 알 수 없거나 불리언이 아닌 capability 키, `text: false`, 미지원 `requested_format`): `route_explanation_format()`은 고정 코드(예: `CAPABILITY_UNKNOWN:<key>`)로 `ValueError`를 발생시킨다. 공개 `cognitive_router.route()`는 이를 전파하지 않고, `format_routing`에 `selection_status=INVALID_INPUT`인 TEXT 계획과 `error` 코드를 담아 반환하므로 인지·검증 라우팅은 영향을 받지 않는다.
- 키워드 힌트: 영문 키워드는 단어 단위로 일치(단순 복수·과거형 접미사 허용), 한국어 키워드는 부분 문자열로 일치하되 알려진 충돌(예: "big picture", "그림자", "영상의학")은 제외 목록으로 처리한다.

## 10. 단계별 구현 계획

### Phase 0 — 설계 기준선
- 설계 계약과 형식 enum 확정
- 입력·출력 스키마 정의
- Cognitive Router 호환성 검토 (완료)

### Phase 1 — 순수 규칙 기반 선택기 (구현됨)
- `src/co_thoughts/explanation_format_router.py`에 결정적 planner 구현
- 사용자 지정 형식, 기본 텍스트, capability fallback 처리
- 선택 이유, 가정, 불확실성 및 상태 반환
- 비텍스트 생성·렌더링은 수행하지 않음

### Phase 2 — Cognitive Router 연결 (구현됨, PR 검토 중)
- `route()` 출력에 `format_routing` 추가
- 기존 `operations`, `verification_routing`, `workflow_routing`의 의미를 보존하도록 통합
- 단위·통합 회귀 테스트 추가
- CI: PR #2 체크 참조

### Phase 3 — Host/Adapter 렌더링 연결
- 실제 사용 가능한 렌더러만 연결
- 생성·렌더링·기능 시험·출처 검증을 분리 기록
- 실패 시 텍스트 대체 경로 검증

### Phase 4 — 평가 및 승격
- 대표 작업군별 선택 정확성·불필요한 매체 생성·fallback·접근성 평가
- 독립 테스트와 회귀 테스트 통과 후에만 구현 상태 승격

## 11. 최소 테스트 기준

- 단순 번역·정의·계산은 TEXT를 선택한다.
- 구성 요소 관계 설명은 DIAGRAM을 후보로 선택한다.
- 시간적 동작 설명은 사용 가능 기능에 따라 ANIMATION/VIDEO 또는 TEXT fallback을 선택한다.
- 변수 조작이 불가능한 환경에서는 INTERACTIVE를 선택 완료로 표시하지 않는다.
- 사용자 지정 형식과 프로젝트 출력 스키마가 충돌하면 충돌을 보고하고 임의로 스키마를 덮어쓰지 않는다.
- format routing이 verification_status를 승격하지 않는다.
- format routing 결과가 기존 인지 연산·검증 라우팅 결과를 변경하지 않는다.
- 선택, 생성, 렌더링, 기능 시험 상태를 독립적으로 검증한다.

## 12. 현재 상태 선언

- 설계 문서: 작성 및 구현 상태 갱신
- 신규 format planner: 구현됨 (feature branch)
- Cognitive Router 연결: 구현됨 (feature branch)
- 단위·통합 테스트: 추가됨. CI 상태는 PR #2의 GitHub Actions 체크에서 확인하며, 커밋 추가 시 문서가 낡지 않도록 본 문서에는 기록하지 않는다.
- 렌더러 연결: 미구현; 현재 조사 범위에서 사용 가능한 host renderer 확인 안 됨
- 매체 생성·렌더링·기능 시험: 미실행
- 독립 검증: 미실시

PR #2가 병합되기 전까지 main 브랜치에 반영된 것으로 간주하지 않는다. CI 및 독립 검토가 끝나기 전까지 구현은 부분 검증 상태다.
