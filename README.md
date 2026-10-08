# 사고 메모 및 심화 대화 프로토콜

> Human–AI Co-Thinking Protocol for Exploratory Dialogue, Critical Examination, Source-grounded Depth, Verification, and State Management

[![Version](https://img.shields.io/badge/version-v2.0-blue.svg)](#current-status)

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
- POST_PUBLICATION — 출판 이후 지식
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

v1.3 문서는 historical baseline으로 보존한다.

## Current Status

**Version:** v2.0  
**Status:** ACTIVE / ARCHITECTURAL BASELINE

