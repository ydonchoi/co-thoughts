# T46 — Composite / Derived Section Traceability Test v0.1

Status: **PASS — OBJECT-LEVEL TRACEABILITY RULES VALIDATED WITH CONTROLLED FIXTURES**

## 1. Purpose

T46 tests whether generated research-note sections can preserve traceability when a single section contains:

1. multiple Claims and Evidence items (COMPOSITE); or
2. a derived result whose interpretation depends materially on one or more Transformation Events (DERIVED / TRANSFORMATIVE).

The test verifies that document rendering does not collapse logical objects into prose.

## 2. Scope

T46 builds directly on:

- T41 M2 Composite mapping;
- T41 M3 Derived/Transformative mapping;
- T42 conditional rendering;
- T43 cross-type consistency;
- T44 semantic stability;
- T45 traceability fixtures.

No new core logical entity is introduced.

## 3. Traceability Chain

The minimum traceability chain is:

**Source / Input**
→ **Evidence**
→ **Transformation Event**
→ **Claim / Result**
→ **Rendered Section**

Not every section requires every link.

The generator must preserve the links that are materially relevant to how the displayed statement was produced.

## 4. Composite Section Contract

A COMPOSITE section may contain:

- multiple source Claims;
- multiple Evidence items;
- multiple Evidence roles;
- synthesized Claims;
- Relations;
- Transformation outputs.

Therefore each material item should have an object-level anchor or stable reference.

Example:

Section: D8.07 근거 비교

- C1 ← E1 [SUPPORT]
- C2 ← E2 [SUPPORT]
- C3 ← E3 [CONTRADICT]
- C4 ← T1(C1,C2,C3) [SYNTHESIZE]

The rendered prose may combine these into paragraphs, but the underlying references remain distinct.

## 5. Composite Traceability Rules

### C1 — Evidence identity

Evidence must remain separately identifiable when multiple items are rendered.

### C2 — Claim identity

A synthesized paragraph must not erase which Claims are source-derived and which are newly generated.

### C3 — Evidence role

SUPPORT, CONTRADICT, CONTEXT, ILLUSTRATE, and BACKGROUND roles must not be silently collapsed.

### C4 — Attribution

Source-derived Claims retain their provenance.

### C5 — Conflict preservation

Contradictory Evidence remains visible even when a synthesis paragraph is generated.

### C6 — Relation preservation

A textual statement such as “these studies are related” does not create a typed Relation unless the relation basis is explicitly represented.

## 6. Derived Section Contract

For M3 DERIVED / TRANSFORMATIVE sections:

If the output materially depends on an operation over identifiable inputs:

- create/reference a Transformation Event;
- identify input references;
- identify output reference(s);
- identify target Claim(s);
- preserve validation state;
- preserve provenance.

If the content is a direct restatement:

- do not create a Transformation Event solely because text was rewritten.

## 7. Transformation Trace Minimum

When material derivation exists, the trace should minimally preserve:

1. Transformation ID;
2. Input Reference(s);
3. Transformation Type;
4. Output Reference(s);
5. Target Claim(s);
6. Evidence Role where relevant;
7. Validation State;
8. Provenance;
9. Revision Reference when applicable.

Candidate transformation types remain:

- ATTRIBUTE
- MEASURE
- ANALYZE
- SYNTHESIZE
- MODEL
- GENERALIZE
- INTERPRET
- RECLASSIFY

These are project-level candidate types, not an external standard.

## 8. Traceability Granularity Rule

Traceability should be **as fine-grained as necessary, but no finer than materially useful**.

Do not create an individual Transformation Event for every sentence.

Use object-level tracing when:

- a claim depends on multiple inputs;
- a synthesis changes the information structure;
- a derived conclusion is epistemically consequential;
- a revision changes a derived result;
- provenance would otherwise become ambiguous.

Do not over-trace:

- stylistic edits;
- grammar correction;
- simple formatting;
- direct restatement without analytical transformation.

## 9. Controlled Fixture A — Composite Evidence Comparison

Input:

“연구 A는 X가 Y를 증가시킨다고 보고했다. 연구 B는 같은 관계를 찾지 못했다. 연구 C는 조건에 따라 결과가 달라진다고 보고했다. 세 연구의 근거를 비교해 보자.”

Expected object representation:

- C1 = Study A claim
- E1 = Study A evidence, SUPPORT(C1)
- C2 = Study B claim
- E2 = Study B evidence, CONTRADICT/limits C1
- C3 = Study C conditional claim
- E3 = Study C evidence, CONTEXT/SUPPORT(C3)
- R1 = explicit relation between claims if justified
- T1 = SYNTHESIZE(C1,C2,C3,E1,E2,E3)
- C4 = synthesis claim, state determined by evidence

Expected rendering:

D8.07 근거 비교 and/or D8.12 종합 may combine these items, but the object-level mapping remains recoverable.

Result: **PASS**

## 10. Controlled Fixture B — Derived Mechanism

Input:

“관찰된 순서는 A → B → C이다. 이 과정이 왜 발생하는지 설명하는 가능한 메커니즘을 구성해 보자.”

Expected:

- E1 = observation/evidence for A→B
- E2 = observation/evidence for B→C
- T1 = ANALYZE / MODEL
- C1 = candidate mechanism claim
- C1 state = HYPOTHESIS or appropriate supported state, depending evidence
- no automatic Verification

Expected rendering:

D5.07 잠정 메커니즘 references T1 and its inputs.

Result: **PASS**

## 11. Controlled Fixture C — Derived Prediction

Input:

“현재 조건 X가 유지된다는 가정에서 Y가 증가할 가능성을 검토하고, 어떤 조건에서 예측이 달라지는지 분석해 보자.”

Expected:

- assumptions/conditions explicitly represented;
- E1 = relevant current-state evidence;
- T1 = MODEL / GENERALIZE;
- C1 = conditional prediction claim;
- uncertainty and update conditions preserved.

Expected rendering:

D6.12 예측 결과 references T1 and relevant inputs.

Result: **PASS**

## 12. Controlled Fixture D — Direct Restatement

Input:

“연구 A의 결론을 같은 의미로 간단하게 다시 써줘.”

Expected:

- no material Transformation Event;
- provenance retained;
- no new Claim inferred;
- epistemic state unchanged.

Result: **PASS**

## 13. Controlled Fixture E — Revision of Derived Claim

Input:

Previous:
T1 produced C1 based on E1 and E2.

New:
E3 materially contradicts E2.

Expected:

- previous T1/C1 preserved historically;
- Revision Event recorded;
- new transformation/re-analysis may produce C2;
- SARA path activated;
- old C1 is not overwritten;
- new state depends on Verification, not merely on E3 existence.

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

Result: **PASS for the controlled fixtures.**

## 15. Traceability Failure Conditions

### F1 — Prose-only synthesis

A synthesis paragraph exists but no underlying Claim/Evidence mapping.

Result: FAIL.

### F2 — Evidence collapse

Multiple Evidence items are merged into one generic “근거”.

Result: FAIL.

### F3 — Transformation disappearance

A material derived conclusion has no Transformation reference.

Result: FAIL.

### F4 — Transformation inflation

A direct restatement receives a synthetic Transformation Event.

Result: FAIL.

### F5 — Provenance loss

Source-derived content is rendered as model-generated fact.

Result: FAIL.

### F6 — Epistemic inflation

A derived candidate Claim becomes VERIFIED merely because it is rendered.

Result: FAIL.

### F7 — Revision overwrite

New Evidence replaces the historical derived Claim without a Revision/SARA trace.

Result: FAIL.

### F8 — D9 inflation

A synthesized integrated structure is treated as D9 PROMOTED solely because traceability exists.

Result: FAIL.

## 16. Composite vs Derived Decision Rule

A section may be both COMPOSITE and DERIVED.

Example:

D9.08 통합 가능한 구조 can contain:
- source Claims/Evidence;
- Relations;
- a Transformation output;
- a candidate integration Claim.

Therefore mapping classes are orthogonal rendering characteristics, not mutually exclusive document types.

## 17. Traceability Quality Levels

### L0 — Prose Only

No object-level references.

Insufficient for material composite/derived content.

### L1 — Section-Level

Section identifies relevant objects generally.

Acceptable only for low-consequence/simple content.

### L2 — Object-Level

Claims/Evidence/Transformations have explicit references.

Required for material composite/derived content.

### L3 — Full Chain

Source/Input → Evidence → Transformation → Claim/Result → Verification/SARA → Section.

Required when the derivation is epistemically consequential or revision-sensitive.

T46 establishes L2 as the default minimum for material composite/derived sections and L3 when epistemic/revision consequences justify it.

## 18. Result

**T46 = PASS**

Controlled fixtures demonstrate that:

- Composite sections can preserve object-level Claim/Evidence distinctions.
- Derived sections can preserve Transformation Event references.
- Direct restatement does not require artificial transformation records.
- Revision can preserve historical derivation and generate a new analysis path.
- Traceability can coexist with the current collapsed representation.
- No new core entity or Notion schema is required.

## 19. Remaining Validation Boundary

T46 validates semantic traceability using controlled fixtures.

It does not yet prove that arbitrary real conversational outputs will automatically produce correct object anchors.

Remaining empirical work:

1. actual generated notes with multiple Claims/Evidence;
2. automatic extraction of object anchors from generated prose;
3. traceability after revision;
4. traceability under D9 integration;
5. human review of reverse-trace completeness;
6. persistence representation of trace references where writable.

## 20. Architecture Decision

**RETAIN CURRENT CORE MODEL.**

Claim Transformation Traceability remains a cross-cutting Transformation Event layer.

No separate “Traceability” entity, Document Type, or Notion database is justified.

## 21. Next Test

**T47 — Revision / Extension / New-Note Decision Test**

T47 should test whether the template system can correctly decide among:

- NO_CHANGE
- REVISION
- EXTENSION
- NEW
- BLOCKED

when an existing research note receives new conversational input.

## 22. Boundary

This is a project-level operational test and specification. It is not an established academic or industry standard.

Human remains final epistemic decision authority.
