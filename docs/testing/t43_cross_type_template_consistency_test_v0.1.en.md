# T43 — Cross-Type Template Consistency Test v0.1

Status: **PASS — CROSS-TYPE GENERATION RULES CONSISTENT WITH TYPE DISTINCTIONS**

## 1. Purpose

T43 tests whether the T39 common contract, T40 D1–D9 templates, T41 object mapping, and T42 conditional-rendering rules produce consistent behavior across Document Types.

The test focuses on Document Type selection, Primary Research Purpose distinction, required/conditional/optional rendering, missing-state handling, epistemic safety, type-specific analytical structure, and resistance to template forcing.

T43 tests semantics and generation rules. It does not claim full empirical validation using live production conversations.

## 2. Test Principle

Cross-type consistency does not mean identical outputs.

**Same safety rules + different information architecture**, not **same section behavior + different labels**.

A valid result must preserve both cross-type invariants and type-specific distinctions.

## 3. Cross-Type Invariants

All D1–D9 must satisfy:

1. The Research Object is identified or explicitly unresolved.
2. Primary Research Purpose ≤ 1.
3. Document Type is distinct from Research Purpose.
4. Claims remain distinct from Evidence.
5. Evidence remains distinct from Verification.
6. Transformation output remains distinct from source Evidence.
7. Relations are not created by prose similarity alone.
8. Missing information is never fabricated.
9. Rendering does not upgrade epistemic state.
10. Material provenance is preserved.
11. Revision does not overwrite historical state.
12. D9 Promotion remains independent from document generation.
13. Persistence is not epistemic verification.

## 4. Cross-Type Test Inputs

These controlled prompts represent the dominant information structure of each Document Type.

### Case D1 — Exploration
Prompt: “Let’s organize a repeatedly observed recent phenomenon and explore possible patterns. We do not yet know which explanation is correct.”

Expected:
- Document Type: D1
- Primary Purpose: R1
- Pattern/clue section is conditional
- Provisional structure/hypothesis may appear only as provisional
- No unsupported explanation upgrade

Result: **PASS**

### Case D2 — Description / Current State
Prompt: “Systematically organize the main types, distribution, and recent changes in this phenomenon.”

Expected:
- Document Type: D2
- Primary Purpose: R2
- Classification/distribution/change sections render according to available observations
- No causal explanation generated merely from observed change

Result: **PASS**

### Case D3 — Concept Analysis
Prompt: “Compare what ‘research,’ ‘replacement,’ and ‘assistance’ mean in the phrase ‘AI replaces research,’ and clarify their boundaries.”

Expected:
- Document Type: D3
- Primary Purpose: R1.2
- Definitions and boundaries required
- Competing conceptualizations conditional
- Adopted conceptualization retains attribution/working status
- No empirical conclusion fabricated from conceptual analysis

Result: **PASS**

### Case D4 — Relation / Impact
Prompt: “We observed X and Y increasing together. Examine whether this is an actual impact relationship or whether other explanations are possible.”

Expected:
- Document Type: D4
- Primary Purpose: R3.1 or R3.2 depending on the normalized question
- Association represented separately from causality
- Alternative explanations/counter-evidence conditional
- Causal interpretation cannot be upgraded without a basis

Result: **PASS**

### Case D5 — Mechanism / Process
Prompt: “Explain why this result occurs in terms of components and processes, and compare possible mechanisms.”

Expected:
- Document Type: D5
- Primary Purpose: R3.3 or R3.4 depending on the normalized question
- Components/process required
- Mechanism remains provisional unless supported
- Mediation/moderation/feedback conditional
- Alternatives and counter-evidence preserved

Result: **PASS**

### Case D6 — Prediction
Prompt: “Assuming current conditions continue, examine likely future changes alongside alternative scenarios.”

Expected:
- Document Type: D6
- Primary Purpose: R4
- Horizon and conditions required
- Baseline scenario required
- Alternatives/thresholds conditional
- Uncertainty and update conditions required
- Prediction not represented as fact

Result: **PASS**

### Case D7 — Evaluation
Prompt: “Evaluate whether this policy was effective and examine the criteria and possible improvements.”

Expected:
- Document Type: D7
- Primary Purpose: R5
- Evaluation criteria supplied, justified, or escalated
- Outcomes/process/alternatives conditional
- Judgment linked to criteria and Evidence
- Normative criteria not invented

Result: **PASS**

### Case D8 — Literature / Evidence Synthesis
Prompt: “Find related studies, compare their central claims and evidence, and synthesize agreement and debate across studies.”

Expected:
- Document Type: D8
- Primary Purpose may be R1.5/R3/R5 as normalized; D8 is determined by the actual review task
- Search/selection represented only if actually performed
- Study-level disagreement and methodological differences preserved
- Review Type does not automatically imply methodological rigor

Result: **PASS**

### Case D9 — Integrated Synthesis
Prompt: “Compare the central claims of three existing research notes, analyze their relations, and examine whether an integrated structure explains something not explained by the notes individually.”

Expected:
- Document Type: D9
- Primary Purpose determined by the integration question
- Source notes and source claims required
- Supporting/conflicting relations conditional
- Integrated structure is candidate transformation output
- New integration claims require Claim decomposition and Evidence mapping
- D9 Gate remains independent

Result: **PASS**

## 5. Ambiguity Test

### Case A — D3 vs D1
Prompt: “Find out exactly what ‘research assistance’ means and explore how people use the phrase.”

Possible structures:
- conceptual boundary analysis → D3
- exploratory mapping of usage → D1

Expected:
- do not force one type when the distinction materially affects output;
- normalize the Research Question;
- if unresolved, ESCALATE or use the dominant explicit purpose with ambiguity disclosed.

Result: **PASS**

### Case B — D4 vs D5
Prompt: “Determine whether AI use affects research outcomes and, if so, through what process.”

This combines relationship and mechanism questions.

Expected:
- determine Primary Purpose from the principal question;
- record a Secondary Purpose when appropriate;
- split into separate Research Objects if both questions have independent evidence/lifecycle/conclusions;
- otherwise use one primary type with conditional analytical modules.

Result: **PASS**

### Case C — D7 vs D6
Prompt: “Assess whether this policy will continue to be effective in the future.”

Possible interpretations:
- forecast → D6
- evaluation → D7

Expected:
- distinguish prediction of a future state from evaluation against criteria;
- if evaluation is intended but criteria are absent, ESCALATE rather than invent them.

Result: **PASS**

### Case D — D8 vs D9
Prompt: “Synthesize several studies to create a new explanation.”

Expected:
- literature review/synthesis → D8 when evidence synthesis is the primary task;
- integration across existing research notes/claims → D9 when higher-order integration is primary;
- do not infer D9 Promotion from the phrase “new explanation.”

Result: **PASS**

## 6. Conditional Rendering Consistency Matrix

| Rule | D1 | D2 | D3 | D4 | D5 | D6 | D7 | D8 | D9 |
|---|---|---|---|---|---|---|---|---|---|
| Required sections preserved | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| Unsupported content omitted | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| Missing state visible | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| Provenance preserved | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| Claim/Evidence distinction | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| Epistemic inflation blocked | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| Type-specific structure preserved | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| Reclassification available | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |

## 7. Type-Specific Failure Tests

- **F1 — D1 hypothesis inflation:** A plausible pattern is converted directly into a verified explanation. Expected: reject the upgrade. **PASS.**
- **F2 — D2 causal inflation:** A distributional difference is rendered as a causal explanation. Expected: reject causal interpretation. **PASS.**
- **F3 — D3 conceptual inflation:** A project-adopted definition is presented as universally correct. Expected: preserve attribution and scope. **PASS.**
- **F4 — D4 causal inflation:** Association is rendered as causal effect. Expected: preserve association; causal Claim requires sufficient basis. **PASS.**
- **F5 — D5 mechanism fabrication:** A mechanism is supplied because the template contains a mechanism section. Expected: missing state / provisional status / escalation. **PASS.**
- **F6 — D6 forecast inflation:** A scenario is presented as certain future fact. Expected: retain assumptions and uncertainty. **PASS.**
- **F7 — D7 normative inflation:** Evaluation criteria are invented by the generator. Expected: escalation. **PASS.**
- **F8 — D8 consensus inflation:** Conflicting studies are collapsed into “consensus.” Expected: preserve disagreement and methodological differences. **PASS.**
- **F9 — D9 promotion inflation:** Integrated structure is automatically treated as promoted. Expected: candidate only until D9 Gate requirements are met. **PASS.**

## 8. Consistency Criteria

T43 passes when:
- all nine types obey common semantic safety invariants;
- each type retains its analytical information structure;
- ambiguous prompts trigger controlled normalization/reclassification rather than forced completion;
- conditional sections behave consistently under T42 rendering states;
- no template section automatically creates an epistemic object;
- D9 remains distinct from ordinary synthesis and promotion.

All criteria were satisfied.

## 9. Result

**T43 = PASS**

The D1–D9 template system demonstrates cross-type consistency at the rule and controlled-input level.

Supported architecture:

**Common Research Note Contract** → **Document Type Selection** → **Type-specific Template** → **Conditional Rendering** → **Knowledge-object / Transformation references** → **Epistemic and Provenance controls**

No new Document Type, logical entity, or Notion schema is justified.

## 10. Validation Boundary

T43 is a controlled semantic test, not a statistical evaluation of generation accuracy.

The next empirical layer should test:
1. actual project-style conversational prompts;
2. repeated generation from the same prompt;
3. ambiguous/multi-purpose prompts;
4. revision and extension of existing notes;
5. composite sections with multiple Claims/Evidence;
6. derived sections with Transformation Trace;
7. human-review agreement on Document Type and section rendering;
8. output redundancy/readability.

## 11. Next Test

**T44 — Repeated Generation / Determinism and Semantic Stability Test**

T44 should test whether repeated generation preserves Document Type, Primary Research Purpose, Claim/Evidence distinctions, section inclusion/exclusion, missing-state handling, epistemic state, provenance, and Transformation references while allowing legitimate wording variation.

## 12. Boundary

This is a project-level operational test and proposal, not an established academic or industry standard. The human remains the final epistemic decision authority.

---

[Korean source](t43_cross_type_template_consistency_test_v0.1.md)
