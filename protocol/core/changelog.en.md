# Changelog

## v2.0 — Extensive Co-Thoughts Architecture

- Upgraded the v1.3 linear Deep Path to a state-based Cognitive Architecture.
- Introduced the Cognitive Router; separated Width and Depth; introduced the Depth Engine and Source Dialogue (provisional project term).
- Introduced the Source Context Supply Chain and Temporal / Interpretive Context.
- Introduced Socratic Examination, Aporia, Premise Ledger, SARA Knowledge Gate / Thought Gate, provenance axes, Project Adapter, and attribution / temporal / source-fidelity violations.
- Preserved v1.3 as the historical baseline.

### v2.0+ — SARA Verification Output Policy v1.0

- Defined SARA verification as a Verification → Revision → Re-verification loop rather than a post-hoc evaluation.
- Introduced always-on verification with progressive disclosure and summary-level warnings for critical findings.
- Clarified boundaries among Claim, Evidence, Verification, Uncertainty, and Human Judgment.
- Introduced Evidence Coverage, Verification Coverage, and Inference Ratio; restricted unsupported Accuracy / Recall / Confidence metrics.
- Separated Replication Stability from Model Agreement and used auditable Claim → Evidence → Verification → Revision summaries instead of raw internal chain-of-thought.
- Policy: `protocol/sara_verification_output_policy_v1.0.md`; status: PROPOSED / PROJECT INTEGRATION.

### Compatibility and migration

Core v1.3 principles remain in v2.0. Do not overwrite v1.3; use v2.0 as canonical baseline.

## v2.0++ — Research Note One-Stop Adapter v0.1

- Added explicit `/연구노트` and `/변환` triggers and accepted unambiguous natural-language requests.
- Defined Research Note Engine → Existing-Note Consistency → Notion Mapping → Create/Update → Post-write Verification.
- Defined NEW / REVISION / EXTENSION / NO_CHANGE / BLOCKED; separated persistence from epistemic verification.
- Prohibited bypassing locked/inaccessible targets and misreporting failed writes as saved.

## v2.0+++ — T51–T56 Research Note Disclosure / Full-Pipeline Integration

- Added T51–T56 authorship disclosure, attribution, rendering, multi-note provenance, and full-pipeline regression test specifications.
- Established artifact-level disclosure and a provenance model using a visible marker, provenance block, `confession_report`, and human-review status.
- Confirmed compatibility for the tested scope; live Notion persistence and broad empirical generation validation remain OPEN / CAPABILITY-BOUND.
- No new epistemic entity or Notion database was introduced. Human remains the final epistemic decision authority.

## 2026-10-25 — Problem-Solving Co-Thinking Guidance v0.1 (provisional)

- Added the Korean guidance and English companion under `protocol/core/`.
- Mapped the stage-by-stage review to existing v2.0 operations without replacing the canonical architecture.
- Added guidance for problem framing, competing causal hypotheses, stakeholder frames, fact/value/inference separation, provisional solution hypotheses, feasibility/consequence evaluation, and Human–AI Hypothesis Delta.
- Clarified SARA's independent, repeated verification boundary, honest NOT RUN / UNVERIFIED / BLOCKED reporting, and re-verification after material changes.
- Separated execution state, epistemic verification state, and provisional solution state.
- Status: ACTIVE GUIDANCE CANDIDATE / DESIGN-LEVEL; runtime implementation, CI, and empirical performance remain unverified.

---

[Korean source](changelog.md)

## 2026-10-25 — Verification-Domain Routing Addendum (guidance v0.1)

- Added pre-hypothesis domain scanning and post-hypothesis domain reassessment to the provisional problem-solving guidance.
- Added a provisional top-level verification-domain taxonomy inspired by academic classifications, without claiming it is an official universal taxonomy.
- Added claim-level primary/secondary tags, criticality, temporal sensitivity, evidence strategy, unresolved-domain reporting, and risk/decision-impact prioritization.
- Added domain-fit examples for law, health/sciences, data/statistics, finance/operations, social science/policy, humanities, ethics, and spatial/housing issues.
- Added test candidates for domain routing, source-fit, and verification efficiency. Runtime automation and measured cost reduction remain unverified.

### 2026-10-25 — Verification-Domain Routing Reference Implementation

- Added deterministic keyword-based domain routing to `src/co_thoughts/cognitive_router.py`, with optional pre/post solution scans and caller-supplied claim tagging.
- Returned evidence-strategy hints, high-risk cross-tags, and temporal-sensitivity hints while keeping verification status `UNVERIFIED`.
- Added unit regression cases for domain identification, new post-solution domains, low-signal tasks, public route integration, and malformed claims.
- Verified: all 30 unit and integration tests pass. Claim extraction, evidence retrieval, SARA execution, and the complete problem-solving workflow are not implemented.

### 2026-10-25 — On-Demand Problem-Solving Workflow Clusters

- Added `CognitiveRuntime.run_workflow()` for explicit single-cluster invocation: problem diagnosis, solution design, feasibility review, or hypothesis delta.
- Each request carries only the selected cluster's stages and existing operation hints and uses one backend call; ordinary `run()` remains available.
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
- Tool outputs remain unverified observations; plans never invoke tools automatically. Concrete service adapters and credentials remain host-provided.
- Added tests for need routing, availability checks, no-auto-execution, default-deny behavior, side-effect gating, and non-promotion of tool output. Full suite: 44 passed.

### 2026-10-25 — Default SARA v2.4 Adapter Connection

- Connected `CognitiveRuntime` by default to the sibling SARA v2.4 epistemic-state adapter, configurable with `CO_THOUGHTS_SARA_V24_ROOT`.
- Runtime assessments validate claim-state and attribution constraints after generation and reset backend-supplied claim verification labels to `UNVERIFIED`.
- Missing adapters fail closed with `NOT_CONNECTED`; adapter execution is explicitly not source search or factual truth verification. SARA v2.5 live judgment/source-verification providers remain separately configured.
- Added default-connection, injection, missing-adapter, and runtime-boundary tests. Full suite: 48 passed.
