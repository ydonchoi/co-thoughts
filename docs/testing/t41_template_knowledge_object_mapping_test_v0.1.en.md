# T41 — Template ↔ Knowledge Object Mapping Test v0.1

Status: **PASS — SEMANTIC MAPPING VALIDATED WITH CONDITIONAL AREAS**

## 1. Purpose
T41 tests whether D1–D9 template sections can represent the Research Note Engine's logical objects without semantic inflation or conflation.

Tested logical layers:
- Research Object
- Claim
- Evidence
- Transformation Event
- Verification
- Relation
- Provenance
- Version / Revision
- D9 Gate

The test evaluates mapping semantics, not Notion queryability.

## 2. Mapping Principle
A document section is a **rendering location**, not automatically a knowledge object.

Section ≠ Research Object / Claim / Evidence / Verification / Transformation / Relation.

A section may render one or more referenced objects, but the identity of each underlying object must remain explicit.

## 3. Mapping Classes

### M1 — DIRECT
The section has a clear dominant logical object.

Examples:
- D1.01 Object → Research Object
- D4.12 Verification Status → Verification / epistemic-state rendering
- D9.01 Source Notes → Research Object / Research Note references

### M2 — COMPOSITE
The section intentionally renders multiple object types.

Examples:
- D5.10 Evidence → Evidence mapped to mechanism Claims
- D8.07 Evidence Comparison → Evidence + Claims + Transformation
- D9.08 Integrable Structure → Relation + Transformation + candidate Claim

Composite sections must preserve object-level distinctions.

### M3 — DERIVED / TRANSFORMATIVE
The section primarily represents an output produced through a Transformation Event.

Examples:
- D1.06 Provisional Structure
- D1.09 Generated Hypothesis / Model
- D6.12 Prediction Result
- D8.12 Synthesis
- D9.09 Integrated Explanation / Model

These outputs are not automatically Evidence or Verification.

### M4 — CONTEXT / CONTROL
The section provides scope, boundary, process, or state control.

Examples:
- Scope / Boundary
- D8.02 Inclusion Criteria
- D6.10 Uncertainty
- D7.03 Evaluation Criteria

These may affect Claims and transformations but are not automatically Claims or Evidence.

## 4. Cross-Type Mapping Matrix

| Template area | Dominant object | Secondary object(s) | Mapping class |
|---|---|---|---|
| Target | Research Object | Research Note | M1 |
| Research Question | Research Object / Question | Claim context | M1 |
| Scope / Boundary | Research Object | Claim / Evidence conditions | M4 |
| Current Knowledge | Claims | Evidence / Provenance | M2 |
| Phenomenon / Problem | Research Object | Claims / Evidence | M2 |
| Pattern / Clue | Evidence-derived result | Claim / Transformation | M3 |
| Provisional Structure | Transformation output | Relation / Claim | M3 |
| Definition | Claim / attributed representation | Provenance | M2 |
| Relation Structure | Relation | Claims / Evidence | M2 |
| Process | Transformation / result representation | Claims / Relations | M3 |
| Mechanism | Claim / Model | Evidence / Transformation | M3 |
| Evidence | Evidence | Target Claims / Relations | M1 |
| Counter-evidence | Evidence | Contradicted Claims | M1 |
| Verification State | Verification / Epistemic State | Claim | M1 |
| Prediction | Claim / Model output | Evidence / Conditions | M3 |
| Evaluation Criteria | Evaluation structure | Evidence / Claim | M4 |
| Evaluation Judgment | Claim | Criteria / Evidence / Verification | M2 |
| Literature Synthesis | Transformation result | Claims / Evidence | M3 |
| Integrated Structure | Transformation result | Relations / Claims | M3 |
| Provenance | Provenance | All referenced objects | M1 |
| Revision History | Version / Revision Event | Claim / Evidence / Transformation changes | M1 |
| D9 Gate | D9 Gate | Claims / Relations / Evidence / SARA | M1 |

## 5. Critical Semantic Tests

### C1. Evidence Inflation — PASS
A section named “Evidence” is not itself Evidence. Evidence identity must remain separately identifiable.

### C2. Claim Inflation — PASS
A generated section such as “Synthesis,” “Prediction Result,” or “Judgment” does not automatically become a VERIFIED Claim. Claim state remains separately represented.

### C3. Transformation Inflation — PASS
A process or synthesis section may represent a Transformation Event/result, but operation and result remain distinct.

### C4. Verification Inflation — PASS
A “Verification Status” display renders Verification / epistemic state. Its presence does not itself create a Verification record.

### C5. Relation Inflation — PASS
A section such as “Commonalities” or “Relational Structure” may render Relations, but textual similarity alone does not create a typed Relation without an explicit basis.

### C6. Provenance Preservation — PASS
Definitions, literature claims, historical statements, and interpretations can retain source/attribution provenance without collapsing into a single source for all claims.

### C7. D9 Promotion Inflation — PASS
D9 template rendering does not imply D9 PROMOTED. D9 Gate remains a separate promotion mechanism.

### C8. Revision Inflation — PASS
A revised section does not overwrite the previous epistemic state. Revision remains a Version / Revision Event.

## 6. Type-Specific Risk Areas

### D1
“Patterns / Clues” can become unsupported pattern inference if Evidence is not explicit.  
Control: require identifiable Evidence/observation and label generated structure as provisional.

### D3
“Adopted Conceptualization” can be mistaken for a universally correct definition.  
Control: preserve attribution and mark a project-adopted conceptualization as a working representation.

### D4
“Impact” and “Causal Interpretation” can inflate association into causality.  
Control: causal language must track Evidence and verification.

### D5
“Provisional Mechanism” can become a fabricated explanatory mechanism.  
Control: require an Evidence/analysis basis and preserve provisional status.

### D6
“Prediction Result” can be mistaken for a future fact.  
Control: retain assumptions, horizon, uncertainty, and update conditions.

### D7
“Judgment” can conceal normative criteria or unsupported recommendations.  
Control: make criteria and Evidence linkage explicit.

### D8
“Agreement” can erase heterogeneity and disagreement.  
Control: preserve study-level claims, contradictory Evidence, methodological differences, and scope.

### D9
“Integrable Structure” can be mistaken for a verified new theory/model.  
Control: represent it as transformation output/candidate Claim and apply D9 Gate separately.

## 7. Coverage Result
All nine Document Types have at least one valid mapping path to the core logical layers.

No Document Type requires a new logical entity. No mapping requires treating Document Type as epistemic state or Research Note as Evidence.

## 8. Conditional Findings
The mapping is semantically valid, but three areas require explicit implementation rules in later tests:

1. **Composite sections** need object-level anchors when multiple Claims/Evidence items are rendered.
2. **Derived sections** need Transformation Event references when the derivation materially matters.
3. **Verification displays** need to distinguish a display of state from an underlying Verification record.

These are implementation requirements, not reasons to expand the core data model.

## 9. Decision
**T41 = PASS**

D1–D9 template sections can be mapped to the Research Note Engine's logical objects without semantic inflation, provided object-level references and transformation/provenance links are preserved where applicable.

Architecture expansion is not justified.

## 10. Next Test
**T42 — Template Generation Rules / Conditional Rendering Test**

T42 should specify when sections are rendered, omitted, marked unresolved, or escalated for human decision, and test whether generation rules prevent unsupported content from filling template slots.

## 11. Boundary
This is a project-level semantic mapping test, not a claim that the template architecture is an established academic standard. The human remains the final epistemic decision authority.

---

[Korean source](t41_template_knowledge_object_mapping_test_v0.1.md)
