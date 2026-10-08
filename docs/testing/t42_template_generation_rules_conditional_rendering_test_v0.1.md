# T42 — Template Generation Rules / Conditional Rendering Test v0.1

Status: **PASS — CONDITIONAL RENDERING RULES DEFINED**

## 1. Purpose

T42 defines how the Research Note generator decides whether a template section is rendered, omitted, marked unresolved, or escalated for human decision.

The objective is to prevent template-completion pressure from producing unsupported Claims, Evidence, Relations, mechanisms, predictions, evaluation criteria, literature findings, or verification states.

This test operates on the T39 common contract, T40 D1–D9 template specification, and T41 knowledge-object mapping.

## 2. Core Principle

A template is a rendering contract, not a completeness mandate.

The generator must prefer:

**semantic validity > provenance preservation > epistemic safety > document-type structure > completeness > stylistic completeness**

A missing value is not a defect to be silently filled. It is a state that must be represented explicitly when the section is required or materially relevant.

## 3. Section Rendering States

Every section is evaluated into one of five rendering outcomes:

### R1 — RENDER
Use when the section is applicable, sufficient input/object references exist, and rendering does not require unsupported inference.

### R2 — RENDER_MISSING_STATE
Use when the section is REQUIRED and applicable, but necessary information is unavailable, unestablished, unresolved, or requires verification.

Allowed labels:
- NOT_AVAILABLE
- NOT_ESTABLISHED
- NOT_APPLICABLE
- REQUIRES_VERIFICATION
- UNRESOLVED

These labels are presentation/operational states. They do not replace canonical epistemic states.

### R3 — OMIT
Use when the section is CONDITIONAL or OPTIONAL and its trigger condition is not satisfied. Omission must not hide a required unresolved issue.

### R4 — ESCALATE
Use when generation would require a material human epistemic or methodological decision, or when competing interpretations materially affect the Research Object, Claim, classification, or conclusion.

The generator must not resolve such cases by guessing.

### R5 — BLOCK
Use when required inputs cannot be safely obtained, provenance/object identity is materially ambiguous, a safety invariant would be violated, or mutation would be unsafe.

A non-mutating candidate may still be generated where the protocol permits, but the blocked condition must be reported.

## 4. Rendering Decision Order

For every section:

1. Applicability
2. Required / Conditional / Optional status
3. Input availability
4. Object identity and provenance
5. Evidence / transformation sufficiency
6. Epistemic and verification constraints
7. Human-decision requirement
8. Rendering outcome

No later step may override a safety failure detected earlier.

## 5. Required-Section Rule

A REQUIRED section must appear in the generated representation even when substantive content is unavailable, unless it is genuinely NOT_APPLICABLE and the template permits that state.

Therefore:

**REQUIRED + unavailable → explicit missing-state representation**

not:

**REQUIRED + unavailable → fabricated content**

Examples:
- D6.04 근거 with no identified evidence → NOT_AVAILABLE / REQUIRES_VERIFICATION
- D7.03 평가기준 with no established criteria → NOT_ESTABLISHED / REQUIRES_VERIFICATION
- D8.03 검색/선별 when no review search was performed → represent the actual state; do not fabricate a search procedure
- D5.10 근거 with no mechanism evidence → NOT_AVAILABLE; do not invent mechanism support

## 6. Conditional-Section Rule

A CONDITIONAL section renders only when its trigger condition is satisfied.

General form:

if Trigger(section) = TRUE → evaluate and render
if Trigger(section) = FALSE → OMIT
if Trigger(section) = UNKNOWN and material → ESCALATE or RENDER_MISSING_STATE

Examples:
- D1.05 패턴/단서 → identifiable pattern or clue is present.
- D4.08 인과 해석 → causal interpretation is materially part of the analysis and its evidentiary basis can be represented.
- D5.08 매개/조절/피드백 → such structure is supported or explicitly modeled.
- D6.08 대안 시나리오 → alternatives materially affect the forecast.
- D8.09 불일치/논쟁 → disagreement or heterogeneity is present.
- D9.07 충돌 → source-note claims or relations conflict.

## 7. Optional-Section Rule

OPTIONAL sections may be rendered when they provide material analytical value.

They must not be rendered merely to make a note appear more complete.

Optional rendering must never introduce unsupported Claims, invented Evidence, unrecorded Verification, inferred Relations presented as established, fabricated methodology, fabricated numerical values, fabricated literature searches, or fabricated causal mechanisms.

## 8. Missing-State Rule

Missing-state labels must be selected according to the actual reason for absence.

| Condition | Preferred state |
|---|---|
| Information was not obtained | NOT_AVAILABLE |
| Concept/relationship has not been established | NOT_ESTABLISHED |
| Section does not apply | NOT_APPLICABLE |
| Verification is needed before assertion | REQUIRES_VERIFICATION |
| Competing or unresolved states remain | UNRESOLVED |

The generator must not use NOT_AVAILABLE as a substitute for an actual contradiction, and must not use VERIFIED or another epistemic state merely because a section was generated.

## 9. Object-Preservation Rule

Rendering must preserve the distinction established by T41:

- Section ≠ Research Object
- Section ≠ Claim
- Section ≠ Evidence
- Section ≠ Transformation Event
- Section ≠ Verification
- Section ≠ Relation

When a section contains multiple Claims or Evidence items, object-level references should be retained where material.

When a section represents a derived result and the derivation materially affects interpretation, the relevant Transformation Event should be referenced.

## 10. No-Inference-Filling Rule

The generator must never infer missing content solely from the section title or document type.

Examples:
- “근거” does not create Evidence.
- “검증 상태” does not create Verification.
- “관계 구조” does not create a typed Relation.
- “종합” does not create a verified Claim.
- “예측 결과” does not create a future fact.
- “판단” does not create evaluation criteria.
- “잠정 메커니즘” does not justify an invented mechanism.
- “합의” does not justify collapsing disagreement.
- “통합 설명/모델” does not imply D9 PROMOTED.

## 11. Document-Type Reclassification Rule

Template selection remains subordinate to the actual Research Object and research purpose.

If generation reveals that the selected Document Type materially misrepresents the information structure:
1. stop forced rendering;
2. record the classification conflict;
3. re-evaluate Research Purpose / Question / Document Type;
4. reclassify when justified;
5. regenerate using the appropriate template.

The generator must not distort content to fit a preselected template.

Reclassification is not itself evidence that the original classification was erroneous; it is a controlled classification revision.

## 12. Human Escalation Conditions

Escalation is required when automated generation cannot safely determine:
- Research Object boundary;
- materially consequential Research Question;
- primary versus secondary Research Purpose;
- competing Document Type classification;
- whether a Claim is supported or merely hypothesized;
- whether evidence permits causal/mechanistic interpretation;
- evaluation criteria that materially affect judgment;
- whether conflicting claims can legitimately be integrated;
- whether a D9 candidate structure satisfies a promotion condition;
- whether a revision changes the principal proposition set.

The system may propose alternatives, but the unresolved decision must remain visible.

## 13. Conditional Analytical Modules

Analytical modules follow the same rendering rules as sections.

Examples:
- Evidence Mapping → Claims and identifiable Evidence coexist.
- Claim Decomposition → truth-evaluable propositions require separation.
- Counter-evidence → contradictory or limiting Evidence exists.
- Competing Explanation → materially plausible alternatives exist.
- Comparison → multiple comparable objects/claims are present.
- Scenario Analysis → conditional futures are relevant.
- Evaluation Criteria → evaluation is the actual analytical task.
- Literature Screening → a literature-review workflow is actually performed.
- SARA → Verification / Revision / Re-verification activity exists or is required.
- D9 Gate → the object is subject to D9 integration/promotion.

Modules do not create the underlying logical objects automatically.

## 14. Minimal Sufficient Representation Test

The generator passes the minimality test when:
1. all REQUIRED applicable sections are represented;
2. unsupported CONDITIONAL/OPTIONAL sections are omitted;
3. material missing states remain visible;
4. no section is populated solely to satisfy visual completeness;
5. material provenance and object identity are preserved;
6. no epistemic state is upgraded by rendering.

This establishes minimum sufficient representation, not maximum template completion.

## 15. Type-Level Trigger Matrix

| Type | High-value conditional triggers |
|---|---|
| D1 | identifiable patterns, provisional structures, competing interpretations, generated hypotheses |
| D2 | composition/types, distribution, change, patterns/exceptions |
| D3 | definitional disagreement, adjacent concepts, dimensions, competing conceptualizations |
| D4 | direction/form, comparison, impact possibility, causal interpretation, alternatives, counterevidence |
| D5 | tentative mechanism, mediation/moderation/feedback, alternatives, counterevidence |
| D6 | alternative scenarios, thresholds, uncertainty analysis |
| D7 | outcomes, process, alternatives, improvement/decision implications |
| D8 | concepts, literature flow, convergence, disagreement, methodological differences, gaps |
| D9 | commonalities, tensions, support relations, conflicts, integrated explanation/model |

The matrix is a generation aid, not a replacement for the section-level contracts in T40.

## 16. Safety Regression Tests

### G1 — Empty-slot pressure
Input: required section lacks evidence.
Expected: RENDER_MISSING_STATE.
**PASS.**

### G2 — Unsupported conditional section
Input: no identifiable pattern for D1.05.
Expected: OMIT.
**PASS.**

### G3 — Section-name inflation
Input: D5.10 근거 requested without source-derived Evidence.
Expected: no fabricated Evidence; missing state or escalation.
**PASS.**

### G4 — Verification inflation
Input: generated D4.12 verification display without a Verification event.
Expected: display only actual state; do not fabricate Verification record.
**PASS.**

### G5 — Causal inflation
Input: correlational evidence with D4 causal interpretation requested.
Expected: retain association; causal interpretation marked unsupported/unresolved or escalated.
**PASS.**

### G6 — Prediction inflation
Input: D6 forecast requested from incomplete conditions.
Expected: expose assumptions/uncertainty and avoid future-fact wording.
**PASS.**

### G7 — D9 promotion inflation
Input: integrated structure generated without passing D9 Gate.
Expected: candidate structure only; D9 remains CANDIDATE or NOT_APPLICABLE as appropriate.
**PASS.**

### G8 — Classification forcing
Input: selected D5 template but evidence indicates D3 conceptual analysis.
Expected: reclassification path, not forced D5 completion.
**PASS.**

### G9 — Missing critical decision
Input: evaluation judgment depends on an unstated normative criterion.
Expected: ESCALATE / REQUIRES_VERIFICATION; do not invent criterion.
**PASS.**

### G10 — Persistence separation
Input: generated note is successfully persisted.
Expected: persistence does not upgrade Claim epistemic state or Verification state.
**PASS.**

## 17. Overall Result

**T42 = PASS**

Conditional rendering rules are sufficiently defined to connect the D1–D9 section contracts to generation behavior without expanding the core knowledge-object model.

The rules establish:
- required sections → explicit missing state when necessary;
- conditional sections → trigger-based rendering;
- optional sections → value-based rendering;
- unsafe inference → omission, missing state, escalation, or block;
- classification mismatch → controlled reclassification;
- persistence → independent of epistemic verification.

## 18. Remaining Validation Boundary

T42 validates generation-rule semantics, not full real-conversation generation quality.

Remaining tests:
1. real-conversation generation consistency;
2. D1–D9 template selection under ambiguous prompts;
3. composite-section object anchoring in generated notes;
4. derived-section Transformation Trace rendering;
5. verification-display versus Verification-record consistency;
6. output readability and redundancy control.

No new Document Type, logical entity, or Notion schema is justified by T42.

## 19. Boundary

This is a project-level operational specification and test result. It is not presented as an established academic or industry standard.

Human remains final epistemic decision authority.
