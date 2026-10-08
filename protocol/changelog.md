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
