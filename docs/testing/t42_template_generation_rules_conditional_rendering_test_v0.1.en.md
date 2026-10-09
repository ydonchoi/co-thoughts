# T42 — Template Generation Rules / Conditional Rendering Test v0.1

Status: **PASS — CONDITIONAL RENDERING RULES DEFINED**

## 1. Purpose
T42 defines how the Research Note generator decides whether a template section is rendered, omitted, marked unresolved, or escalated for human decision.

The objective is to prevent pressure to complete templates from producing unsupported Claims, Evidence, Relations, mechanisms, predictions, evaluation criteria, literature findings, or verification states.

This test builds on the T39 common contract, T40 D1–D9 template specification, and T41 knowledge-object mapping.

## 2. Core Principle
A template is a rendering contract, not a completeness mandate.

The generator must prioritize:

**semantic validity > provenance preservation > epistemic safety > document-type structure > completeness > stylistic completeness**

A missing value is not a defect to be silently filled. When a required or materially relevant section lacks information, the absence must be explicitly represented.

## 3. Section Rendering States

Every section is assigned one of five outcomes.

### R1 — RENDER
Use when the section applies, sufficient input/object references exist, and rendering does not require unsupported inference.

### R2 — RENDER_MISSING_STATE
Use when the section is REQUIRED and applicable, but necessary information is unavailable, unestablished, unresolved, or requires verification.

Allowed labels:
- NOT_AVAILABLE
- NOT_ESTABLISHED
- NOT_APPLICABLE
- REQUIRES_VERIFICATION
- UNRESOLVED

These are presentation/operational states, not replacements for canonical epistemic states.

### R3 — OMIT
Use when a CONDITIONAL or OPTIONAL section's trigger is not met. Omission must not conceal a required unresolved issue.

### R4 — ESCALATE
Use when generation requires a material human epistemic/methodological decision or when competing interpretations materially affect the Research Object, Claim, classification, or conclusion.

The generator must not resolve such cases by guessing.

### R5 — BLOCK
Use when required inputs cannot be safely obtained, provenance/object identity is materially ambiguous, a safety invariant would be violated, or mutation would be unsafe.

A non-mutating candidate may still be generated where allowed, but the blocked condition must be reported.

## 4. Rendering Decision Order
For every section:
1. Applicability
2. Required / Conditional / Optional status
3. Input availability
4. Object identity and provenance
5. Evidence / transformation sufficiency
6. Epistemic and verification constraints
7. Need for human decision
8. Rendering outcome

No later step may override a safety failure detected earlier.

## 5. Required-Section Rule
A REQUIRED section must appear in the generated representation even when substantive content is unavailable, unless it is genuinely NOT_APPLICABLE and the template permits that state.

**REQUIRED + unavailable → explicit missing-state representation**, not fabricated content.

Examples:
- D6.04 Evidence with no identified Evidence → NOT_AVAILABLE / REQUIRES_VERIFICATION
- D7.03 Evaluation Criteria with no established criteria → NOT_ESTABLISHED / REQUIRES_VERIFICATION
- D8.03 Search/Screening when no review search was performed → report the actual state; do not fabricate a search procedure
- D5.10 Evidence with no mechanism Evidence → NOT_AVAILABLE; do not invent support for a mechanism

## 6. Conditional-Section Rule
A CONDITIONAL section renders only when its trigger condition is met.

General form:
- if Trigger(section) = TRUE → evaluate and render;
- if Trigger(section) = FALSE → OMIT;
- if Trigger(section) = UNKNOWN and material → ESCALATE or RENDER_MISSING_STATE.

Examples:
- D1.05 Patterns / Clues → an identifiable pattern or clue is present.
- D4.08 Causal Interpretation → causal interpretation is materially part of the analysis and its Evidence basis can be represented.
- D5.08 Mediation / Moderation / Feedback → such a structure is supported or explicitly modeled.
- D6.08 Alternative Scenarios → alternatives materially affect the forecast.
- D8.09 Disagreement / Debate → disagreement or heterogeneity is present.
- D9.07 Conflict → source-note Claims or Relations conflict.

## 7. Optional-Section Rule
OPTIONAL sections may be rendered when they add material analytical value. They must not be rendered merely to make a note appear more complete.

Optional rendering must never introduce unsupported Claims, invented Evidence, unrecorded Verification, inferred Relations presented as established, fabricated methodology, fabricated numerical values, fabricated literature searches, or fabricated causal mechanisms.

## 8. Missing-State Rule
Select missing-state labels according to the actual reason for absence.

| Condition | Preferred state |
|---|---|
| Information was not obtained | NOT_AVAILABLE |
| Concept/relationship has not been established | NOT_ESTABLISHED |
| Section does not apply | NOT_APPLICABLE |
| Verification is needed before assertion | REQUIRES_VERIFICATION |
| Competing or unresolved states remain | UNRESOLVED |

The generator must not use NOT_AVAILABLE to mask an actual contradiction or use VERIFIED merely because a section was generated.

## 9. Object-Preservation Rule
Rendering must preserve the distinctions established by T41:
- Section ≠ Research Object
- Section ≠ Claim
- Section ≠ Evidence
- Section ≠ Transformation Event
- Section ≠ Verification
- Section ≠ Relation

When a section contains multiple Claims or Evidence items, retain object-level references where material.

When a section represents a derived result and the derivation materially affects interpretation, reference the relevant Transformation Event.

## 10. No-Inference-Filling Rule
The generator must never infer missing content solely from a section title or Document Type.

Examples:
- “Evidence” does not create Evidence.
- “Verification Status” does not create Verification.
- “Relational Structure” does not create a typed Relation.
- “Synthesis” does not create a verified Claim.
- “Prediction Result” does not create a future fact.
- “Judgment” does not create evaluation criteria.
- “Provisional Mechanism” does not justify an invented mechanism.
- “Agreement” does not justify collapsing disagreement.
- “Integrated Explanation / Model” does not imply D9 PROMOTED.

## 11. Document-Type Reclassification Rule
Template selection remains subordinate to the actual Research Object and Research Purpose.

If generation reveals that the selected Document Type materially misrepresents the information structure:
1. stop forced rendering;
2. record the classification conflict;
3. re-evaluate Research Purpose / Question / Document Type;
4. reclassify when justified;
5. regenerate using the appropriate template.

The generator must not distort content to fit a preselected template.

Reclassification does not itself prove the original classification was erroneous; it is a controlled classification revision.

## 12. Human Escalation Conditions
Escalation is required when generation cannot safely determine:
- Research Object boundary;
- a materially consequential Research Question;
- primary versus secondary Research Purpose;
- competing Document Type classification;
- whether a Claim is supported or only hypothesized;
- whether Evidence permits causal/mechanistic interpretation;
- evaluation criteria that materially affect judgment;
- whether conflicting Claims can legitimately be integrated;
- whether a D9 candidate satisfies a promotion condition;
- whether a revision changes the principal proposition set.

The system may propose alternatives, but the unresolved decision must remain visible.

## 13. Conditional Analytical Modules
Analytical modules follow the same rendering rules as sections.

Examples:
- Evidence Mapping → Claims and identifiable Evidence coexist.
- Claim Decomposition → truth-evaluable propositions require separation.
- Counter-evidence → contradictory or limiting Evidence exists.
- Competing Explanation → materially plausible alternatives exist.
- Comparison → multiple comparable objects/Claims are present.
- Scenario Analysis → conditional futures are relevant.
- Evaluation Criteria → evaluation is the actual analytical task.
- Literature Screening → a literature-review workflow is actually performed.
- SARA → Verification / Revision / Re-verification exists or is required.
- D9 Gate → the object is subject to D9 integration/promotion.

Modules do not automatically create the underlying logical objects.

## 14. Minimal Sufficient Representation Test
The generator passes the minimality test when:
1. all applicable REQUIRED sections are represented;
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
| D4 | direction/form, comparison, impact possibility, causal interpretation, alternatives, counter-evidence |
| D5 | tentative mechanism, mediation/moderation/feedback, alternatives, counter-evidence |
| D6 | alternative scenarios, thresholds, uncertainty analysis |
| D7 | outcomes, process, alternatives, improvement/decision implications |
| D8 | concepts, literature flow, convergence, disagreement, methodological differences, gaps |
| D9 | commonalities, tensions, supporting relations, conflicts, integrated explanation/model |

The matrix is a generation aid, not a replacement for T40 section-level contracts.

## 16. Safety Regression Tests

- **G1 — Empty-slot pressure:** required section lacks Evidence → RENDER_MISSING_STATE. **PASS.**
- **G2 — Unsupported conditional section:** no identifiable pattern for D1.05 → OMIT. **PASS.**
- **G3 — Section-name inflation:** D5.10 Evidence requested without source-derived Evidence → no fabricated Evidence; missing state or escalation. **PASS.**
- **G4 — Verification inflation:** D4.12 display without a Verification Event → display only actual state; no fabricated record. **PASS.**
- **G5 — Causal inflation:** correlational Evidence with D4 causal interpretation requested → retain association; mark causal interpretation unsupported/unresolved or escalate. **PASS.**
- **G6 — Prediction inflation:** D6 forecast requested from incomplete conditions → expose assumptions/uncertainty and avoid wording it as future fact. **PASS.**
- **G7 — D9 promotion inflation:** integrated structure without passing D9 Gate → candidate structure only; D9 remains CANDIDATE or NOT_APPLICABLE as appropriate. **PASS.**
- **G8 — Classification forcing:** D5 selected but Evidence indicates D3 conceptual analysis → reclassification, not forced D5 completion. **PASS.**
- **G9 — Missing critical decision:** evaluation judgment depends on an unstated normative criterion → ESCALATE / REQUIRES_VERIFICATION; do not invent the criterion. **PASS.**
- **G10 — Persistence separation:** note successfully persisted → persistence does not upgrade Claim epistemic or Verification state. **PASS.**

## 17. Overall Result
**T42 = PASS**

Conditional-rendering rules are sufficiently defined to connect D1–D9 section contracts to generation behavior without expanding the core knowledge-object model.

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
This is a project-level operational specification and test result, not an established academic or industry standard. The human remains the final epistemic decision authority.

---

[Korean source](t42_template_generation_rules_conditional_rendering_test_v0.1.md)
