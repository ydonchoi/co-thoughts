# T40 — D1–D9 Standard Template Specification v0.1

Status: **PASS — INITIAL OPERATIONAL TEMPLATE SPECIFICATION**

## 1. Purpose

T40 converts the existing D1–D9 document structures into contract-compliant standard templates using T39.

This specification defines section IDs, status, purpose, primary inputs, output intent, omission conditions, and inference constraints.

It does not redefine Research Purpose, Claim, Evidence, Verification, Transformation Event, Relation, or D9 semantics.

## 2. Common Template Rules

All D1–D9 templates inherit:
- Common Metadata
- Common Framing
- Claim/Evidence/Verification separation
- provenance preservation
- uncertainty disclosure
- non-destructive revision
- SARA rendering rules
- missing-information safety

Section statuses: REQUIRED, CONDITIONAL, OPTIONAL.

A REQUIRED section may report NOT_AVAILABLE / NOT_ESTABLISHED / REQUIRES_VERIFICATION / UNRESOLVED rather than fabricate content.

## 3. D1 — Exploratory Research Note

Primary function: structure an inquiry space before the object is sufficiently understood.

| ID | Section | Status | Purpose |
|---|---|---|---|
| D1.01 | Object / Purpose | REQUIRED | define the inquiry target and purpose |
| D1.02 | Current Knowledge | REQUIRED | establish known state and starting evidence |
| D1.03 | Scope | REQUIRED | define inquiry boundary |
| D1.04 | Phenomenon / Problem | REQUIRED | describe observed phenomenon/problem |
| D1.05 | Patterns / Clues | CONDITIONAL | identify evidence-supported signals |
| D1.06 | Provisional Structure | CONDITIONAL | formulate provisional organization/model |
| D1.07 | Competing Interpretations | CONDITIONAL | compare plausible explanations |
| D1.08 | Exploration Results | REQUIRED | summarize what exploration established |
| D1.09 | Generated Hypothesis / Model | CONDITIONAL | record newly generated hypotheses/models |
| D1.10 | Unknown Areas | REQUIRED | identify unresolved knowledge |
| D1.11 | Follow-up Questions | REQUIRED | derive next research questions |

Constraints:
- D1 may generate hypotheses but must not upgrade them to verified Claims.
- Pattern detection requires identifiable input Evidence or explicit observation.
- Competing interpretations must not be invented merely to create balance.

## 4. D2 — Descriptive / Current-State Research Note

Primary function: describe characteristics, composition, distribution, and change.

| ID | Section | Status | Purpose |
|---|---|---|---|
| D2.01 | Object / Purpose / Scope | REQUIRED | define descriptive boundary |
| D2.02 | Observation / Classification Criteria | REQUIRED | state observation/classification basis |
| D2.03 | Characteristics | REQUIRED | describe observed attributes |
| D2.04 | Composition / Types | CONDITIONAL | describe categories/components |
| D2.05 | Distribution | CONDITIONAL | describe distribution when data exist |
| D2.06 | Change | CONDITIONAL | describe temporal/change patterns |
| D2.07 | Patterns / Exceptions | CONDITIONAL | identify recurring patterns or exceptions |
| D2.08 | Summary | REQUIRED | synthesize descriptive findings |
| D2.09 | Limitations / Unknowns | REQUIRED | state coverage and unknowns |

Constraints:
- Description must not silently become causal explanation.
- Absence of observed variation does not prove absence of variation.
- Classification criteria must be explicit when classification affects conclusions.

## 5. D3 — Concept Analysis Research Note

Primary function: analyze meaning, structure, boundaries, dimensions, and competing conceptualizations.

| ID | Section | Status | Purpose |
|---|---|---|---|
| D3.01 | Concept / Question | REQUIRED | define focal concept and question |
| D3.02 | Background | CONDITIONAL | establish historical/theoretical context |
| D3.03 | Major Definitions | REQUIRED | represent relevant definitions |
| D3.04 | Differences Among Definitions | CONDITIONAL | compare definitional variation |
| D3.05 | Core Attributes | REQUIRED | identify defining/central attributes |
| D3.06 | Boundaries | REQUIRED | distinguish inclusion/exclusion |
| D3.07 | Adjacent Concepts | CONDITIONAL | distinguish related concepts |
| D3.08 | Components / Dimensions | CONDITIONAL | structure concept dimensions |
| D3.09 | Concept Relations | CONDITIONAL | map relations to other concepts |
| D3.10 | Competing Conceptualizations | CONDITIONAL | compare competing conceptualizations |
| D3.11 | Adopted Conceptualization | REQUIRED | state adopted working conceptualization |
| D3.12 | Scope / Limitations | REQUIRED | state applicability and limitations |
| D3.13 | Follow-up Questions | REQUIRED | identify unresolved conceptual questions |

Constraints:
- Definitions must preserve attribution/provenance.
- Project interpretation must not be presented as an author's definition.
- A selected conceptualization is not automatically empirically verified.

## 6. D4 — Relation / Impact Analysis Research Note

Primary function: analyze relations, associations, effects, and competing causal interpretations.

| ID | Section | Status | Purpose |
|---|---|---|---|
| D4.01 | Question | REQUIRED | define relation/impact question |
| D4.02 | Objects / Variables / Concepts | REQUIRED | define relational units |
| D4.03 | Existing Explanations | REQUIRED | represent prior explanations |
| D4.04 | Relational Structure | REQUIRED | map relationships |
| D4.05 | Direction / Form | CONDITIONAL | characterize direction/form |
| D4.06 | Comparison / Differences | CONDITIONAL | compare groups/conditions |
| D4.07 | Potential Impacts | CONDITIONAL | assess possible effects |
| D4.08 | Causal Interpretation | CONDITIONAL | state causal interpretation only when warranted |
| D4.09 | Alternative Explanations | CONDITIONAL | identify competing explanations |
| D4.10 | Falsification / Counter-evidence | CONDITIONAL | represent contradictory Evidence |
| D4.11 | Boundary Conditions | REQUIRED | specify conditions/limits |
| D4.12 | Verification Status | REQUIRED | expose relevant verification states |
| D4.13 | Conclusion | REQUIRED | state current relational conclusion |

Constraints:
- Association must not be rendered as causation without adequate support.
- Causal language must track Evidence and verification state.
- Alternative explanations must be evidence-grounded or explicitly marked as hypotheses.

## 7. D5 — Mechanism / Process Analysis Research Note

Primary function: explain how a system or phenomenon operates through processes and mechanisms.

| ID | Section | Status | Purpose |
|---|---|---|---|
| D5.01 | Question | REQUIRED | define mechanism/process question |
| D5.02 | Object | REQUIRED | define system/process boundary |
| D5.03 | Existing Explanations | REQUIRED | represent existing mechanisms/explanations |
| D5.04 | Components | REQUIRED | identify relevant components |
| D5.05 | Relational Structure | REQUIRED | map component relations |
| D5.06 | Process | REQUIRED | represent temporal/functional sequence |
| D5.07 | Provisional Mechanism | CONDITIONAL | formulate mechanism when supported |
| D5.08 | Mediation / Moderation / Feedback | CONDITIONAL | represent higher-order process relations |
| D5.09 | Alternatives | CONDITIONAL | compare competing mechanisms |
| D5.10 | Evidence | REQUIRED | map Evidence to mechanism Claims |
| D5.11 | Counter-evidence | CONDITIONAL | represent contradictory Evidence |
| D5.12 | Boundaries | REQUIRED | define mechanism applicability |
| D5.13 | Verification Status | REQUIRED | expose verification state |
| D5.14 | Conclusion / Follow-up | REQUIRED | state current mechanism and next questions |

Constraints:
- Mechanisms must not be fabricated to fill a structural slot.
- A plausible process description is not automatically a verified mechanism.
- Mediation/moderation/feedback terminology requires corresponding analytical support.

## 8. D6 — Predictive Research Note

Primary function: generate and evaluate conditional forecasts.

| ID | Section | Status | Purpose |
|---|---|---|---|
| D6.01 | Prediction Question | REQUIRED | define forecast target |
| D6.02 | Object / Time Horizon | REQUIRED | define target and horizon |
| D6.03 | Current State | REQUIRED | establish forecast baseline |
| D6.04 | Evidence | REQUIRED | map forecast Evidence |
| D6.05 | Variables / Conditions | REQUIRED | identify predictive factors and conditions |
| D6.06 | Model / Logic | REQUIRED | state forecasting model/logic |
| D6.07 | Baseline Scenario | REQUIRED | define baseline scenario |
| D6.08 | Alternative Scenarios | CONDITIONAL | define materially distinct alternatives |
| D6.09 | Threshold Conditions | CONDITIONAL | identify thresholds/trigger conditions |
| D6.10 | Uncertainty | REQUIRED | expose forecast uncertainty |
| D6.11 | Verification / Falsification Conditions | REQUIRED | define future evaluation criteria |
| D6.12 | Result | REQUIRED | state forecast |
| D6.13 | Update Conditions | REQUIRED | specify Evidence that should update the forecast |

Constraints:
- Forecast output is not a current fact.
- Scenarios must retain their assumptions.
- Future verification conditions must be explicit where possible.

## 9. D7 — Evaluation Research Note

Primary function: evaluate an object against explicit criteria and support decision-making.

| ID | Section | Status | Purpose |
|---|---|---|---|
| D7.01 | Object | REQUIRED | define evaluation object |
| D7.02 | Purpose | REQUIRED | define evaluation purpose |
| D7.03 | Evaluation Criteria | REQUIRED | state criteria |
| D7.04 | Basis for Criteria | REQUIRED | justify criteria |
| D7.05 | Current State | REQUIRED | establish baseline |
| D7.06 | Effect / Performance / Impact | CONDITIONAL | evaluate relevant outcomes |
| D7.07 | Process | CONDITIONAL | evaluate implementation/process |
| D7.08 | Alternatives | CONDITIONAL | compare alternatives |
| D7.09 | Positive / Negative Outcomes | REQUIRED | balance findings |
| D7.10 | Uncertainty / Limitations | REQUIRED | expose evaluation limitations |
| D7.11 | Judgment | REQUIRED | state evidence-based judgment |
| D7.12 | Improvement / Decision Implications | CONDITIONAL | derive actionable implications |

Constraints:
- Evaluation criteria must not be invented merely to reach a judgment.
- Judgment must remain traceable to criteria and Evidence.
- Recommendation is distinct from Evidence and Verification.

## 10. D8 — Literature / Evidence Synthesis Research Note

Primary function: systematically or transparently synthesize literature/Evidence.

| ID | Section | Status | Purpose |
|---|---|---|---|
| D8.01 | Review Question | REQUIRED | define synthesis question |
| D8.02 | Scope / Inclusion Criteria | REQUIRED | define evidence boundary |
| D8.03 | Search / Screening | REQUIRED | document retrieval/selection process when applicable |
| D8.04 | Concepts | CONDITIONAL | normalize relevant concepts |
| D8.05 | Research Streams | CONDITIONAL | describe literature development |
| D8.06 | Claims | REQUIRED | extract/structure study Claims |
| D8.07 | Evidence Comparison | REQUIRED | compare Evidence |
| D8.08 | Agreement | CONDITIONAL | identify supported convergence |
| D8.09 | Disagreement / Debate | CONDITIONAL | preserve disagreement |
| D8.10 | Methodological Differences | CONDITIONAL | account for methodological heterogeneity |
| D8.11 | Evidence Strength / Limitations | REQUIRED | assess Evidence limitations |
| D8.12 | Synthesis | REQUIRED | produce synthesis result |
| D8.13 | Research Gaps | CONDITIONAL | identify supported gaps |
| D8.14 | Follow-up Questions | REQUIRED | derive future research questions |

Review Type is metadata, not itself a claim of methodological rigor:
Narrative Review, Systematic Review, Scoping Review, Integrative Review, Meta-analysis, Qualitative Synthesis, Other.

Constraints:
- “Consensus” must not erase disagreement.
- Synthesis is a transformation operation/result, not Evidence by itself.
- Absence of literature must not automatically be interpreted as absence of research.

## 11. D9 — Integrated / Synthesis Research Note

Primary function: construct a new, traceable integration across existing Research Notes/Objects.

| ID | Section | Status | Purpose |
|---|---|---|---|
| D9.01 | Source Notes | REQUIRED | identify integrated source notes/objects |
| D9.02 | Integration Question | REQUIRED | define higher-order question |
| D9.03 | Key Claims from Each Note | REQUIRED | represent source Claims |
| D9.04 | Commonalities | CONDITIONAL | identify shared structure |
| D9.05 | Tensions / Differences | CONDITIONAL | preserve meaningful differences |
| D9.06 | Supporting Relations | CONDITIONAL | map supporting relations |
| D9.07 | Conflicts | CONDITIONAL | map contradictions/conflicts |
| D9.08 | Integrable Structure | REQUIRED | identify candidate higher-order structure |
| D9.09 | Integrated Explanation / Model | CONDITIONAL | formulate integrated explanation/model |
| D9.10 | Integrated Evidence | REQUIRED | map Evidence to integration Claims |
| D9.11 | Limitations | REQUIRED | state integration limits |
| D9.12 | Unresolved Problems | REQUIRED | preserve unresolved tensions |
| D9.13 | New Questions | REQUIRED | generate higher-order follow-up questions |

D9-specific controls:
- D9 is not a summary-only format.
- New integration Claims require Claim decomposition and Evidence Mapping.
- D9 Gate G1–G6 remains independent of the template.
- D9 CANDIDATE and PROMOTED must be displayed separately.
- PROMOTED does not mean VERIFIED.
- Source-note epistemic states must not be overwritten by integration.

## 12. Cross-Type Conditional Modules

The following modules may be attached to any compatible template:
- Evidence Mapping
- Claim Decomposition
- Counter-evidence
- Competing Explanation
- Comparison
- Scenario Analysis
- Evaluation Criteria
- Literature Screening
- SARA
- Revision
- Relation Mapping
- D9 Gate

Modules are invoked by conditions, not by a requirement to fill every section.

## 13. Cross-Type Generation Rules

1. Select Document Type only after provisional classification and evidence-aware reclassification.
2. Use the minimum template sufficient for the selected type.
3. Render REQUIRED sections even when they contain an explicit missing/unresolved state.
4. Render CONDITIONAL sections only when trigger conditions are satisfied.
5. Never fabricate missing Claims, Evidence, Verification, Relations, mechanisms, variables, criteria, or literature findings.
6. Preserve attribution and temporal context.
7. Preserve Claim-level epistemic states.
8. Preserve revision history and provenance.
9. Treat synthesis as a Transformation Event/result unless independently supported as Evidence.
10. Persistence never changes epistemic state.
11. The human remains the final epistemic decision authority.

## 14. Decision

**T40 = PASS**

The existing D1–D9 structures have been converted into an initial executable template specification.

This remains a **project-level template proposal**, not an established academic standard.

No new Document Type is introduced. No new logical entity is introduced. No Notion schema expansion is required.

## 15. Next Test

**T41 — Template ↔ Knowledge Object Mapping Test**

T41 should test whether each template section can be mapped without semantic inflation to Research Object, Claim, Evidence, Transformation Event, Verification, Relation, and Provenance.

## 16. Known Limitations

T40 defines structure and safety constraints but does not yet prove:
- complete object-to-section coverage;
- absence of redundant sections;
- generation consistency across real conversations;
- rendering quality;
- queryability of template-level metadata.

Those require subsequent tests.

## Cross-Type AI Disclosure Rule

All D1–D9 templates inherit a common artifact-level disclosure requirement:

**AI-generated / AI-structured Research Note**

The marker is rendered outside the type-specific body and therefore survives changes in Document Type. The provenance block should retain generation system, AI participation, human-review status, and generation provenance.

D1–D9 must not reinterpret the marker as Evidence, Verification, a Claim state, D9 promotion, or source authorship.

Human edits and source-derived material remain separately attributable where provenance supports the distinction.

---

[Korean source](t40_d1_d9_standard_template_specification_v0.1.md)
