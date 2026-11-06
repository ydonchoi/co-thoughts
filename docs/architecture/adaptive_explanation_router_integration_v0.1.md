# 적응형 설명 형식 라우터 연동 설계 v0.1

> 상태: PARTIALLY IMPLEMENTED — planner·Cognitive Router 연결은 `main` 반영(PR #2–#18, #25–#26), Host/Adapter 인터페이스는 참조 구현(`format_host.py`), DIAGRAM 렌더러(`diagram_renderer.py`, Mermaid flowchart 부분집합 → SVG) 연결, 그 밖의 렌더러는 미연결
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

규칙 기반 planner와 Cognitive Router 연결은 `main`에 반영되었다(PR #2, 이후 개선 #3–#18). 실제 렌더링, 매체 생성, 사용자 인터페이스 통합은 완료되지 않았다. CI 결과는 커밋별 GitHub Actions 기록으로 확인하며, 문서가 낡지 않도록 본 문서에는 특정 커밋의 CI 결과를 기록하지 않는다.

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
        "detail_level": str | None,  # reserved; not used by planner v0.1
        "accessibility": {           # optional; all default False
            "screen_reader": bool,
            "reduced_motion": bool,
            "captions": bool,
            "text_only": bool
        }
    },
    "output_schema": {                 # optional; project adapter constraint
        "allowed_formats": list[str]   # non-empty, must include TEXT
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
        "fallback": None,
        "selection_status": "SELECTED",   # SELECTED | FALLBACK | CONFLICT | INVALID_INPUT
        "conflicts": [],
        "accessibility_requirements": []  # e.g. ["TEXT_ALTERNATIVE", "CAPTIONS"]
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

계획 필드 의미: `fallback`은 `primary` 렌더링 실패 시 사용할 형식이며, `primary`가 이미 TEXT인 경우(FALLBACK·INVALID_INPUT 포함) `None`이다. `excluded_formats`는 검토했으나 선택되지 않은 후보 형식(FALLBACK)이며 그 외에는 `[]`이다. `secondary`는 예약 필드로, v0.1은 단일 primary 형식만 계획하므로 `[]`을 반환한다. 출력 스키마(`output_schema.allowed_formats`)는 프로젝트 어댑터가 선언하는 제약이며, 선언되지 않으면 제약이 없다. 사용자가 명시한 `requested_format`이 스키마에 없으면 스키마를 덮어쓰지 않고 `selection_status=CONFLICT`, TEXT 계획, `excluded_formats=[요청 형식]`을 반환하며, `conflicts`에 `{"type": "REQUESTED_FORMAT_NOT_IN_OUTPUT_SCHEMA", "requested_format", "allowed_formats"}`를 기록한다. 충돌 해결은 사용자나 프로젝트 소유자가 한다. 과제에서 추론한 형식이 스키마에 없으면 충돌이 아니라 `FALLBACK`(TEXT)이다. 스키마가 허용한 형식도 호스트 기능이 없으면 기존처럼 `FALLBACK`이다. 충돌이 없으면 `conflicts`는 `[]`이다.

접근성 입력(`output_intent.accessibility`, §7 우선순위 1)은 스키마보다 먼저 평가한다. `text_only`는 TEXT 외 형식을, `reduced_motion`은 ANIMATION·VIDEO를 제외한다. 사용자가 명시한 형식이 제외되면 요구를 덮어쓰지 않고 `CONFLICT`(TEXT 계획)와 `{"type": "REQUESTED_FORMAT_CONFLICTS_WITH_ACCESSIBILITY", "requested_format", "requirement"}`를 기록하며, 추론한 형식이 제외되면 `FALLBACK`이다. 접근성 충돌과 스키마 충돌이 함께 있으면 `conflicts`에 우선순위 순서(접근성 → 스키마)로 모두 기록한다. `screen_reader`와 `captions`는 형식을 제외하지 않고, 선택된 `primary`에 대해 호스트가 지켜야 할 의무를 `accessibility_requirements`로 반환한다: TEXT가 아닌 `primary`에 `screen_reader`면 `TEXT_ALTERNATIVE`, VIDEO에 `captions`면 `CAPTIONS`. planner는 이 의무를 이행하거나 검증하지 않는다(렌더링·기능 시험은 Phase 3). 고대비·글꼴 크기 등 형식 선택과 무관한 표시 설정은 이 입력에 포함하지 않는다(알 수 없는 키는 오류). context 신호는 고정 우선순위 `simulation_required` > `requires_interaction` > `time_dependent_behavior` > `visual_subject` > `process_or_structure` = `has_competing_hypotheses`로 평가하며, 참인 신호는 과제 키워드보다 우선한다.

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
- 형식 계획 입력 오류(불리언이 아닌 context 신호, 알 수 없거나 불리언이 아닌 capability 키, `text: false`, 미지원 `requested_format`, 잘못된 `output_schema` — 예: `OUTPUT_SCHEMA_INVALID`, `OUTPUT_SCHEMA_UNKNOWN_FIELD:<key>`, `OUTPUT_SCHEMA_ALLOWED_FORMATS_INVALID`, `OUTPUT_SCHEMA_FORMAT_UNSUPPORTED:<format>`, `OUTPUT_SCHEMA_TEXT_REQUIRED`, 잘못된 접근성 입력 — `ACCESSIBILITY_INVALID`, `ACCESSIBILITY_INVALID:<key>`, `ACCESSIBILITY_UNKNOWN:<key>`): `route_explanation_format()`은 고정 코드(예: `CAPABILITY_UNKNOWN:<key>`)로 `ValueError`를 발생시킨다. 공개 `cognitive_router.route()`는 이를 전파하지 않고, `format_routing`에 `selection_status=INVALID_INPUT`인 TEXT 계획과 `error` 코드를 담아 반환하므로 인지·검증 라우팅은 영향을 받지 않는다.
- 공통 요청 필드(`request`는 mapping, `task`는 공백이 아닌 문자열, `context`는 mapping이며 없거나 `None`일 때만 `{}`로 대체)는 Cognitive Router, format planner, runtime `SafetyGate` 모두 `request_validation.validate_routing_request()`로 검증한다. `mode`도 없거나 `None`일 때만 `MIXED`로 대체하고 대소문자를 정규화하며(`normalize_mode()`), runtime은 정규화된 요청을 backend에 전달한다. 따라서 공통 필드 오류는 라우팅 전에 `route()`에서 `REQUEST_MUST_BE_MAPPING` / `TASK_REQUIRED` / `CONTEXT_INVALID`로 발생하며, `INVALID_INPUT`은 형식 전용 필드에만 적용된다.
- 키워드 힌트: 영문 키워드는 단어 단위로 일치(단순 복수·과거형 접미사 허용), 한국어 키워드는 부분 문자열로 일치하되 알려진 충돌(예: "big picture", "draws upon", "그림자", "영상의학")은 활용형까지 처리하는 제외 목록으로 거른다. 키워드는 요청 표현(가까운 요청 동사, "as/in/with a …", 과제 첫머리의 형식 명사, 명령형 동사 키워드, 한국어 `로/으로` 또는 조사+요청 동사)이 있을 때만 비텍스트 형식을 고르며, 형식 단어가 주제로만 쓰이면 TEXT를 유지한다.

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

### Phase 2 — Cognitive Router 연결 (구현됨, `main` 반영)
- `route()` 출력에 `format_routing` 추가
- 기존 `operations`, `verification_routing`, `workflow_routing`의 의미를 보존하도록 통합
- 단위·통합 회귀 테스트 추가
- 공통 요청 검증을 Cognitive Router·format planner·runtime `SafetyGate`·v1.3 execution 요청에 통일(PR #6–#8)

### Phase 3 — Host/Adapter 렌더링 연결 (인터페이스 구현됨, DIAGRAM 렌더러 연결)
- 실제 사용 가능한 렌더러만 연결
- 생성·렌더링·기능 시험·출처 검증을 분리 기록
- 실패 시 텍스트 대체 경로 검증

`src/co_thoughts/format_host.py` (참조 구현, 가짜 렌더러로 단위 테스트):

- `RendererRegistry`: 형식별 렌더러를 명시적으로 등록한다. 기본 연결은 없고, TEXT는 등록 대상이 아니다. 렌더러는 `render(payload) -> {"artifact": …}`를 구현하며, INTERACTIVE·SIMULATION 렌더러는 `functional_test(artifact) -> {"passed": bool}`도 구현해야 전달된다.
- `FormatHost.prepare_request(request)`: 요청의 `capabilities`를 등록된 렌더러로만 다시 쓰고(호출자가 기능을 주장할 수 없음), `output_schema`는 호스트에 설정된 값으로 바꾼다(없으면 제거). 잘못된 스키마는 호스트 생성 시 오류이며, 스키마는 생성 시점의 불변 사본으로 보관한다.
- `FormatHost.deliver(format_routing, content)`: `content["text"]`(TEXT 대체본, 항상 필수)와 선택적 `media`(`{형식: payload}`), `text_alternative`, `captions`를 받아 계획을 실행하고 단계별 기록을 반환한다: `generation_status`(콘텐츠 제공 여부), `render_status`, `functional_test_status`, `accessibility_status`(의무별 MET/NOT_MET), `source_verification_status`(항상 `NOT_RUN`), `verification_status=UNVERIFIED`, `is_evidence=False`.
- 대체 사유(`fallback_reason`): `FORMAT_NOT_IN_OUTPUT_SCHEMA`(호스트 밖에서 만든 계획도 호스트 스키마로 다시 확인), `MEDIA_CONTENT_MISSING`, `ACCESSIBILITY_REQUIREMENT_NOT_MET:<의무>`(렌더링 전에 확인), `RENDERER_NOT_CONNECTED`, `RENDER_FAILED:<예외>`, `RENDER_OUTPUT_INVALID`(mapping이 아니거나 `artifact`가 없거나 `None`), `FUNCTIONAL_TEST_UNAVAILABLE`, `FUNCTIONAL_TEST_FAILED`, `FUNCTIONAL_TEST_ERROR:<예외>`. 어떤 경우든 `planned_format`(선택 결과)은 보존하고 TEXT를 전달한다.
- 렌더러 출력의 `verification_status`·`is_evidence`·`verified`·`is_verified`는 버린다. 계획 객체는 변경하지 않는다.

DIAGRAM 렌더러 `src/co_thoughts/diagram_renderer.py`(`MermaidFlowchartRenderer`, 외부 의존성 없음):

- 지원 부분집합: 머리글 `graph`/`flowchart` + `TD`·`TB`·`LR`(같은 줄 `;` 뒤에 문장을 이어 쓰는 `graph TD; A --> B` 형식 포함); 노드 `id`, `id[라벨]`, `id(라벨)`(둥근 상자), `id{라벨}`(판단); 연결 `-->`(화살표)·`---`(선), 라벨 `-->|라벨|`·`-- 라벨 -->`, 체인 `A --> B --> C`; `%%` 주석, `;` 구분(따옴표·괄호·`|라벨|` 안의 `;`는 라벨 문자). 그 밖의 문법(`subgraph`, `==>`, `&`, 원·엑스 연결 `---o`/`---x`/`-->o`/`-->x`, 다른 다이어그램 종류 등)과 XML에서 쓸 수 없는 제어 문자(`DIAGRAM_INVALID_CHARACTER`)는 `DiagramSyntaxError`(고정 코드: `DIAGRAM_HEADER_UNSUPPORTED`, `DIAGRAM_SYNTAX_UNSUPPORTED:line N`, `DIAGRAM_NODE_REDEFINED:<id>` 등)로 거부하므로 호스트에서 `RENDER_FAILED:DiagramSyntaxError`와 TEXT 대체가 된다. 추측해서 그리지 않는다.
- 한도: 노드 200, 연결 400, 라벨 200자, 원본 20,000자, 제목 200자, 설명 2,000자(자동 요약은 2,000자에서 잘라 "(truncated)" 표시).
- 배치: 진입 연결이 없는 노드에서 시작하는 너비 우선 계층 배치(결정적, 순환 허용). 인접 계층 사이 연결만 직선으로 그리고, 역방향·같은 계층·자기 순환·계층을 건너뛰는 연결은 도식 옆(TD는 오른쪽, LR은 아래쪽) 전용 통로로 돌려 다른 노드를 지나지 않게 한다. 통로로 가는 연결은 노드 옆(같은 계층 노드가 있는 곳)이 아니라 계층 사이 빈 공간의 짧은 트랙으로 나가고 들어온다. 같은 두 노드를 잇는 평행 연결은 서로 비켜 그리고 라벨도 겹치지 않게 엇갈려 둔다. 글자는 명시한 monospace 글꼴(`font-family`)로 그리고 폭을 글자 종류별 보수적 상한(일반 0.625em, 전각 1em)으로 계산하며, 모든 글자는 자기 도형 안에 들어가도록 크기를 정한다(판단 마름모는 내접 사각형이 절반 크기이므로 글자 영역의 두 배). 연결 라벨도 120px 폭으로 줄바꿈하고, 계층 간격·행열 간격·통로 간격을 라벨 크기에 맞춰 넓히며, SVG 크기는 실제로 그린 모든 요소의 경계로 정한다. 라벨은 렌더링 폭(전각 문자는 넓게 계산) 기준으로 줄바꿈하고 상자 크기를 맞추며, XML 이스케이프한다.
- 접근성: SVG에 `role="img"`, 문서마다 고유한 id(내용 해시 + 렌더러별 순번)로 연결한 `aria-labelledby`, `<title>`(기본 "Flowchart", payload `title`로 지정 가능), `<desc>`(payload `description` 또는 노드·연결 자동 요약)를 넣는다. 호스트의 `TEXT_ALTERNATIVE` 의무는 별도로 `content["text_alternative"]`로 확인한다.
- 출력: `{"artifact": SVG 문자열, "mime_type": "image/svg+xml", "node_count", "edge_count", "summary"}`. 렌더링은 도식 내용을 검증하지 않는다.
- 등록 예: `registry.register("DIAGRAM", MermaidFlowchartRenderer())`. 테스트는 SVG 구문 유효성(XML 파싱), 노드·연결 수, 배치 방향, 이스케이프, `<title>`/`<desc>`, 호스트 경유 전달·실패 대체·접근성 차단을 각각 확인한다.

### Phase 4 — 평가 및 승격
- v0.1 키워드 평가: `docs/testing/format_routing_keyword_eval_v0.1.md` (작성자 라벨링 과제 77개, 전체 0.623, 주제 언급으로 인한 불필요한 매체 비율 0.452, 바꿔 말한 요청 재현율 0). 요청 표현 조건(보고서 7절)으로 홀드아웃 세트(38개)는 0.526에서 0.842로, 불필요한 매체 비율은 0.619에서 0.048로 개선됐다. 바꿔 말한 요청 인식(보고서 8절)으로 두 번째 홀드아웃 세트(40개)의 바꿔 말한 요청 재현율이 0/20에서 18/20으로 올랐고, TEXT 과제 16개 중 1개에서 새 오탐이 생겼다. 자체 신호 구문 문맥 확인(보고서 9절)으로 세 번째 홀드아웃 세트(20개)는 8/20에서 20/20이 되었고, 세트 밖 새 사례로는 11/12였다. PR #13–#18의 리뷰 후속 수정 내역은 보고서 8.5·9.5·9.6절에 있다.
- 대표 작업군별 선택 정확성·불필요한 매체 생성·fallback·접근성 평가
- 독립 테스트와 회귀 테스트 통과 후에만 구현 상태 승격

## 11. 최소 테스트 기준

- 단순 번역·정의·계산은 TEXT를 선택한다.
- 구성 요소 관계 설명은 DIAGRAM을 후보로 선택한다.
- 시간적 동작 설명은 사용 가능 기능에 따라 ANIMATION/VIDEO 또는 TEXT fallback을 선택한다.
- 변수 조작이 불가능한 환경에서는 INTERACTIVE를 선택 완료로 표시하지 않는다.
- 사용자 지정 형식과 프로젝트 출력 스키마가 충돌하면 충돌을 보고하고 임의로 스키마를 덮어쓰지 않는다. (구현·단위 테스트됨: `selection_status=CONFLICT`, `conflicts`)
- 사용자의 접근성 요구(`text_only`, `reduced_motion`)는 형식 선택보다 우선하고, 명시 요청과 충돌하면 보고한다. `screen_reader`·`captions`는 `accessibility_requirements`로 호스트 의무를 전달한다. (구현·단위 테스트됨)
- format routing이 verification_status를 승격하지 않는다.
- format routing 결과가 기존 인지 연산·검증 라우팅 결과를 변경하지 않는다.
- 선택, 생성, 렌더링, 기능 시험 상태를 독립적으로 검증한다.

## 12. 현재 상태 선언

| 영역 | 상태 | 근거 |
|---|---|---|
| format planner (규칙 기반) | 구현됨, `main` 반영 | PR #2, 개선 #3–#18 |
| Cognitive Router 연결 | 구현됨, `main` 반영 | PR #2 |
| 공통 요청 검증 | 구현됨 | PR #6–#8 |
| 형식 선택 평가 | 프로젝트 내부 측정 | 개발 77/77, 홀드아웃 v0.1 37/38, v0.2 37/40, v0.3 20/20, 세트 외 새 사례 11/12 (`docs/testing/format_routing_keyword_eval_v0.1.md`) |
| 독립 평가 | 미실시 (2026-11-04 프로젝트 소유자 결정으로 보류) | 지침만 `main`에 있음(PR #20). 평가자 A 데이터 PR #23은 병합 없이 닫힘. 모든 평가 세트·라벨을 같은 작성자가 작성 |
| 출력 스키마 충돌 보고 | 구현됨 (단위 테스트) | `output_schema.allowed_formats`, `selection_status=CONFLICT`, `conflicts` (§5, §6). 실제 프로젝트 어댑터가 스키마를 선언하는 연결은 Phase 3 범위 |
| 접근성 입력 | 구현됨 (단위 테스트) | `output_intent.accessibility`, `accessibility_requirements`, 접근성 충돌 (§5, §6). 의무 이행·검증(대체 텍스트·자막 생성)은 Phase 3 범위로 미구현 |
| 보조 형식(`secondary`), `audience`/`detail_level` | 미구현 | §5–§7 |
| Host/Adapter 인터페이스 (Phase 3) | 참조 구현 (가짜 렌더러로 단위 테스트) | `format_host.py`: 렌더러 등록, 기능 선언, 단계별 상태 기록, TEXT 대체. planner의 `render_status`는 여전히 `NOT_RUN`이며, 실행 결과는 호스트 기록에 있다 |
| DIAGRAM 렌더러 | 구현됨 (단위 테스트) | `diagram_renderer.py`: Mermaid flowchart 부분집합 → SVG, `<title>`/`<desc>`, 미지원 문법은 거부. 브라우저·보조기술에서의 실제 표시 시험은 미실행 |
| 그 밖의 렌더러(IMAGE·ANIMATION·VIDEO·INTERACTIVE·SIMULATION)·기능 시험 | 미구현·미실행 | 사용 가능한 renderer 없음 |
| SARA v3 호출 방식 | 전환됨 (2026-11-04, 단위 테스트) | 턴마다 자동 호출하지 않는다. 사용자가 요청하면 대화 전체를 검증한다. 사용자·AI 주장 모두 대상, 턴 ID별 발화 본문만 전송, 전송 전 미리보기와 `plan_id` 확인, 식별자 가명화. 계약: [`conversation_verification_contract_v0.1.md`](../contracts/conversation_verification_contract_v0.1.md) |
| SARA v3 Live 왕복 | 미검증 | Live 테스트 `test_live_conversation_verification_round_trip`은 `CO_THOUGHTS_SARA_V3_LIVE=1`과 SARA v3 체크아웃(`SARA_v3/cli.py`, 기본 `../SARA`, 또는 `CO_THOUGHTS_SARA_ROOT`)이 모두 있을 때만 실행된다. 2026-11-04에 실제 체크아웃과 provider 설정으로 실행했지만, provider가 크레딧 부족(HTTP 400)으로 실패했다. SARA는 이를 `NOT_ASSESSED`로 흡수했고, 테스트는 `claims_not_assessed=2`로 실패를 보고했다. 이 테스트는 claim이 하나라도 평가되지 않으면 실패하도록 강화했다. SARA CLI의 fail-closed 테스트는 실제 체크아웃으로 통과했다. 나머지 통합 테스트는 가짜 SARA를 쓴다. |

평가 수치는 같은 작성자가 만든 세트에서 측정한 값이므로 일반화 성능으로 해석하지 않는다. 특정 커밋의 CI 결과는 GitHub Actions 기록으로 확인한다.

## 13. 개발 절차와 규칙 기반 접근의 안정화 결정

### 13.1 병합 전 독립 리뷰

PR #12–#17은 자동 리뷰(Codex)가 끝나기 전에 병합되었고, 리뷰가 병합 후 새 오탐·누락을 찾아 후속 PR이 필요했다(#12: 2건, #13: 3건, #14: 1건, #15: 5건, #16: 3건, #17: 1건). #18은 병합 전에 리뷰가 끝났고 지적 1건을 같은 PR에서 고쳤다. 앞으로는 다음을 기본 절차로 한다.

1. PR의 CI가 통과하고 자동 리뷰가 **완료된 뒤** 병합한다.
2. 리뷰 후 수정 커밋을 올렸다면 `@codex review`로 최신 커밋을 다시 리뷰받는다.
3. 리뷰 지적은 수정 전 코드에서 재현한 뒤 고치고, 예시는 단위 테스트로 고정한다.
4. 홀드아웃 세트는 규칙 조정에 쓰지 않는다. 홀드아웃 오류를 보고 규칙을 고치면 그 사실을 보고서에 기록한다.

### 13.2 규칙 확장 중단 기준

PR #12–#18에서 리뷰가 규칙을 바꿀 때마다 새 반례를 찾았다. 규칙은 구문을 어휘로 근사한 것이므로, 다음 기준에 따라 키워드·예외 규칙의 **기능 확장을 중단**하고 결함 수정만 받는다.

- 새 형식 어휘나 새 예외 범주 추가는 하지 않는다. 회귀(기존 동작이 깨지는 결함) 수정만 허용한다.
- 추가 개선은 (a) 호스트가 선언하는 `output_intent.requested_format`·context 신호를 우선 사용하고, (b) 독립 평가 세트로 규칙 기반 planner와 학습형 분류기를 비교한 뒤 결정한다. 독립 평가가 보류된 동안 (b)는 수행할 수 없으므로 (a)만 진행한다.
- 리뷰에서 나온 반례는 적대적 회귀 세트로 모은다(보류 중인 작업).

### 13.3 다음 단계 (우선순위 순)

1. 문서·상태 동기화 (본 절 포함)
2. ~~독립 평가 체계~~ — **보류** (2026-11-04 프로젝트 소유자 결정). 지침(`docs/testing/format_routing_independent_eval_guidelines_v0.1.md`)은 유지하며, 재개 시 새 평가자가 처음부터 작성한다. 그동안 형식 선택 수치는 같은 작성자 세트 기준으로만 보고한다.
3. 출력 스키마 충돌 보고와 접근성 입력 — 구현됨 (§7 우선순위 1·2, §11)
4. Host/Adapter 인터페이스: 렌더러 프로토콜, 생성·렌더링·기능 시험·출처 검증 상태 분리 기록, 실패 시 TEXT 대체 — 참조 구현됨(`format_host.py`)
5. 실제 렌더러 연결: DIAGRAM부터, 렌더링·접근성·기능 시험을 분리 검증 — DIAGRAM 구현됨(`diagram_renderer.py`), 다른 형식은 미연결
6. SARA v3 Live 왕복 검증: 실제 Provider 환경에서, 사용자 요청 대화 검증 → SARA → assessment envelope → 후속 backend 전달 (provider 크레딧 또는 무료 provider 필요)

외부 검토(2026-11-04)는 SARA v3 쪽 일부 게이트가 WAIVED 상태라고 언급했다. 이 저장소에서는 확인하지 않았다. 이 저장소에서는 2026-11-04에 Live 왕복을 실행했지만, provider가 크레딧 부족으로 실패해 끝까지 성공한 적이 없다. 따라서 Live 왕복은 미검증 상태다.
