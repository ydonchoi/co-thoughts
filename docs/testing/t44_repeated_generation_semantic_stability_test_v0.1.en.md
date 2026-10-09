# T44 — Repeated Generation / Determinism and Semantic Stability Test v0.1

Status: **PASS — SEMANTIC STABILITY CONTRACT DEFINED / EMPIRICAL REPETITION DEFERRED**

## 1. Purpose

T44 tests whether repeated generation from the same input preserves the research structure established by T39–T43 while allowing legitimate linguistic variation.

The test distinguishes lexical, stylistic, structural, semantic, and epistemic variation.

The objective is not deterministic wording. It is **semantic stability under repeated generation**.

## 2. Core Principle

For identical input and unchanged relevant context:

**wording may vary; research meaning must remain materially stable.**

Repeated generation is acceptable when it preserves the same underlying Research Object, principal Research Purpose, Document Type, Claims, Evidence relations, epistemic states, provenance, and material Transformation structure, subject to explicit uncertainty or legitimate ambiguity.

## 3. Stability Layers

### S1 — Lexical Stability
Words and sentence structures may vary; identical wording is not required.

### S2 — Structural Stability
The same applicable D1–D9 sections should generally be rendered. Variation is allowed only when a conditional trigger is genuinely ambiguous, a section is immaterial in one rendering, and the generator explicitly records the reason.

### S3 — Object Stability
The following should remain materially invariant:
- Research Object identity/boundary;
- Claim identity when claims are already decomposed;
- Evidence identity and attribution;
- explicitly established Relation types;
- materially established Transformation identity.

### S4 — Epistemic Stability
Repeated generation must not silently change states such as:
- VERIFIED → SUPPORTED;
- SUPPORTED → VERIFIED;
- HYPOTHESIS → VERIFIED;
- CONTRADICTED → SUPPORTED;
- UNVERIFIED → VERIFIED.

An epistemic transition requires new Evidence, Verification, Revision, or an explicit change in input/context.

### S5 — Provenance Stability
Source attribution and provenance references must remain materially consistent. The generator must not alternate between a sourced statement, model-generated interpretation, and user-provided assertion without preserving their provenance classes.

### S6 — Transformation Stability
A material derivation should retain its Transformation Event representation. Repeated generation must not arbitrarily create a transformation for a simple restatement, remove a transformation when derivation matters, or change the transformation type without a changed analytical operation.

## 4. Controlled Repetition Protocol

For each test input:
1. Freeze user input.
2. Freeze relevant repository/project state.
3. Freeze available source/evidence context.
4. Generate the same Research Note multiple times.
5. Compare outputs at semantic layers.
6. Ignore permitted lexical variation.
7. Record structural/object/epistemic differences.
8. Classify each difference as ACCEPTABLE_VARIATION, MATERIAL_VARIATION, UNSAFE_VARIATION, or CONTEXT_DEPENDENT.
9. Investigate all MATERIAL and UNSAFE variations.

The architecture-definition stage does not prescribe a fixed number of runs.

## 5. Stability Contract

With unchanged input/context, the following are **hard stability targets**:
1. Research Object boundary;
2. Primary Research Purpose;
3. Document Type when classification is unambiguous;
4. required section presence;
5. explicit reason for missing state;
6. Claim/Evidence distinction;
7. epistemic state;
8. material provenance;
9. material Transformation Trace;
10. D9 state, when applicable.

The following are **soft stability targets**:
- wording;
- paragraph order within a section;
- examples;
- explanatory verbosity;
- sentence segmentation;
- optional section inclusion where it adds no new epistemic content.

## 6. Acceptable Variation

Examples include equivalent expressions such as “current evidence is limited” and “the evidence currently available is insufficient,” equivalent explanations of the same relation, different ordering of non-dependent paragraphs, or omission of an optional explanatory sentence that does not change the represented Claim set.

These are ACCEPTABLE_VARIATION if object identity and epistemic meaning remain stable.

## 7. Material Variation

Material variation includes:
- D4 → D5 without changed input;
- R3 → R4 Primary Purpose change;
- adding/removing a material Claim;
- changing Claim state or Evidence role;
- changing causal versus correlational interpretation;
- D9 CANDIDATE → PROMOTED without new gate evidence;
- removing material provenance;
- converting an interpretation into an attributed fact;
- creating/removing a material Transformation Event.

Material variation requires investigation.

## 8. Unsafe Variation

Unsafe variation includes:
- fabricated Evidence appearing in only one run;
- fabricated source/citation;
- unsupported Verification;
- epistemic upgrade without new basis;
- loss of contradictory Evidence;
- causal Claim appearing/disappearing solely due to generation randomness;
- invented evaluation criteria;
- D9 promotion without Gate conditions;
- persistence represented as verification.

Any unsafe variation is a FAIL for that test case.

## 9. Ambiguity Stability Rule

Not every ambiguity requires identical output.

Repeated generation may produce different candidate interpretations only if the ambiguity is disclosed, the alternatives are semantically plausible, no alternative is silently presented as established fact, and material divergence triggers ESCALATE_HUMAN or controlled reclassification.

**Ambiguity may vary; hidden epistemic commitment may not.**

## 10. Missing-State Stability

With unchanged context:
- NOT_AVAILABLE must not randomly become NOT_ESTABLISHED;
- REQUIRES_VERIFICATION must not become VERIFIED;
- UNRESOLVED must not resolve solely through repetition;
- NOT_APPLICABLE must not become an invented substantive section.

A change in missing state requires an identifiable change in available information or interpretation.

## 11. Document-Type Stability Test Set

- **R1 — Clear D1:** exploratory pattern discovery; D1 remains consistent and hypotheses provisional.
- **R2 — Clear D4:** asks whether an observed relationship is causal; D4 and association/causality distinction preserved.
- **R3 — Clear D5:** asks for mechanism/process explanation; D5 and mechanism status preserved.
- **R4 — Clear D6:** asks for conditional future prediction; D6, assumptions, and uncertainty preserved.
- **R5 — Clear D7:** asks for evaluation against criteria; D7 and criteria/Evidence relation preserved.
- **R6 — Clear D8:** explicitly requires literature search and synthesis; D8, with no fabricated search activity.
- **R7 — Clear D9:** integrates multiple existing notes at a higher level; D9, with candidate status until D9 Gate is independently satisfied.
- **R8 — Ambiguous D4/D5:** relation and mechanism questions; primary classification may vary only within disclosed ambiguity, independent questions may be split, and causal/mechanistic inflation is prohibited.
- **R9 — Ambiguous D7/D6:** asks whether an intervention will “work” in the future; distinguish forecast from evaluation and do not invent missing criteria.
- **R10 — Ambiguous D8/D9:** asks to synthesize studies into a new explanation; use D8 for literature evidence synthesis, D9 for integration of existing research-note structures, with no automatic D9 Promotion.

## 12. Repeated-Generation Comparison Matrix

| Layer | Expected tolerance | Failure condition |
|---|---|---|
| Wording | High | None by itself |
| Section order | Medium | Changes analytical meaning |
| Optional sections | Medium | Hides material information |
| Document Type | Low | Unexplained material change |
| Research Purpose | Low | Unexplained material change |
| Claim set | Very low | Material addition/removal |
| Evidence mapping | Very low | Changed role/provenance |
| Epistemic state | Very low | Unexplained state change |
| Provenance | Very low | Attribution loss/change |
| Transformation Trace | Low | Material derivation lost/created |
| D9 state | Very low | Unexplained promotion/downgrade |

## 13. Semantic Equivalence Test

Two outputs are semantically equivalent when:
1. Research Object boundaries are equivalent;
2. Primary Purpose and Document Type are equivalent or explicitly unresolved;
3. material Claim sets are equivalent;
4. Evidence roles/provenance are equivalent;
5. epistemic states are equivalent;
6. material Relations and Transformations are equivalent;
7. differences do not change the conclusion, uncertainty, or decision boundary.

Exact text equality is not required.

## 14. Repeatability vs Reproducibility

- **Repeatability:** the same system/context/input produces materially stable results across repeated runs.
- **Reproducibility:** an independently reconstructed process obtains materially equivalent results.

T44 primarily tests repeatability. Full reproducibility is separate because it requires controlled reconstruction of context, evidence, state, and generation conditions.

## 15. Result

**T44 = PASS — CONTRACT DEFINED**

The semantic-stability contract is sufficiently specified for implementation and empirical testing.

This PASS does **not** claim actual repeated LLM generations have already been measured. The empirical test remains **DEFERRED** until repeated live generation under controlled conditions is executed.

## 16. Failure Handling

If empirical repetition reveals material variation:
1. determine whether source ambiguity is genuine;
2. compare classification inputs;
3. inspect Claim/Evidence decomposition;
4. inspect conditional-rendering triggers;
5. inspect provenance and Transformation references;
6. determine whether variation is model nondeterminism or an underspecified project rule;
7. update the relevant rule only if evidence demonstrates a specification gap;
8. re-run the affected test.

Do not resolve instability by forcing identical wording.

## 17. No Architecture Expansion

T44 does not justify a new Document Type, logical entity, Notion database, or deterministic text-generation requirement. The current architecture can express semantic stability.

## 18. Next Test

**T45 — Empirical Generation Stability / Ambiguity Stress Test**

T45 should use realistic conversational inputs and repeated generations to measure Document Type agreement, Primary Purpose agreement, section-rendering agreement, Claim/Evidence stability, epistemic-state stability, provenance preservation, Transformation Trace stability, and human-review agreement.

## 19. Boundary

This is a project-level operational test and specification, not an established academic or industry standard. The human remains the final epistemic decision authority.

---

[Korean source](t44_repeated_generation_semantic_stability_test_v0.1.md)
