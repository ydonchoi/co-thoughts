# 대화 전체 독립 검증 계약 v0.1

상태: 구현됨 (가짜 SARA로 단위 테스트). 실제 provider 왕복은 조건부로만 확인됨 (§9)
구현: `src/co_thoughts/conversation_verification.py`, `src/co_thoughts/runtime.py`
결정: 2026-11-04 프로젝트 소유자 (ydonchoi)

## 1. 목적과 전환 배경

SARA v3는 턴마다 외부 LLM·검색 provider를 호출한다(judgment와 응답 생성, 최소 2회). 대화마다 이를 실행하면 비용과 지연이 턴 수에 비례한다. 또 대화용 구독과 별도로 API 크레딧이 필요하다. 2026-11-04 라이브 시험에서는 provider 오류(크레딧 부족, HTTP 400)가 났다. 그런데 SARA는 이를 `NOT_ASSESSED`로 흡수했고, 검증이 빠진 사실이 겉으로 드러나지 않았다.

그래서 SARA v3 호출 시점을 **매 턴 자동**에서 **사용자가 별도로 요청할 때 대화 전체를 한 번에**로 바꾼다.

## 2. 결정 사항

| 항목 | 결정 |
|---|---|
| 호출 시점 | 사용자 요청 시에만. 대화 턴 실행 중에는 SARA를 호출하지 않는다 |
| 검증 대상 | 사용자 발화의 주장과 AI 응답의 주장 모두 |
| 전송 단위 | 턴 ID별 발화 본문 1개(사용자 또는 AI)와 그 발화에서 나온 claim만. SARA 호출 1회에 1개 |
| 기본 범위 | 대화 전체. `turn_ids` 또는 `claim_refs`로 줄일 수 있다 |
| 전송 전 확인 | 계획(`plan`)의 미리보기를 보여 준 뒤, 그 `plan_id`를 확인값으로 받아야 실행한다 |
| 식별자 | SARA로 가는 `conversation_id`·`request_id`·`turn_id`·claim ID·provenance ID는 실행마다 새로 만든 가명이다. 실제 ID와의 대응은 로컬에만 둔다 |
| 사용자 인용 출처 (2026-11-13 추가) | 호스트가 준 `user_claims[].source_urls`만 그 발화의 SARA 호출에 `evidence`로 보낸다. 백엔드가 붙인 URL은 보내지 않는다 |
| 사용자 제공 원문 (2026-11-13 추가) | SARA가 일부만 읽을 수 있는 출처는 사용자가 직접 구한 원문 파일(`user_documents`)로 보완할 수 있다. 해당 claim의 호출에만 붙인다. 파일 이름은 보내지 않는다. 문서가 인용 출처가 맞는지와 그 문서를 얼마나 신뢰할지는 SARA가 정한다(§10) |

## 3. 흐름

```text
대화 턴 (runtime.run)
  └─ SARA v3가 설정된 경우에만 턴 기록: 사용자 발화 + user_claims, AI 응답 + claims
     출력: conversation_verification = {status: NOT_REQUESTED, verification_status: UNVERIFIED, recorded_claim_refs}
     외부 전송 없음

사용자가 검증 요청
  1. plan = runtime.plan_conversation_verification(conversation_id, turn_ids=?, claim_refs=?)
     → plan["preview"]를 사용자에게 보여 준다. 외부 전송 없음
  2. 사용자 확인
  3. result = runtime.verify_conversation(conversation_id, confirmation=plan["plan_id"], 같은 선택)
     → 발화별 배치를 SARA v3로 전송하고 claim별 결과를 돌려준다
```

## 4. 턴 기록

- **AI claim:** 백엔드 출력의 `claims`(`id`, `text`)
- **사용자 claim:**
  - 우선 요청의 `user_claims`(호스트가 지정)를 쓴다. 없으면 백엔드 출력의 `user_claims`(백엔드가 추출)를 쓴다.
  - Co-thoughts는 사용자 발화에서 claim을 직접 추출하지 않는다.
  - claim을 지정하지 않으면 `UC-n`이 ID로 붙는다.
  - 요청의 `user_claims` 항목은 `source_urls`(사용자가 인용한 출처 URL 목록)를 가질 수 있다. 주장당 5개까지, HTTPS·기본 포트만 허용하고, 인증 정보·fragment·공백이 있으면 백엔드 호출 전에 `USER_CLAIMS_INVALID`로 거부한다. 중복 URL은 하나로 합친다. 같은 문장의 claim이 여러 번 오면 첫 번째 ID를 남기고 모든 사본의 URL을 합치며(합쳐서 5개 이하), 버려지는 사본의 URL도 똑같이 검증한다.
  - 백엔드 출력의 `claims`나 `user_claims`에 붙은 `source_urls`는 백엔드 근거이므로 기록하지 않는다.
  - `run_workflow`, `run_natural_language` 경로로 요청해도 `user_claims`는 그대로 기록까지 전달된다(회귀 테스트로 고정).
- **사용자 발화 본문:** 요청의 `task`
- **AI 응답 본문:** 출력의 `response`. 비어 있으면 claim 문장들을 이어 붙인다.
- **잘못된 입력 처리:**
  - 요청의 `user_claims`가 잘못되면 백엔드 호출 전에 `USER_CLAIMS_INVALID`로 거부한다.
  - 백엔드의 `user_claims`가 잘못되어도 대화 턴은 실패시키지 않는다. 사용자 claim만 기록에서 빼고 `warnings: ["BACKEND_USER_CLAIMS_INVALID"]`로 표시한다.
- **기록 단위:**
  - claim이 없는 발화는 기록하지 않고, 전송하지도 않는다.
  - 같은 `turn_id`를 다시 실행하면 이전 기록을 대체한다.
  - 한 발화 안에서 공백을 정규화한 문장이 같은 claim은 한 번만 보낸다. 다른 발화에 있는 같은 문장은 본문 맥락이 다르므로 따로 보낸다.
- **보관:**
  - 기록은 프로세스 메모리에만 있다(영구 저장 없음).
  - 대화당 최대 500턴, 최대 100개 대화를 보관하고, 넘으면 오래된 것부터 버린다.
  - 버린 턴 수는 계획 미리보기의 `turns_evicted_before_plan`에 표시한다.
- **SARA v3 미설정 시:** 기록하지 않는다.

## 5. 계획과 확인

`plan["preview"]`가 담는 항목은 다음과 같다.

| 필드 | 뜻 |
|---|---|
| `provider_calls` | SARA 호출 수(발화별 배치 수) |
| `turns_sent`, `turn_ids_sent` | 전송될 턴 |
| `claims_sent`, `claims_by_role` | 전송될 claim 수(USER / ASSISTANT) |
| `content_chars_sent` | 전송될 본문 글자 수 합 |
| `source_urls_sent` | 전송될 사용자 인용 URL 수(호출별 합) |
| `user_documents` | 문서별 `document`(`D<n>`), `file_name`, `media_type`, `pages`, `cites`, `claim_refs`, `sha256`, `chars`, `calls`. 본문은 넣지 않는다 |
| `document_chars_to_sara`, `document_excerpt_chars_per_claim_max` | SARA로 가는 문서 글자 수(호출별 합)와, SARA가 claim마다 외부 provider에 보내는 발췌 상한(30,000자) |
| `send_unit` | `ONE_UTTERANCE_BODY_PER_CALL` |
| `context_forwarded` | 항상 `false` |
| `identifiers` | `PSEUDONYMIZED_PER_RUN` |
| `turns_recorded`, `turns_evicted_before_plan` | 기록된 턴 수, 보관 한도로 버려진 턴 수 |

- `plan_id`는 대화 ID, 배치 내용, 버린 턴 수, 배치 한도로 만든 해시다.
- 대화에 새 턴이 추가되거나 선택 범위가 바뀌면 `plan_id`가 달라진다.
- 그래서 사용자가 확인하지 않은 범위는 보낼 수 없다. 이전 계획의 ID를 쓰면 `VERIFICATION_PLAN_NOT_CONFIRMED`가 난다.

## 6. 전송 내용 (SARA 호출 1회)

```json
{"request_id": "cv-<run>-b<n>", "conversation_id": "cv-<run>", "turn_id": "t<위치>-u|a",
 "content": "<그 발화 본문>", "claim_candidates": [{"id": "K<n>", "text": "..."}],
 "evidence": [{"id": "S<n>", "url": "<사용자 인용 URL>", "snippet": "USER_SUPPLIED_SOURCE_URL"}],
 "provenance_ids": ["co-thoughts:cv-<run>:b<n>"]}
```

- 다른 턴의 본문, 요청 `context`, 백엔드 evidence, 백엔드가 주장한 상태는 보내지 않는다.
- `evidence`에는 그 호출에 든 claim들에 사용자가 인용한 URL만 넣는다(호출당 최대 10개, 넘으면 계획 단계에서 `SOURCE_URLS_PER_CALL_EXCEEDED`). SARA는 한 턴의 evidence를 그 턴의 모든 claim에 적용하므로, 같은 호출의 다른 claim도 이 URL을 근거 후보로 본다. URL 자체는 신뢰하지 않는 후보이며, SARA가 자기 출처 어댑터로 원문을 다시 읽어야 근거가 된다(SARA `SARA_OPEN_SOURCES_WEB_DOMAINS`).
- claim은 SARA 호출 1회에 최대 8개다(`SARAv3Connection.max_claims`). 넘으면 같은 본문으로 배치를 나눈다.
- 사용자 문서가 붙은 호출에는 `"user_documents": [{"id": "D<n>", "cites": "<인용 URL>", "text": "<추출한 본문>", "sha256": "<본문의 SHA-256>"}]`이 추가된다. 호출당 최대 5개다(넘으면 `USER_DOCUMENTS_PER_CALL_EXCEEDED`).

## 7. 결과

- `execution_status`: `SUCCEEDED` / `PARTIALLY_FAILED` / `FAILED` / `NOT_APPLICABLE`(보낼 claim 없음) / `NOT_CONNECTED`
- `coverage`: `claims_total`, `claims_assessed`, `claims_not_required_by_sara`, `claims_not_assessed`
- `claim_results`: claim별 `claim_ref`(`<turn_id>:<USER|ASSISTANT>:<claim_id>`), `turn_id`, `role`, `claim_id`, `text`, `sara_claim_id`, `status`(`ASSESSED`/`NOT_REQUIRED_BY_SARA`/`NOT_ASSESSED`), `sara_verification_status` 또는 `reason_codes`
- `batches`: 배치별 `sent_scope`, `execution_status`, `error_code`, `sara_reason_codes`
- claim의 `user_documents`: SARA가 그 claim을 판정하며 본 문서별 결과. `document`, `file_name`, `cites`, `identity`(`MATCHED`/`UNMATCHED`/`UNVERIFIED`), `reason_code`, `title_score`, `abstract_score`를 담는다. 이 계획이 보낸 문서와 digest가 다른 보고는 버린다.
- claim의 `full_text_requests`와 최상위 `full_text_requests`: SARA가 초록이나 스니펫만 읽어 판정하지 못한 출처 목록이다. 최상위 목록은 URL별로 묶고 `claim_refs`를 단다. 호스트는 이 목록을 보고 사용자에게 원문을 요청하면 된다.
- `assessment_envelopes`: SARA 원본 envelope. 수정하지 않고, claim ID는 가명 `K<n>`이다. 다음 턴에 `sara_assessment_envelopes`로 전달할 수 있다.
- `verification_status`는 항상 `UNVERIFIED`, `is_evidence`는 `false`, `truthfulness_status`는 `UNASSESSED`다. SARA의 판정은 `claim_results` 안에만 있고, Co-thoughts가 자기 출력을 승격하지 않는다.

**조용한 실패 방지:**
- 배치 하나가 실패해도 나머지 배치는 진행한다.
- SARA가 정상 종료했지만 envelope를 돌려주지 않은 claim은 `NOT_ASSESSED`로 표시한다. SARA 자신의 코드를 `reason_codes`에 넣는다. 예: `JUDGMENT_UNAVAILABLE_OR_INVALID`, `LLM_PROVIDER_HTTP_ERROR_400`.
- 예외: SARA가 스스로 **검증이 필요 없다고 판정한** 경우는 `NOT_REQUIRED_BY_SARA`로 따로 집계한다. SARA는 judgment가 "추론 있음"을 HIGH 확신으로 판정할 때만 검증을 시작하므로, 단순 사실 주장은 정상적으로 건너뛰어진다. 이 분류는 SARA의 `activation_decision`이 `activation_action=NO_INFERENCE_TRIGGER`이고 `activation_triggered=false`일 때만 적용한다. 그 밖의 경우(값이 하나라도 없거나 어긋남, `SARA_PRECHECK_REVIEW` 등)는 모두 `NOT_ASSESSED`다. `NOT_REQUIRED_BY_SARA`는 검증되었다는 뜻이 아니다.
- 자유 텍스트 오류 메시지는 내보내지 않는다.

## 8. 노출 범위에 대한 주의

- 호출 단위로 보면 노출이 최소화된다. 하지만 대화 전체를 검증하면 claim이 있는 발화 대부분이 결국 provider로 간다.
- 가명을 써도 같은 실행의 호출들은 같은 가명 `conversation_id`를 공유한다. 따라서 provider는 그 실행 안의 호출들을 하나로 묶을 수 있다. 막을 수 있는 것은 실제 ID 노출과, 서로 다른 실행 사이의 연결이다.
- 다른 턴을 가리키는 주장("그 정책은…")은 맥락이 없어 `NOT_ASSESSED`가 되기 쉽다. claim을 추출할 때 자기완결형 문장으로 만드는 것이 좋다.
- 사용자 인용 URL은 SARA로 가고, SARA는 그 페이지를 가져와 provider LLM에게 관계 판정을 맡긴다. 따라서 URL과 그 페이지 내용도 외부 provider에 노출된다.
- 2026-11-13 확인: 정책브리핑 정책뉴스 기사를 인용하면 SARA가 본문을 `ABSTRACT`로 읽고 관계를 판정했다(Gemini `SUPPORTS`). HTML에서 읽은 본문은 `ABSTRACT`라서 claim은 `UNVERIFIED`로 남았다(`FULL_TEXT_NOT_ACCESSED`).

## 9. 검증 상태

| 항목 | 상태 |
|---|---|
| 기록·계획·확인·배치·가명화·결과 대응 | 단위 테스트 (가짜 SARA, `tests/unit/test_sara_v3_integration.py`) |
| SARA CLI 프로세스 fail-closed | 실제 SARA 체크아웃으로 실행됨 (provider 설정 없음) |
| 사용자 제공 원문 | 단위 테스트(`tests/unit/test_user_documents.py`: 추출, 연결, 계획 확인, 결과 매핑). 2026-11-13 실제 확인: arXiv PDF(1706.03762, 15쪽, 39,521자)를 co-thoughts로 추출해 SARA CLI와 Gemini(`gemini-3.1-flash-lite`)로 왕복했다. 신원 대조는 `MATCHED`(제목 1.0, 초록 0.942)였다. `SARA_TRUST_USER_DOCUMENTS=1`에서는 claim이 `VERIFIED`가 됐다(근거: 원문 발췌 `SUPPORTS`). 같은 PDF를 다른 논문(BERT)의 원문으로 주면 `UNMATCHED`(초록 0.019)였다. 기본값(`0`) 왕복은 judgment가 3회 모두 실패해 실제로는 확인하지 못했다(503 1회, 무효 출력 2회). 이 경우는 단위 테스트로만 확인했다(`PARTIALLY_VERIFIED`, `USER_DOCUMENT_TRUST_NOT_ENABLED`) |
| 실제 provider 왕복 | 조건부 확인 (2026-11-12). Gemini API(`gemini-3.1-flash-lite`, 무료 등급)로 라이브 테스트가 3/3 통과했다(추론형 주장 2개, envelope 2개, 다음 턴 `PRESERVED`). 조건: (1) SARA의 Gemini 요청을 `responseSchema`에서 `responseJsonSchema`로 고친 **로컬 복사본**으로 실행했다. 원본 SARA는 Gemini에서 `additionalProperties` 때문에 항상 HTTP 400이 난다. (2) Brave 검색 키가 없어 envelope는 모두 `UNVERIFIED`(`BRAVE_SEARCH_API_KEY_REQUIRED`)였고, 출처 기반 판정은 시험하지 않았다. (3) 별도 시험 3회 중 1회는 judgment가 `INVALID_OUTPUT`을 내 주장 1개가 `NOT_ASSESSED`였다. 2026-11-04 Anthropic 시도는 크레딧 부족(HTTP 400)으로 실패했다 |

## 10. 사용자 제공 원문 (`user_documents`)

SARA는 자기가 직접 가져온 본문만 원문(`FULL_TEXT`)으로 친다. 유료 논문이나 robots.txt가 자동 접근을 막은 사이트처럼 SARA가 원문을 읽을 수 없는 출처는, 사용자가 직접 받은 파일로 보완할 수 있다.

```python
docs = [{"path": "paper.pdf", "cites": "https://doi.org/10.1000/xyz", "claim_refs": ["T1:USER:U1"]}]
plan = runtime.plan_conversation_verification(cid, user_documents=docs)   # 미리보기: 본문 없음
result = runtime.verify_conversation(cid, confirmation=plan["plan_id"], user_documents=docs)
```

- **형식**
  - PDF: 선택 설치 패키지 `pypdf`로 읽는다. 없으면 `PDF_SUPPORT_UNAVAILABLE`이다.
  - `.txt`, `.md`: UTF-8로 읽고, 안 되면 CP949로 읽는다.
  - `.html`: 스크립트와 스타일을 뺀 텍스트만 쓴다.
  - 파일 50 MB 이하, 추출 텍스트 500~2,000,000자만 받는다. 계획 하나에는 문서 20개, 텍스트 합계 10,000,000자까지만 받는다(`USER_DOCUMENTS_TOO_MANY`, `USER_DOCUMENTS_TOO_LARGE`). 개수는 파일을 읽기 전에 확인하고, PDF는 상한을 넘는 쪽에서 추출을 멈춘다. 스캔 PDF처럼 텍스트 층이 없으면 `USER_DOCUMENT_TEXT_TOO_SHORT`로 거부한다.
- **연결**
  - 문서는 `claim_refs`에 든 claim의 호출, 또는 `cites`와 같은 URL을 `source_urls`로 인용한 호출에 붙는다.
  - 어느 호출에도 붙지 않는 문서는 `USER_DOCUMENT_NOT_ATTACHED`로 거부한다. 선택 범위를 좁혀 빠진 경우도 마찬가지다.
  - 기록에 없는 claim을 가리키면 `USER_DOCUMENT_CLAIM_REF_NOT_RECORDED`다.
- **확인**
  - 계획 ID에는 각 문서의 digest와 `cites`가 들어간다. 미리보기 뒤에 파일이 바뀌면 `VERIFICATION_PLAN_NOT_CONFIRMED`다.
  - 같은 파일을 같은 출처로 두 번 주면 한 번만 보내고 `claim_refs`를 합친다.
- **SARA의 판단**
  - SARA는 인용 출처를 직접 가져와 제목과 초록이 문서에 들어 있는지 대조한다. 일치하는 문서만 원문 근거로 쓴다.
  - 기본값에서는 그 문서만으로 `VERIFIED`·`CONTRADICTED`가 되지 않는다. 운영자가 SARA에 `SARA_TRUST_USER_DOCUMENTS=1`을 켜야, 인용 출처의 신뢰 도메인 정책에 따라 승격된다.
  - 판정에 쓰이면 `USER_SUPPLIED_DOCUMENT_USED`가 남는다.
- **노출**
  - 문서 전체는 로컬에서 실행되는 SARA 프로세스까지만 간다. 외부 provider에는 claim마다 최대 30,000자 발췌가 간다.
  - 파일 이름과 `claim_refs`는 보내지 않는다.
  - 유료 논문 원문을 외부 provider에 보내도 되는지는 그 문서의 이용 조건에 따라 사용자가 판단해야 한다.
