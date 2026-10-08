# T44 — Repeated Generation / Determinism and Semantic Stability Test v0.1

Status: **PASS — SEMANTIC STABILITY CONTRACT DEFINED / EMPIRICAL REPETITION DEFERRED**

## 1. Purpose

T44 tests whether repeated generation from the same input can preserve the research structure established by T39–T43 while allowing legitimate linguistic variation.

The test distinguishes:

- lexical variation;
- stylistic variation;
- structural variation;
- semantic variation;
- epistemic variation.

The objective is not deterministic wording. The objective is **semantic stability under repeated generation**.

## 2. Core Principle

For identical input and unchanged relevant context:

**wording may vary; research meaning must remain materially stable.**

A repeated generation is acceptable when it preserves the same underlying Research Object, principal research purpose, document type, Claims, Evidence relations, epistemic states, provenance, and material Transformation structure, subject to explicit uncertainty or legitimate ambiguity.

## 3. Stability Layers

### S1 — Lexical Stability

Words and sentence structures may vary.

Not required to be identical.

### S2 — Structural Stability

The same applicable D1–D9 sections should generally be rendered.

Variation is allowed only when:
- a conditional trigger is genuinely ambiguous;
- a section is immaterial in one rendering;
- the generator explicitly records the reason.

### S3 — Object Stability

The following should remain materially invariant:

- Research Object identity/boundary;
- Claim identity where claims are already decomposed;
- Evidence identity and attribution;
- Relation type where explicitly established;
- Transformation identity where materially established.

### S4 — Epistemic Stability

Repeated generation must not silently change:

- VERIFIED → SUPPORTED;
- SUPPORTED → VERIFIED;
- HYPOTHESIS → VERIFIED;
- CONTRADICTED → SUPPORTED;
- UNVERIFIED → VERIFIED;

or other material epistemic transitions.

An epistemic transition requires new Evidence, Verification, Revision, or an explicit change in input/context.

### S5 — Provenance Stability

Source attribution and provenance references must remain materially consistent.

The generator must not alternate between:
- sourced statement;
- model-generated interpretation;
- user-provided assertion

without preserving their provenance class.

### S6 — Transformation Stability

A material derivation should retain its Transformation Event representation.

Repeated generation must not arbitrarily:
- create a new transformation for a simple restatement;
- remove a transformation when derivation materially matters;
- change the transformation type without a changed analytical operation.

## 4. Controlled Repetition Protocol

For each test input:

1. Freeze user input.
2. Freeze relevant Repository/project state.
3. Freeze available source/evidence context.
4. Generate the same Research Note multiple times.
5. Compare outputs at semantic layers.
6. Ignore permitted lexical variation.
7. Record structural/object/epistemic differences.
8. Classify each difference as:
   - ACCEPTABLE_VARIATION
   - MATERIAL_VARIATION
   - UNSAFE_VARIATION
   - CONTEXT_DEPENDENT
9. Investigate all MATERIAL and UNSAFE variations.

The protocol does not require a fixed number of runs at the architecture-definition stage.

## 5. Stability Contract

For unchanged input/context, the following are **hard stability targets**:

1. Research Object boundary;
2. Primary Research Purpose;
3. Document Type when classification is unambiguous;
4. required section presence;
5. explicit missing-state reason;
6. Claim/Evidence distinction;
7. epistemic state;
8. material provenance;
9. material Transformation Trace;
10. D9 state when applicable.

The following are **soft stability targets**:

- wording;
- paragraph order within a section;
- examples;
- explanatory verbosity;
- sentence segmentation;
- optional section inclusion when the optional section adds no new epistemic content.

## 6. Acceptable Variation

Examples:

- “현재 근거는 제한적이다” vs “현재 확인된 근거가 충분하지 않다”;
- two equivalent explanations of the same relation;
- different ordering of two non-dependent explanatory paragraphs;
- omission of an optional explanatory sentence that does not alter the represented Claim set.

These are ACCEPTABLE_VARIATION if object identity and epistemic meaning remain stable.

## 7. Material Variation

Material variation includes:

- D4 → D5 without changed input;
- R3 → R4 primary-purpose change;
- adding/removing a material Claim;
- changing Claim state;
- changing Evidence role;
- changing causal versus correlational interpretation;
- changing D9 CANDIDATE → PROMOTED without new gate evidence;
- removing material provenance;
- converting an interpretation into an attributed fact;
- creating/removing a material Transformation Event.

Material variation requires investigation.

## 8. Unsafe Variation

Unsafe variation includes:

- fabricated Evidence appearing in only one run;
- fabricated source or citation;
- unsupported Verification;
- epistemic upgrade without new basis;
- loss of contradictory Evidence;
- causal claim appearing/disappearing solely due to generation randomness;
- invented evaluation criteria;
- D9 promotion generated without Gate conditions;
- persistence represented as verification.

Any unsafe variation is a FAIL for that test case.

## 9. Ambiguity Stability Rule

Not every ambiguity requires identical output.

When input genuinely permits multiple interpretations, repeated generation may produce different candidate interpretations only if:

1. the ambiguity is disclosed;
2. the alternatives are semantically plausible;
3. no alternative is silently presented as established fact;
4. material divergence triggers ESCALATE_HUMAN or controlled reclassification.

Thus:

**ambiguity may vary; hidden epistemic commitment may not.**

## 10. Missing-State Stability

For unchanged context:

- NOT_AVAILABLE must not randomly become NOT_ESTABLISHED;
- REQUIRES_VERIFICATION must not become VERIFIED;
- UNRESOLVED must not become resolved solely through repetition;
- NOT_APPLICABLE must not become an invented substantive section.

A change in missing-state requires an identifiable change in available information or interpretation.

## 11. Document-Type Stability Test Set

### R1 — Clear D1

Input clearly describes exploratory pattern discovery.

Expected:
- D1 consistently selected;
- hypothesis remains provisional.

### R2 — Clear D4

Input clearly asks whether an observed relationship is causal.

Expected:
- D4 consistently selected;
- association/causality distinction preserved.

### R3 — Clear D5

Input explicitly asks for mechanism/process explanation.

Expected:
- D5 consistently selected;
- mechanism status preserved.

### R4 — Clear D6

Input asks for conditional future prediction.

Expected:
- D6 consistently selected;
- assumptions and uncertainty preserved.

### R5 — Clear D7

Input asks for evaluation against criteria.

Expected:
- D7 consistently selected;
- criteria/evidence relationship preserved.

### R6 — Clear D8

Input explicitly requires literature search and synthesis.

Expected:
- D8 consistently selected;
- no fabricated search activity.

### R7 — Clear D9

Input explicitly references multiple existing notes and asks for higher-order integration.

Expected:
- D9 consistently selected;
- integrated structure remains candidate unless D9 Gate is independently satisfied.

### R8 — Ambiguous D4/D5

Input combines relationship and mechanism questions.

Expected:
- primary classification may vary only within disclosed ambiguity;
- independent questions may trigger Research Object split;
- no silent causal/mechanistic inflation.

### R9 — Ambiguous D7/D6

Input asks whether an intervention will “work” in the future.

Expected:
- distinguish forecast from evaluation;
- if evaluation criteria are missing, do not invent them.

### R10 — Ambiguous D8/D9

Input asks to “synthesize studies into a new explanation”.

Expected:
- D8 when literature evidence synthesis is primary;
- D9 when existing research-note structures are being integrated;
- no automatic D9 Promotion.

## 12. Repeated-Generation Comparison Matrix

| Layer | Expected tolerance | Failure condition |
|---|---|---|
| Wording | High | none by itself |
| Section order | Medium | changes analytical meaning |
| Optional sections | Medium | hides material information |
| Document Type | Low | unexplained material change |
| Research Purpose | Low | unexplained material change |
| Claim set | Very low | material addition/removal |
| Evidence mapping | Very low | changed role/provenance |
| Epistemic state | Very low | unexplained state change |
| Provenance | Very low | attribution loss/change |
| Transformation Trace | Low | material derivation lost/created |
| D9 state | Very low | unexplained promotion/downgrade |

## 13. Semantic Equivalence Test

Two outputs should be treated as semantically equivalent when:

1. their Research Object boundaries are equivalent;
2. their Primary Research Purpose and Document Type are equivalent or explicitly disclosed as unresolved;
3. their material Claim sets are equivalent;
4. their Evidence roles/provenance are equivalent;
5. their epistemic states are equivalent;
6. their material Relations and Transformations are equivalent;
7. differences do not change the conclusion, uncertainty, or decision boundary.

Exact textual equality is not required.

## 14. Repeatability vs Reproducibility

T44 distinguishes:

- **Repeatability:** same system/context/input produces materially stable results across repeated runs.
- **Reproducibility:** an independently reconstructed process can obtain materially equivalent results.

T44 primarily tests repeatability.

Full reproducibility remains a separate validation concern because it requires controlled reconstruction of context, evidence, state, and generation conditions.

## 15. Result

**T44 = PASS — CONTRACT DEFINED**

The semantic stability contract is sufficiently specified for implementation and empirical testing.

However, this PASS does **not** claim that actual repeated LLM generations have already been measured.

The empirical test remains **DEFERRED** until repeated live generation under controlled conditions is executed.

## 16. Failure Handling

If empirical repetition reveals material variation:

1. determine whether the source ambiguity is genuine;
2. compare classification inputs;
3. inspect Claim/Evidence decomposition;
4. inspect conditional-rendering triggers;
5. inspect provenance and Transformation references;
6. determine whether variation is model nondeterminism or an underspecified project rule;
7. update the relevant rule only if the evidence demonstrates a specification gap;
8. re-run the affected test.

Do not solve instability by forcing identical wording.

## 17. No Architecture Expansion

T44 does not justify:
- a new Document Type;
- a new logical entity;
- a new Notion database;
- deterministic text-generation requirements.

The current architecture is sufficient to express semantic stability.

## 18. Next Test

**T45 — Empirical Generation Stability / Ambiguity Stress Test**

T45 should use actual project-style conversational inputs and repeated generations to measure:
- Document Type agreement;
- Primary Purpose agreement;
- section-rendering agreement;
- Claim/Evidence stability;
- epistemic-state stability;
- provenance preservation;
- Transformation Trace stability;
- human-review agreement.

## 19. Boundary

This is a project-level operational test and specification. It is not an established academic or industry standard.

Human remains final epistemic decision authority.
