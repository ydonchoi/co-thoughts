# 설명 형식 라우팅 — 키워드 평가 v0.1 (Phase 4)

> 상태: MEASURED (프로젝트 내부, 작성자 라벨링) / 독립 검증 안 됨
> 범위: `explanation_format_router` 키워드 매칭의 후보 형식 선택 (호스트 capability·context 신호 제외)
> 재현: `PYTHONPATH=src/co_thoughts python tests/evaluation/format_routing_eval.py`
> 데이터: `tests/evaluation/format_routing_eval_v0.1.json` · 게이트: `tests/evaluation/test_format_routing_eval.py`
> 측정 기준: `main` @ `1a2c2d5`

## 1. 방법

- 과제 77개(영어 45, 한국어 32). 각 과제에 "독자가 합리적으로 요청 형식이라고 볼" 형식을 라벨링했다.
- 5개 그룹: `explicit`(등록 키워드로 형식을 요청), `plain`(형식 어휘 없음), `topic`(형식 단어가 요청이 아니라 주제), `collision`(알려진 부분 문자열·구 충돌), `paraphrase`(등록 키워드 없이 형식을 요청).
- 측정 대상: capability 대체 전 후보인 `capability_status.requested`.

## 2. 결과

| 그룹 | n | 정답 | 정확도 |
|---|---|---|---|
| explicit | 25 | 25 | 1.000 |
| plain | 14 | 14 | 1.000 |
| collision | 8 | 7 | 0.875 |
| topic | 20 | 2 | 0.100 |
| paraphrase | 10 | 0 | 0.000 |
| **전체** | **77** | **48** | **0.623** |

| 지표 | 값 | 정의 |
|---|---|---|
| 불필요한 매체 비율 | 0.452 (19/42) | TEXT가 정답인데 비텍스트 후보를 낸 비율 |
| 매체 누락 비율 | 0.286 (10/35) | 매체가 정답인데 TEXT를 낸 비율 |
| 다른 매체 오선택 비율 | 0.000 (0/35) | 매체가 정답인데 다른 매체를 낸 비율 |

형식별 정밀도는 IMAGE(0.417)와 VIDEO(0.429)가 가장 낮다. "image compression", "brand image", "video codecs", "the movie", "이미지 처리", "기업 이미지", "영상 압축" 같은 주제 언급 때문이다.

## 3. 발견 사항

1. **명시적 요청과 일반 텍스트는 모두 맞았다** (39/39). 등록 키워드를 요청으로 쓰면 올바른 형식을 고르고, 일반 과제에 형식을 지어내지 않는다.
2. **주제 언급이 주된 오류다 (20개 중 18개 오답).** 키워드 매칭은 "JPEG 이미지 압축 원리 설명"(TEXT)과 "이미지를 보여줘"(IMAGE)를 구분하지 못한다. 키워드가 부족해서가 아니라 어휘 기반 매칭의 구조적 한계다.
3. **바꿔 말한 요청은 하나도 잡지 못했다 (0/10).** "visualize", "photo", "clip", "tweak the parameters", "시각화", "사진"은 키워드가 아니다.
4. **제외 목록 결함 1건:** 제외 목록이 "draw upon" 같은 고정 구문이라 활용형 "draws upon"을 제외하지 못한다(C05).
5. **대체 동작이 피해를 줄인다.** 잘못된 비텍스트 후보는 호스트가 그 capability를 명시적으로 선언했을 때만 primary가 되고, 아니면 TEXT로 대체된다. 기능이 많은 호스트에서는 45%의 불필요한 매체 비율이 그대로 드러난다.

## 4. 권고 (이번 변경에서는 구현하지 않음)

- 비텍스트 형식을 고르기 전에 키워드 근처의 요청 표현을 요구한다(예: "show/draw/make/create … as/in a <형식>", "~로 보여줘/그려줘/만들어줘"). 주제 언급 오탐을 줄인다.
- 제외 목록도 키워드와 같은 활용형 처리를 적용한다.
- 의미가 분명한 경우에만 바꿔 말하기 어휘를 소량 추가한다("visualize", "시각화" → DIAGRAM, "photo", "사진" → IMAGE). 이 평가 세트로 효과를 측정한다.
- 호스트가 줄 수 있다면 어휘 추론보다 `output_intent.requested_format`이나 context 신호를 우선한다.

## 5. 한계

- 라벨은 작성자 판단이며 외부 평가자나 평가자 간 일치도가 없다.
- 현재 키워드·제외 규칙을 만든 작성자가 이 데이터도 만들었다. 특히 `collision` 그룹은 이미 규칙이 처리하는 사례 쪽으로 치우쳐 있다.
- 77개는 형식별 수치를 안정적으로 추정하기에 적다. 형식별 수치의 불확실성이 크다.
- 후보 선택만 측정했다. 렌더링, 접근성, 사용자에게 주는 이득은 평가하지 않았다.

## 6. 회귀 게이트

`tests/evaluation/test_format_routing_eval.py`는 다음을 강제한다: explicit·plain 그룹 100%, 다른 매체 오선택 0, 전체 정답 48개 이상, collision 7개 이상, topic 2개 이상, 불필요한 매체 비율 0.452 이하, 매체 누락 비율 0.286 이하. 계획기가 개선되면 기준을 올린다.

---

[English companion](format_routing_keyword_eval_v0.1.en.md)
