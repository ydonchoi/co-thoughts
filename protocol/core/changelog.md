# Changelog

## v2.0 — Extensive Co-thoughts Architecture

- v1.3 linear Deep Path를 state-based Cognitive Architecture로 승격
- Cognitive Router 도입
- Width / Depth 분리
- Depth Engine 및 Source Dialogue (가칭) 도입
- Source Context Supply Chain 도입
- Temporal & Interpretive Context 도입
- Historical / Contemporary / Modern Interpretation 분리
- Socratic Examination 및 Aporia state 도입
- Premise Ledger 도입
- SARA Knowledge Gate / Thought Gate 인터페이스 정의
- Attribution / Temporal / Provenance 축 추가
- Project Adapter Interface 도입
- Attribution / Temporal / Source Fidelity violations 추가
- v1.3을 historical baseline으로 보존

### v2.0+ — SARA Verification Output Policy v1.0

- SARA 검증을 사후 평가가 아닌 Verification → Revision → Re-verification loop로 명시
- Always-on verification / progressive disclosure 원칙 도입
- 기본 출력은 핵심 검증 상태만 표시하고 상세 Audit은 요청 시 확장
- Critical finding은 사용자 요청 없이도 요약 수준에서 경고
- Claim / Evidence / Verification / Uncertainty / Human Judgment 경계 명시
- Evidence Coverage / Verification Coverage / Inference Ratio 도입
- 기존 Accuracy / Recall / Confidence 등의 비엄밀한 메타 수치 사용을 제한
- Replication Stability / Model Agreement를 각각 재현 안정성과 모델 간 합의로 분리
- 내부 chain-of-thought 대신 감사 가능한 Claim → Evidence → Verification → Revision 요약을 사용
- 정책 문서: `protocol/sara_verification_output_policy_v1.0.md`
- Status: PROPOSED / PROJECT INTEGRATION

### Compatibility

v1.3의 Human Agency, Anti-Sycophancy, Epistemic Separation, Revision over Consistency, Information Gain, Non-Monotonic Revision, Checkpoint / State–Evidence Separation은 v2.0에서 유지된다.

### Migration Rule

v1.3 문서를 덮어쓰지 않는다. v2.0을 canonical active version으로 사용한다.

### v2.0++ — Research Note One-Stop Adapter v0.1

- `/연구노트` 및 `/변환` 명시적 호출어 도입
- 의도가 명확한 자연어 연구노트 요청을 호출어로 수용
- Research Note Engine → Existing-note Consistency → Notion Mapping → Create/Update → Post-write Verification 원스톱 흐름 정의
- NEW / REVISION / EXTENSION / NO_CHANGE / BLOCKED 결과 상태 정의
- Notion persistence와 epistemic verification을 분리
- 잠금/접근불가 대상 우회 금지 및 실패 저장 오보고 금지
- Canonical adapter protocol: `protocol/research_note_one_stop_pipeline_v0.1.md`

## v2.0+++ — T51–T56 Research Note Disclosure / Full-Pipeline Integration

- Added T51 AI Authorship Disclosure / Provenance Transparency Test.
- Added T52 Real-Conversation Research Note Attribution Regression Test.
- Added T53 Cross-Document-Type AI Disclosure Regression Test.
- Added T54 AI Disclosure Rendering / Actual Research Note Output Test.
- Added T55 Multi-Note AI Disclosure / Provenance Consistency Test.
- Added T56 Research Note Full-Pipeline Output Regression Test.
- Established mandatory artifact-level disclosure: **AI 작성·구조화 연구노트**.
- Established cross-cutting provenance model using visible marker + provenance block + existing `confession_report` + human-review status.
- Added optional local provenance distinctions A1 AI-generated, A2 AI-structured, A3 Human-authored, A4 Human-edited, A5 Source-derived; uncertain local attribution must not be fabricated.
- Confirmed compatibility with D1–D9, NEW / REVISION / EXTENSION / NO_CHANGE / BLOCKED, Branch/Merge, D9, and human post-editing for tested scope.
- Full-pipeline semantic integration is CLOSED FOR TESTED SCOPE.
- Live Notion persistence and broad empirical generation validation remain OPEN / CAPABILITY-BOUND.
- No new epistemic entity or Notion database introduced.

Human remains final epistemic decision authority.

## 2026-10-25 — Problem-Solving Co-Thinking Guidance v0.1 (provisional)

- Added `protocol/core/problem_solving_cothinking_guidance_v0.1.md` and its English companion.
- Mapped the prior stage-by-stage comparison to existing v2.0 operations without replacing the canonical architecture.
- Added guidance for problem framing, competing causal hypotheses, stakeholder frames, fact/value/inference separation, provisional solution hypotheses, feasibility/consequence evaluation, and Human–AI Hypothesis Delta.
- Clarified SARA's independent, repeated verification boundary across relevant stages, including honest NOT RUN / UNVERIFIED / BLOCKED reporting and re-verification after material changes.
- Explicitly separated execution state, epistemic verification state, and provisional solution state.
- Status: ACTIVE GUIDANCE CANDIDATE / DESIGN-LEVEL; runtime implementation, CI, and empirical performance remain unverified.

### 2026-10-25 — Verification-Domain Routing Addendum (guidance v0.1)

- Added a pre-hypothesis domain scan and a post-hypothesis domain reclassification step to the provisional problem-solving guidance.
- Added a provisional top-level verification-domain taxonomy inspired by academic classifications, without claiming to adopt a single official taxonomy.
- Added claim-level primary/secondary domain tags, criticality, temporal sensitivity, evidence/source strategy, unresolved-domain reporting, and risk/decision-impact-based verification prioritization.
- Added domain-fit verification examples for law, health/sciences, data/statistics, finance/operations, social science/policy, humanities, ethics, and spatial/housing questions.
- Added regression-test candidates for domain routing, source-fit, and verification efficiency. No runtime automation or measured cost reduction is claimed.

### 2026-10-25 — Verification-Domain Routing Reference Implementation

- Added deterministic, keyword-based domain routing to `src/co_thoughts/cognitive_router.py`, including optional pre/post solution scans and caller-supplied claim tagging.
- Returned evidence-strategy hints, high-risk cross-tags, and temporal-sensitivity hints while keeping verification status `UNVERIFIED`.
- Added unit regression cases for domain identification, newly introduced post-solution domains, low-signal tasks, public route integration, and malformed claims.
- Verified: all 30 unit and integration tests pass. This does not implement claim extraction, evidence retrieval, SARA execution, or the complete problem-solving workflow.

### 2026-10-25 — On-Demand Problem-Solving Workflow Clusters

- Added `CognitiveRuntime.run_workflow()` for explicit single-cluster invocation: problem diagnosis, solution design, feasibility review, or hypothesis delta.
- Each request carries only the selected cluster's stages and existing operation hints and uses one backend call; ordinary `run()` behavior remains available.
- Added regression tests for one-call execution, unknown workflow rejection, and inclusion in the user-mediated prompt. Full suite: 33 passed.
- These are cluster-level backend prompts, not deterministic per-stage execution or SARA verification.

### 2026-10-25 — Natural-Language Workflow Routing

- Added Korean and English trigger phrases for the four on-demand workflow clusters.
- Exposed routing status and candidates through `CognitiveRouter.route()` and added `CognitiveRuntime.run_natural_language()` as the NL dispatch entry point.
- Unmatched requests use the normal run path; ambiguous multi-cluster requests stop before backend execution.
- Added regression coverage for both languages, fallback, ambiguity, and zero-call behavior. Full suite: 37 passed.

### 2026-10-25 — External Tool Need Planning and Adapter Boundary

- Added workflow-level tool need assessment for web/source search, calculation, dataset analysis, and spatial lookup.
- Added a provider-neutral `ToolRegistry`, connection availability reporting, and explicit runtime invocation guarded by default-deny tool and side-effect policies.
- Tool outputs are retained as unverified observations; plans never invoke tools automatically. Concrete service adapters and credentials remain host-provided.
- Added tests for need routing, availability checks, no-auto-execution, default-deny behavior, side-effect gating, and non-promotion of tool output. Full suite: 44 passed.

### 2026-10-25 — Default SARA v2.4 Adapter Connection

- Connected `CognitiveRuntime` by default to the sibling SARA v2.4 epistemic-state adapter, configurable with `CO_THOUGHTS_SARA_V24_ROOT`.
- Runtime assessments validate claim-state and attribution constraints after generation and reset backend-supplied claim verification labels to `UNVERIFIED`.
- Missing adapters fail closed with `NOT_CONNECTED`; adapter execution is explicitly not source search or factual truth verification. SARA v2.5 live judgment/source-verification providers remain separately configured.
- Added default-connection, injection, missing-adapter, and runtime-boundary tests. Full suite: 48 passed.
