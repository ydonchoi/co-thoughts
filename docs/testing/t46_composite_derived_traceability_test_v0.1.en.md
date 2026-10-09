# T46 — Composite / Derived Section Traceability Test v0.1

Status: **PASS — OBJECT-LEVEL TRACEABILITY RULES VALIDATED WITH CONTROLLED FIXTURES**

## 1. Purpose
T46 tests whether generated Research Note sections preserve traceability when a section contains (1) multiple Claims and Evidence items (COMPOSITE), or (2) a derived result whose interpretation materially depends on Transformation Events (DERIVED / TRANSFORMATIVE).

The test ensures that document rendering does not collapse logical objects into prose.

## 2. Scope
T46 builds on:
- T41 M2 Composite mapping;
- T41 M3 Derived/Transformative mapping;
- T42 conditional rendering;
- T43 cross-type consistency;
- T44 semantic stability;
- T45 traceability fixtures.

No new core logical entity is introduced.

## 3. Traceability Chain
Minimum chain:

**Source / Input → Evidence → Transformation Event → Claim / Result → Rendered Section**

Not every section requires every link. The generator must preserve links materially relevant to how the displayed statement was produced.

## 4. Composite Section Contract
A COMPOSITE section may contain multiple source Claims, Evidence items and roles, synthesized Claims, Relations, and Transformation outputs. Each material item should therefore have an object-level anchor or stable reference.

Example — D8.07 Evidence Comparison:
- C1 ← E1 [SUPPORT]
- C2 ← E2 [SUPPORT]
- C3 ← E3 [CONTRADICT]
- C4 ← T1(C1,C2,C3) [SYNTHESIZE]

Rendered prose may combine items into paragraphs, but the underlying references remain distinct.

## 5. Composite Traceability Rules
- **C1 — Evidence identity:** Evidence remains separately identifiable when multiple items are rendered.
- **C2 — Claim identity:** A synthesized paragraph must not erase which Claims are source-derived and which are newly generated.
- **C3 — Evidence role:** SUPPORT, CONTRADICT, CONTEXT, ILLUSTRATE, and BACKGROUND must not be silently collapsed.
- **C4 — Attribution:** Source-derived Claims retain their provenance.
- **C5 — Conflict preservation:** Contradictory Evidence remains visible even when synthesis is generated.
- **C6 — Relation preservation:** “These studies are related” does not create a typed Relation unless its basis is explicitly represented.

## 6. Derived Section Contract
For M3 DERIVED / TRANSFORMATIVE sections, when output materially depends on an operation over identifiable inputs:
- create/reference a Transformation Event;
- identify input references;
- identify output reference(s);
- identify target Claim(s);
- preserve validation state;
- preserve provenance.

For direct restatement, do not create a Transformation Event solely because text was rewritten.

## 7. Transformation Trace Minimum
When material derivation exists, preserve at minimum:
1. Transformation ID;
2. Input Reference(s);
3. Transformation Type;
4. Output Reference(s);
5. Target Claim(s);
6. Evidence Role where relevant;
7. Validation State;
8. Provenance;
9. Revision Reference when applicable.

Candidate types remain ATTRIBUTE, MEASURE, ANALYZE, SYNTHESIZE, MODEL, GENERALIZE, INTERPRET, RECLASSIFY. These are project-level candidate types, not an external standard.

## 8. Traceability Granularity Rule
Traceability should be **as fine-grained as necessary, but no finer than materially useful**.

Do not create one Transformation Event per sentence. Use object-level tracing when a Claim depends on multiple inputs, synthesis changes information structure, a derived conclusion is epistemically consequential, a revision changes a derived result, or provenance would otherwise become ambiguous.

Do not over-trace stylistic edits, grammar correction, simple formatting, or direct restatement without analytical transformation.

## 9. Controlled Fixture A — Composite Evidence Comparison
Input: Study A reports that X increases Y; Study B does not find the same relation; Study C reports that results depend on conditions. Compare their Evidence.

Expected representation:
- C1 = Study A Claim
- E1 = Study A Evidence, SUPPORT(C1)
- C2 = Study B Claim
- E2 = Study B Evidence, CONTRADICT/limits C1
- C3 = Study C conditional Claim
- E3 = Study C Evidence, CONTEXT/SUPPORT(C3)
- R1 = explicit relation between Claims if justified
- T1 = SYNTHESIZE(C1,C2,C3,E1,E2,E3)
- C4 = synthesis Claim, with state determined by Evidence

D8.07 Evidence Comparison and/or D8.12 Synthesis may combine the items, but object-level mapping remains recoverable.

Result: **PASS**

## 10. Controlled Fixture B — Derived Mechanism
Input: The observed sequence is A → B → C. Construct a possible mechanism explaining why the process occurs.

Expected:
- E1 = observation/Evidence for A→B
- E2 = observation/Evidence for B→C
- T1 = ANALYZE / MODEL
- C1 = candidate mechanism Claim
- C1 state = HYPOTHESIS or another supported state, depending on Evidence
- no automatic Verification

D5.07 Provisional Mechanism references T1 and its inputs.

Result: **PASS**

## 11. Controlled Fixture C — Derived Prediction
Input: Assuming current condition X continues, examine whether Y may increase and analyze which conditions would change the prediction.

Expected:
- assumptions/conditions explicitly represented;
- E1 = relevant current-state Evidence;
- T1 = MODEL / GENERALIZE;
- C1 = conditional prediction Claim;
- uncertainty and update conditions preserved.

D6.12 Prediction Result references T1 and relevant inputs.

Result: **PASS**

## 12. Controlled Fixture D — Direct Restatement
Input: Rewrite Study A's conclusion briefly without changing its meaning.

Expected:
- no material Transformation Event;
- provenance retained;
- no new Claim inferred;
- epistemic state unchanged.

Result: **PASS**

## 13. Controlled Fixture E — Revision of a Derived Claim
Previous: T1 produced C1 based on E1 and E2.  
New: E3 materially contradicts E2.

Expected:
- previous T1/C1 preserved historically;
- Revision Event recorded;
- new transformation/re-analysis may produce C2;
- SARA path activated;
- old C1 is not overwritten;
- new state depends on Verification, not merely on E3 existing.

Result: **PASS**

## 14. Reverse Trace Test
For every material derived statement, the system should be able to answer:
1. What Claim is being expressed?
2. What Evidence supports, contradicts, or contextualizes it?
3. What Transformation produced it?
4. What inputs did that Transformation use?
5. What Verification/SARA state applies?
6. What provenance is retained?
7. Which rendered section displays it?

If these questions cannot be answered, traceability is incomplete.

Result: **PASS for controlled fixtures.**

## 15. Traceability Failure Conditions
- **F1 — Prose-only synthesis:** synthesis paragraph exists without underlying Claim/Evidence mapping. FAIL.
- **F2 — Evidence collapse:** multiple Evidence items merged into one generic “evidence” bucket. FAIL.
- **F3 — Transformation disappearance:** a material derived conclusion has no Transformation reference. FAIL.
- **F4 — Transformation inflation:** direct restatement receives a synthetic Transformation Event. FAIL.
- **F5 — Provenance loss:** source-derived content is rendered as model-generated fact. FAIL.
- **F6 — Epistemic inflation:** a derived candidate Claim becomes VERIFIED merely because it is rendered. FAIL.
- **F7 — Revision overwrite:** new Evidence replaces the historical derived Claim without Revision/SARA trace. FAIL.
- **F8 — D9 inflation:** integrated structure is treated as D9 PROMOTED solely because traceability exists. FAIL.

## 16. Composite vs Derived Decision Rule
A section may be both COMPOSITE and DERIVED.

For example, D9.08 Integrable Structure can contain source Claims/Evidence, Relations, a Transformation output, and a candidate integration Claim.

Mapping classes are orthogonal rendering characteristics, not mutually exclusive Document Types.

## 17. Traceability Quality Levels

### L0 — Prose Only
No object-level references. Insufficient for material composite/derived content.

### L1 — Section-Level
Section identifies relevant objects generally. Acceptable only for simple, low-consequence content.

### L2 — Object-Level
Claims/Evidence/Transformations have explicit references. Required for material composite/derived content.

### L3 — Full Chain
Source/Input → Evidence → Transformation → Claim/Result → Verification/SARA → Section. Required when derivation is epistemically consequential or revision-sensitive.

T46 establishes L2 as the default minimum for material composite/derived sections and L3 where epistemic/revision consequences justify it.

## 18. Result
**T46 = PASS**

Controlled fixtures demonstrate that composite sections can preserve object-level Claim/Evidence distinctions, derived sections can preserve Transformation Event references, direct restatement does not require artificial transformation records, revisions can preserve historical derivation and produce a new analysis path, and traceability can coexist with the current collapsed representation.

No new core entity or Notion schema is required.

## 19. Remaining Validation Boundary
T46 validates semantic traceability using controlled fixtures. It does not prove that arbitrary real conversational outputs automatically produce correct object anchors.

Remaining empirical work:
1. actual generated notes with multiple Claims/Evidence;
2. automatic extraction of object anchors from generated prose;
3. traceability after revision;
4. traceability under D9 integration;
5. human review of reverse-trace completeness;
6. persistence representation of trace references where writable.

## 20. Architecture Decision
**RETAIN CURRENT CORE MODEL.**

Claim Transformation Traceability remains a cross-cutting Transformation Event layer. No separate “Traceability” entity, Document Type, or Notion database is justified.

## 21. Next Test
**T47 — Revision / Extension / New-Note Decision Test**

T47 should test decisions among NO_CHANGE, REVISION, EXTENSION, NEW, and BLOCKED when an existing Research Note receives new conversational input.

## 22. Boundary
This is a project-level operational test and specification, not an established academic or industry standard. The human remains the final epistemic decision authority.

---

[Korean source](t46_composite_derived_traceability_test_v0.1.md)
