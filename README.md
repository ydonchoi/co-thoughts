# 사고 메모 및 심화 대화 프로토콜

> Human–AI Co-Thinking Protocol for Exploratory Dialogue, Critical Examination, Source-grounded Depth, Verification, and State Management

[![Version](https://img.shields.io/badge/version-v2.0%2B%2B%2B-blue.svg)](#current-status)

## 프로젝트 소개

**사고 메모 및 심화 대화 프로토콜**은 인간과 LLM의 대화를 단순 질의응답이 아니라 공동사고(Co-Thinking) 과정으로 운영하기 위한 모듈형 인지 아키텍처다.

v2.0에서는 v1.3의 핵심 원칙을 유지하면서 선형 Deep Path를 **state-based Cognitive Architecture**로 확장한다.

## 핵심 철학

> **우리는 서로의 생각을 확인하기 위해서가 아니라, 서로의 생각을 수정할 수 있기 위해 대화한다.**

인간은 최종 판단자이자 책임 주체다. LLM은 사고 확장, 구조화, 반론, 경쟁 설명, Socratic examination, source-grounded dialogue, 검증 보조 및 상태 관리 역할을 수행한다.

## v2.0 Architecture

~~~text
HUMAN / Final Agency
        ↓
EXTENSIVE CO-THOUGHTS
        ↓
COGNITIVE ROUTER
 ├─ WIDTH: Explore / Counter / Compete
 ├─ DEPTH: Source Dialogue / Context Expansion
 ├─ EXAMINE: Premise / Socratic
 ├─ VERIFY: SARA / verification system
 └─ SYNTHESIZE / REVISE
        ↓
EPISTEMIC STATE
        ↓
CHECKPOINT
        ↓
PROJECT ADAPTER
~~~

Co-thoughts는 모든 모듈을 순차 실행하지 않는다. Cognitive Router가 현재 사고 상태에 필요한 작업을 선택한다.

## Width × Depth

**WIDTH**는 Explore / Counter / Compete / Relate / Generalize / Alternative를 통해 가능 공간을 넓힌다.

**DEPTH**는 Source → Claim → Premise → Argument → Background → Evidence → Boundary → Counter-evidence → Revision으로 하나의 지식 객체 내부로 내려간다.

## Source Dialogue (가칭)

논문·책·보고서·이론·정책문서 등을 source-grounded interlocutor로 변환하여 인간과 직접 논쟁할 수 있게 한다.

SOURCE / INTERPRETATION / INFERENCE / SIMULATION / OUTSIDE를 구분하며 실제 저자와 동일시하지 않는다.

## Temporal & Interpretive Context

- HISTORICAL — 당시 이용 가능했던 지식
- POST_PUBLICATION — 출판 이후의 지식
- CONTEMPORARY — 현재 지식
- MODERN_INTERPRETATION — 현재 관점의 재해석

핵심 불변식:

> **MODERN_INTERPRETATION ≠ AUTHOR_CLAIM**

현대적 해석은 허용하지만 역사적 귀속과 분리한다.

## Socratic Examination

Claim → Premise Extraction → Premise Classification → Critical Premise Selection → Question / Counterexample → Human Response → Premise Update.

Aporia는 실제 논리적 충돌이 확인된 경우에만 선언한다.

## SARA Dual Gate

**Knowledge Gate:** External Source → Context Expansion → SARA → Evidence/Claim/Context Validation → Depth

**Thought Gate:** Human ↔ Co-thoughts → Inference/New Claim → SARA → Epistemic State → Revision

### SARA Verification Output

SARA 검증은 답변의 마지막에 붙는 단순 사후 평가가 아니라 **Verification → Revision → Re-verification** 품질관리 루프로 동작한다.

사용자에게는 **Always-on verification + progressive disclosure** 원칙을 적용한다.

- 기본 출력: 검증 상태와 핵심 요약만 표시
- 중요 문제가 발견되면 요약 수준에서 경고
- 사용자가 요청하면 Claim / Evidence / Verification / Uncertainty / Revision / Provenance의 상세 Audit을 제공
- 내부 chain-of-thought는 노출하지 않고 감사 가능한 검증 경로만 제공
- Agreement와 Model Agreement는 Evidence 또는 Truth의 대체물로 사용하지 않음

상세 정책은 [protocol/sara_verification_output_policy_v1.0.md](protocol/sara_verification_output_policy_v1.0.md)에 정의한다.

## Research Note One-Stop Adapter

Research-note generation is callable through `/연구노트`, `/변환`, or unambiguous natural-language equivalents. The adapter routes the request through the Research Note Engine and, when the Notion persistence path is available, performs existing-note consistency check → generation → Notion mapping → create/update → post-write verification in one continuous workflow.

Canonical operational contract: `protocol/research_note_one_stop_pipeline_v0.1.md`.

Persistence is not verification. Locked or inaccessible Notion targets are not bypassed, and failed writes are never reported as saved.

## Research Note AI Authorship Disclosure

Every Research Note generated/structured through the Research Note Engine must carry an explicit artifact-level disclosure:

> **AI 작성·구조화 연구노트**

The disclosure is a provenance/presentation layer, not an epistemic state. It is accompanied by generation provenance and human-review status, using the existing `confession_report` representation where available.

The project distinguishes, when provenance is sufficiently reliable:
- A1 AI-generated
- A2 AI-structured
- A3 Human-authored
- A4 Human-edited
- A5 Source-derived

AI participation does not imply that every proposition or token originated from AI. AI generation is not Evidence or Verification, and persistence is not Verification. When local attribution is uncertain, the artifact-level disclosure is retained and false precision is avoided.

T51–T56 establish this disclosure as a cross-cutting layer across D1–D9 and the tested lifecycle states. No separate authorship entity or Notion database is currently justified.

## Project Adapter

PROJECT_CONTEXT / DOMAIN_RULES / EVIDENCE_POLICY / ALLOWED_OPERATIONS / OUTPUT_SCHEMA / DECISION_BOUNDARY를 통해 SARA, Research, Recruitment 등 다른 프로젝트에 연결한다.

## Core Invariants

~~~text
MODE ≠ OPERATION
MODE ≠ STATE
CLAIM ≠ PREMISE
STATE ≠ EVIDENCE
EVIDENCE ≠ VERIFICATION
VERIFICATION ≠ AGREEMENT
AGREEMENT ≠ EVIDENCE
SOURCE ≠ SIMULATION
AUTHOR_CLAIM ≠ MODERN_INTERPRETATION
HISTORICAL ≠ CONTEMPORARY
CHECKPOINT ≠ EVIDENCE
~~~

## Version History

| Version | Focus |
|---|---|
| v1.0 | 기본 공동사고 프로토콜 |
| v1.1 | 운영 규칙·동적 모드 |
| v1.2 | 상태 외부화·Transition Gate |
| v1.3 | Claim/Evidence/Verification 분리 및 T1~T13 검증 |
| **v2.0** | **Extensive Co-thoughts Architecture** |
| **v2.0+** | **SARA Verification Output Policy v1.0** |
| **v2.0++** | **Research Note One-Stop Adapter / Notion Persistence Contract v0.1** |
| **v2.0+++** | **AI Authorship Disclosure / Provenance + Full-Pipeline Regression T51–T56** |
| **v2.0+++** | **Research Note Template Standardization + AI Authorship/Provenance Disclosure + T51–T56 integration** |

v1.3 문서는 historical baseline으로 보존한다.

## Current Status

**Version:** v2.0+++  
**Status:** ACTIVE / ARCHITECTURAL BASELINE  

T51–T56: AI authorship disclosure/provenance and full-pipeline semantic integration **CLOSED FOR TESTED SCOPE**. Live Notion persistence and broad empirical generation validation remain **OPEN / CAPABILITY-BOUND**.

SARA Verification Output Policy v1.0: **PROPOSED / PROJECT INTEGRATION**

Research Note One-Stop Adapter v0.1: **PROJECT INTEGRATION / OPERATIONAL PROTOCOL CANDIDATE**

Research Note Template Contract T39 / D1–D9 Template Specification T40: **PASS / PROJECT-LEVEL**

AI Authorship Disclosure T51–T55: **CLOSED FOR TESTED SCOPE**

Full-Pipeline Regression T56: **CONDITIONAL PASS / SEMANTIC INTEGRATION CLOSED FOR TESTED SCOPE; LIVE PERSISTENCE CAPABILITY-BOUND**

## v2.0 Runtime Modules

Implemented modules: `cognitive_router.py`, `epistemic_state.py`, `context.py`.

- Router selects minimal cognitive operations.
- Epistemic state separates Claim/Premise and supports non-monotonic revision.
- Context module enforces temporal/attribution boundaries.
- Cognitive output remains `UNVERIFIED` and non-evidence until SARA independently evaluates it.
 
## Research Note AI Authorship / Provenance Disclosure

All Research Notes generated or structured through the Research Note Engine must disclose AI participation at the artifact level.

Canonical visible marker:

**AI 작성·구조화 연구노트**

The disclosure is a provenance/presentation layer, not an epistemic state, Evidence, Verification, or Document Type. It is implemented through:

- visible artifact marker;
- generation provenance;
- existing `confession_report` disclosure/provenance field;
- independently reported human-review status.

Where local provenance is sufficiently reliable, the system may distinguish:
- A1 AI-generated
- A2 AI-structured
- A3 Human-authored
- A4 Human-edited
- A5 Source-derived

Local attribution must not be fabricated when provenance is uncertain. AI participation does not imply that every token or proposition originated from AI.

AI generation does not imply verification. Persistence does not imply verification. D9 promotion does not imply verification.

T51–T56 establish the disclosure/provenance contract and full-pipeline semantic integration for the tested scope. Live durable persistence and large-scale empirical generation validation remain capability-bound/open.

Canonical tests:
- T51 AI Authorship Disclosure / Provenance Transparency
- T52 Real-Conversation Attribution Regression
- T53 Cross-Document-Type AI Disclosure Regression
- T54 AI Disclosure Rendering / Actual Output
- T55 Multi-Note Disclosure / Provenance Consistency
- T56 Full-Pipeline Output Regression

## Research Note Validation Closure

The tested semantic architecture, template architecture, lifecycle semantics, AI disclosure integration, and full-pipeline semantic integration are **CLOSED FOR TESTED SCOPE**. This does not claim external academic, legal, institutional, or population-level validation.

Live Notion persistence verification remains capability/state dependent. Human remains final epistemic decision authority.

