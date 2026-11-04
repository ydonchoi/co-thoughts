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

`tests/evaluation/test_format_routing_eval.py`는 개발 세트와 홀드아웃 세트 모두에 7.4절의 기준을 강제한다. 계획기가 개선되면 기준을 올린다.

## 7. 후속: 요청 표현 조건

### 7.1 변경 내용

이제 키워드가 있어도 문장이 그 형식의 출력을 요청할 때만 비텍스트 형식을 고른다.

- 영어: 키워드 앞 4토큰 안에 요청 동사(show, make, create, give, generate, render, build, produce, run, sketch, illustrate, add, display, design, record, prepare, provide, include, use, want, need, present)가 있거나, "as/in/with/into/using/via a(n) …" 형태이거나, 키워드로 과제가 시작할 때("Diagram of …", "A video about …"). 동사형 키워드(draw, simulate, animate)는 명령문으로 쓰였을 때 인정한다("Draw …", "Can you simulate …").
- 한국어: 키워드 뒤에 형식 조사(`로`/`으로`)가 오거나, 짧은 단어 하나와 목적격 조사(생략 가능), 요청 동사(보여, 그려, 만들, 돌려, 해줘, 생성, 띄워, 부탁, 필요, 원해)가 이어질 때.
- 제외 목록이 첫 단어의 활용형을 처리한다("draws upon", "drawing on", "bigger picture").
- 바꿔 말하기 어휘는 추가하지 않았다. 이번 변경은 오탐을 줄이는 것이 목적이라 매체 누락 비율은 그대로다.

### 7.2 홀드아웃 세트

`tests/evaluation/format_routing_eval_holdout_v0.1.json`(새 과제 38개, 같은 그룹 구성)은 계획기를 바꾸기 **전에** 작성·커밋했고 규칙 조정에 쓰지 않았다. 기준선은 `main` @ `44b3676`에서 측정했다.

### 7.3 결과

| 세트 | 지표 | 변경 전 | 변경 후 |
|---|---|---|---|
| 개발(77) | 정답 | 48 (0.623) | **67 (0.870)** |
| | topic 그룹 | 2/20 | **20/20** |
| | collision 그룹 | 7/8 | **8/8** |
| | 불필요한 매체 비율 | 0.452 | **0.000** |
| | 매체 누락 비율 | 0.286 | 0.286 |
| 홀드아웃(38) | 정답 | 20 (0.526) | **31 (0.816)** |
| | topic 그룹 | 1/12 | **11/12** |
| | collision 그룹 | 2/4 | **3/4** |
| | 불필요한 매체 비율 | 0.619 (13/21) | **0.095 (2/21)** |
| | 매체 누락 비율 | 0.294 (5/17) | 0.294 (5/17) |

두 세트 모두 explicit·plain 그룹은 100%, 다른 매체 오선택은 0을 유지했다.

남은 홀드아웃 오탐 (보고만 하고 규칙은 조정하지 않음):
- HT08 "**Show that** the image of a compact set …": 수학 관용구 "show that"을 요청 동사로 읽는다.
- HC01 "The match ended **in a draw**": "in a …" 형식 조건이 명사 "draw"(무승부)에 걸린다.

### 7.4 게이트 기준

개발: 정답 67개 이상, topic 20개 이상, collision 8개 이상, 불필요한 매체 비율 0.000 이하, 매체 누락 비율 0.286 이하. 홀드아웃: 정답 32개 이상, topic 12개 이상, collision 3개 이상, 불필요한 매체 비율 0.048 이하, 매체 누락 비율 0.294 이하 (7.6절 반영 후 갱신). 공통: explicit·plain 100%, 다른 매체 오선택 0.

### 7.5 절충과 한계

- 개발 세트 수치는 낙관적이다. 이 세트를 보며 규칙을 조정했기 때문이다("the plot of the movie"가 걸린 뒤 동사 목록에서 "plot"을 뺀 조정 1건). 현실적인 추정치는 홀드아웃 수치로 본다.
- 홀드아웃 세트도 규칙과 개발 세트를 만든 작성자가 썼으므로 작성자의 표현 습관을 공유한다.
- 두 세트 모두 동사 없는 짧은 요청이 없다. 그런 사례를 따로 확인한 뒤 "키워드로 시작" 조건과 한국어 부탁/필요/원해 조건을 추가했고 단위 테스트로 고정했다. 알려진 비용: 형식 단어를 주제로 쓰면서 과제를 *시작*하는 경우("Image compression in JPEG: how does it work?")는 형식으로 선택된다.
- 요청 표현도 없고 키워드로 시작하지도 않는 요청(예: 관사 없는 복수형 "Explain photosynthesis with diagrams")은 이제 놓친다.
### 7.6 리뷰 후속 조치 (#12에 대한 Codex 리뷰)

외부 자동 리뷰가 두 평가 세트 밖에서 요청 표현 조건의 오탐 2종을 찾았다.

- 요청 동사가 다른 절을 지배하는 경우: "I **need to** understand video codecs", "We **need to** discuss image compression". 수정: 요청 동사와 키워드 사이에 `to`, 의문사, `that`, `if`가 없을 때만 인정한다("Show **how** video codecs work"도 해결).
- `in/with a …`가 다른 명사를 꾸미는 경우: "rules in a **video game**", "in a **video codec**". 수정: 형식 단어가 구의 중심어일 때만(뒤에 문장 끝, 구두점, `of/about/that/to/for/with/…`가 올 때만) 인정한다.

수정 후: 개발 세트는 변화 없음(67/77, 불필요한 매체 비율 0.000). 홀드아웃은 **32/38 (0.842)**, 불필요한 매체 비율 **0.048 (1/21)**, 매체 누락 비율은 그대로다.

**오염 주의:** 절 경계 규칙은 홀드아웃 HT08("Show **that** the image of …")도 해결한다. 이 규칙을 작성할 때 HT08이 실패한다는 사실을 이미 알고 있었다. 규칙의 동기는 리뷰어의 예시였지만, 홀드아웃이 31에서 32로 오른 것은 독립적인 증거가 아니다. 남은 홀드아웃 오탐은 HC01("ended in a draw;" — 명사 "draw"가 구의 중심어이고 뒤에 구두점이 온다)이다.

## 8. 후속: 바꿔 말한 요청 인식

### 8.1 변경 내용

형식별로 바꿔 말하기 어휘를 추가했다. 새 단어는 모두 7절과 같은 요청 표현 조건을 거친다. 단, 그 자체로 출력 형태를 나타내는 구(자체 신호)는 예외다.

| 형식 | 요청 표현 조건을 거치는 단어 | 자체 신호 구 |
|---|---|---|
| DIAGRAM | visualize/visualise/visualization, chart, graph, mind map, timeline, 시각화, 차트, 그래프, 도표, 도해, 마인드맵, 타임라인 | boxes and arrows |
| IMAGE | photo, photograph, clip art, 사진 | — |
| VIDEO | clip, screencast, 녹화, 클립 | — |
| INTERACTIVE | — | let me tweak/adjust/play with/change/vary, 바꿔가며, 바꿔볼 수 있게, 조절하면서, 조절하며, 조절할 수 있게 |
| SIMULATION | what-if, scenario analysis, 시나리오별 | model what happens |
| ANIMATION | in motion, 움직이게 | 움직이는 모습으로 |

`visualize`, `visualise`, `chart`, `graph`는 명령문 동사 키워드로도 인정한다("Chart the revenue …", "Graph y = x²").

### 8.2 두 번째 홀드아웃 세트

`tests/evaluation/format_routing_eval_holdout_v0.2.json`(40개: 바꿔 말한 요청 20, "graph theory"·"photo editing"·"chart of accounts"처럼 새 어휘를 주제로 쓴 과제 12, plain 4, explicit 4)은 이번 변경 **전에** 작성·커밋했고, 다른 세트와 겹치는 과제가 없다. 기준선은 `main` @ `fa9dd95`에서 측정했다.

### 8.3 결과

| 세트 | 지표 | 변경 전 | 변경 후 |
|---|---|---|---|
| 개발(77) | 정답 | 67 | 77 |
| | paraphrase 그룹 | 0/10 | 10/10 |
| | 매체 누락 비율 | 0.286 | 0.000 |
| 홀드아웃 v0.1(38) | 정답 | 32 | 37 |
| | paraphrase 그룹 | 0/5 | 5/5 |
| **홀드아웃 v0.2(40)** | 정답 | 20 (0.500) | **37 (0.925)** |
| | paraphrase 그룹 | 0/20 | **18/20** |
| | topic 그룹 | 12/12 | 11/12 |
| | 불필요한 매체 비율 | 0.000 | **0.062 (1/16)** |
| | 매체 누락 비율 | 0.833 | **0.083** |

세 세트 모두 explicit·plain 그룹은 100%, 다른 매체 오선택은 0을 유지했다.

**어떤 수치를 믿을지:** 어휘를 개발 세트의 바꿔 말하기 오류에서 만들었으므로 개발 세트 결과는 조정된 값이다. 홀드아웃 v0.1의 바꿔 말하기 사례도 같은 단어(visualize, photo, 시각화, 사진)를 쓰므로 그 향상도 독립적이지 않다. 홀드아웃 v0.2를 기준으로 삼는다. 바꿔 말한 요청 재현율이 0에서 0.9로 올랐고, 그 대가로 TEXT 과제 16개 중 1개에서 새 오탐이 생겼다.

남은 v0.2 오류 (보고만 하고 조정하지 않음):
- QT03 "Give me tips for **photo** editing" → IMAGE: "give"의 목적어는 "tips"인데, 요청 동사 범위 검사가 동사의 목적어를 확인하지 않는다.
- QR07 "Render a 3D **view** of the molecule" → TEXT: "view"가 어휘에 없다.
- QR10 "Give me **controls** to change gravity" → TEXT: "controls"는 주제로 너무 흔해 일부러 넣지 않았다.

### 8.4 한계

- 홀드아웃 v0.2도 같은 작성자가 썼고, 어휘의 큰 방향(chart/graph/photo/clip)을 정한 뒤에 작성했다. topic 그룹은 오탐을 재려고 일부러 그 어휘를 썼지만, 작성자의 표현 습관은 여전히 공유한다.
- 자체 신호 구("let me change", "조절하면서")는 추가 확인 없이 형식을 고른다. "Let me change the subject" 같은 문장도 INTERACTIVE로 선택된다.
- 어휘는 닫힌 목록이다. 새로운 바꿔 말하기("render a 3D view", "controls to …")는 명시적으로 추가하고 새 홀드아웃 세트로 측정해야 한다.

### 8.5 리뷰 후속 조치 (#13에 대한 Codex 리뷰)

#13의 Codex 리뷰가 머지 후에 끝났고, 모든 평가 세트 밖에서 오탐 3종을 보고했다. 세 가지 모두 `main` @ `db02b3c`에서 재현됐고 수정했다.

- 문장 첫머리의 `graph`/`chart`가 주어 명사로 쓰인 경우("Graph theory **is** …", "Chart **of** accounts …")를 명령문으로 보고 DIAGRAM을 골랐다. 이제 동사형 키워드 뒤에 `of`가 오거나 세 토큰 안에 계사·조동사(is, are, was, were, has, have, can, will)가 오면 명령문으로 인정하지 않는다. 단, 키워드 바로 뒤에 의문사가 오면 목적절이므로 명령문으로 인정한다("Chart **what** is happening …", "Chart **who** is buying". #14에 대한 Codex 추가 지적).
- 사동 표현 `움직이게`("힘이 물체를 움직이게 **하는 이유**")가 자체 신호로 처리돼 ANIMATION을 골랐다. 이제 자체 신호에서 빼고 한국어 요청 동사 조건("움직이게 **보여줘**")을 거치게 했다.
- "clip art"가 `clip` 때문에 VIDEO로 선택됐다. 이제 "clip art"는 IMAGE 키워드이고, `clip` 뒤에 "art"가 오면 건너뛴다.

세 평가 세트 결과는 바뀌지 않았다(개발 77/77, 홀드아웃 v0.1 37/38, 홀드아웃 v0.2 37/40). 예시는 단위 테스트로 고정했다.

---

[English companion](format_routing_keyword_eval_v0.1.en.md)
