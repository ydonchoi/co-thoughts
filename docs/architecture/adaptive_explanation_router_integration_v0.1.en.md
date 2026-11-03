# Adaptive Explanation Format Router Integration Design v0.1

> Status: DESIGN PROPOSAL / NOT IMPLEMENTED
> Target: co-thoughts v2.0 Cognitive Router and Adaptive Explanation Format Protocol v0.1
> Scope: An interface design that separates and connects cognitive planning with human-facing explanation-format planning.

## 1. Purpose

Use the cognitive operations and task context selected by the Cognitive Router to produce a provisional explanation-format plan under the Adaptive Explanation Format Protocol.

The design separates **what to think about** from **how to explain the result**. Format selection must not change cognitive operations, evidence quality, verification status, or truth claims.

## 2. Current Implementation and Design Boundary

The inspected implementation currently provides:

- `CognitiveRouter.route()` selects FAST/MIXED/DEEP modes and cognitive operations.
- `route_verification_domains()` returns keyword-based verification-domain hints. It does not perform semantic understanding, automatic claim extraction, or verification.
- `route_workflow_natural_language()` selects predefined problem-solving workflows.
- `CognitiveRuntime` validates backend responses and prevents epistemic-status promotion.
- Adaptive Explanation Format Protocol v0.1 is design guidance, not a runtime media selector.

This document proposes a new router contract and integration point. It does not claim code implementation, actual rendering, media generation, or UI integration.

## 3. Recommended Architecture

```text
REQUEST
  |
  v
COGNITIVE ROUTER
  |-- mode / operations / reasons
  |-- workflow routing
  |-- verification-domain hints
  |
  +------------------------------+
  |                              |
  v                              v
COGNITIVE PLAN             EXPLANATION FORMAT ROUTER
                                  ^
                                  |
                         task + context + output intent
                                  |
                                  v
                         FORMAT PLAN (provisional)
                                  |
                                  v
                         PROJECT ADAPTER / HOST
                                  |
                                  v
                         TEXT / DIAGRAM / IMAGE /
                         INTERACTIVE / VIDEO / SIMULATION
```

The explanation-format router is not a cognitive operation. Both plans are derived in parallel from the same request and are combined at the final output stage.

## 4. Module Responsibilities

### 4.1 Cognitive Router

- Selects the current task mode and cognitive operations.
- Preserves reasons and existing workflow and verification-domain routing results.
- Does not add or remove cognitive operations because of format selection.

### 4.2 Explanation Format Router (proposed)

- Evaluates task purpose, conceptual structure, temporality, data availability, need for user interaction, risk, and requested output medium.
- Selects the least complex format that serves the task.
- Adds secondary formats only when useful.
- Does not report unsupported or unverified capabilities as generated.
- Returns rationale, exclusions, assumptions, uncertainty, and fallback.

### 4.3 Project Adapter / Host

- Applies project-specific `OUTPUT_SCHEMA`, domain rules, user requests, and platform capabilities.
- Checks whether actual renderers and image, video, or web execution capabilities are available.
- Records generation, rendering, functional testing, and source verification separately.

## 5. Draft Input Contract

```python
{
    "task": str,                       # required
    "mode": "FAST" | "MIXED" | "DEEP",
    "operations": list[str],           # Cognitive Router output
    "context": Mapping[str, Any],
    "output_intent": {
        "requested_format": str | None,
        "audience": str | None,
        "detail_level": str | None
    },
    "capabilities": {
        "text": bool,
        "diagram": bool,
        "image": bool,
        "interactive": bool,
        "animation": bool,
        "video": bool,
        "simulation": bool
    }
}
```

The task is the only required input. Missing optional inputs must not be fabricated as facts; use defaults or UNKNOWN. If a requested medium is unsupported, disclose the limitation and offer an alternative.

## 6. Draft Output Contract

```python
{
    "format_plan": {
        "primary": "TEXT",
        "secondary": [],
        "rationale": [],
        "excluded_formats": [],
        "assumptions": [],
        "uncertainties": [],
        "fallback": "TEXT",
        "selection_status": "SELECTED"
    },
    "capability_status": {
        "requested": [],
        "available": [],
        "unavailable": []
    },
    "execution_status": "NOT_RUN",
    "render_status": "NOT_RUN",
    "verification_status": "UNVERIFIED",
    "is_evidence": False
}
```

Candidate format identifiers: TEXT, DIAGRAM, IMAGE, INTERACTIVE, ANIMATION, VIDEO, SIMULATION. Before implementation, check compatibility with existing project schemas and finalize the enum.

## 7. Selection Rules

| Condition | Default format | Secondary format |
|---|---|---|
| Definitions, short explanations, precise conditions | TEXT | Table |
| Static components and relationships | TEXT or DIAGRAM | Explanatory prose |
| Procedures, branches, state transitions | DIAGRAM | Step-by-step text |
| Claim, evidence, and competing-hypothesis comparison | TEXT + DIAGRAM | Evidence table |
| Space, appearance, and shape | TEXT + IMAGE | Annotated illustration |
| Time-dependent behavior | TEXT + ANIMATION/VIDEO | Script |
| Variable manipulation and conditional exploration | TEXT + INTERACTIVE | Static result table |
| Assumption-based outcome comparison | TEXT + SIMULATION | Sensitivity table |

Selection priority:

1. Explicit user format and accessibility requirements
2. Project adapter output schema and domain constraints
3. Information structure required by the task
4. Capabilities actually available in the host
5. Production cost and complexity

TEXT is the default for simple tasks. Do not add visual media unless it materially improves understanding or decision-making.

## 8. Invariants and Safeguards

1. **Format ≠ Cognition:** Explanation format does not replace cognitive operations.
2. **Format ≠ Evidence:** Diagrams, images, videos, and simulations are not evidence by themselves.
3. **Rendering ≠ Verification:** Successful rendering is not successful fact verification.
4. **Selection ≠ Generation:** Selecting a medium does not mean it has been generated.
5. **Generation ≠ Functional Test:** Creating a file does not verify interaction or operation.
6. **Agreement ≠ Evidence:** User agreement or persuasive presentation cannot raise verification status.
7. **Epistemic State Preservation:** Preserve the meaning of FACT/INTERPRETATION/INFERENCE/HYPOTHESIS/SIMULATION and VERIFIED/PARTIALLY VERIFIED/UNVERIFIED/CONTRADICTED.
8. **Human Agency:** Final interpretation and decision authority remain with the human.
9. **Capability Honesty:** Never claim an unavailable capability is available.
10. **Progressive Disclosure:** Present the core result first and make detailed evidence and source data expandable.

## 9. Errors and Fallback Behavior

- Insufficient input: TEXT with explicit assumptions or one necessary clarification.
- Unsupported medium: TEXT fallback and reason for non-support.
- Rendering failure: preserve the selection but set render_status=FAILED.
- Functional test not run: set functional_test_status=NOT_RUN.
- Unknown data source: disclose the unknown source; do not add visual authority.
- High-risk decisions: do not present visualization as the sole conclusion; include evidence, uncertainty, and need for expert review.

## 10. Phased Implementation Plan

### Phase 0 — Design Baseline
- Review and approve this contract.
- Finalize format enum and input/output schemas.
- Check compatibility with the Cognitive Router and Project Adapter.

### Phase 1 — Pure Rule-Based Selector
- Implement a deterministic format planner without external generation capabilities.
- Handle user-requested formats, text defaults, and capability fallback.
- Return rationale and uncertainty.

### Phase 2 — Cognitive Router Integration
- Add `format_routing` to `route()` output or expose a separate public API.
- Preserve the semantics and results of existing `operations`, `verification_routing`, and `workflow_routing`.
- Add backward-compatibility tests.

### Phase 3 — Host/Adapter Rendering Integration
- Connect only renderers that are actually available.
- Record generation, rendering, functional testing, and source verification separately.
- Verify text fallback when rendering fails.

### Phase 4 — Evaluation and Promotion
- Evaluate selection accuracy, unnecessary media generation, fallback, and accessibility across representative task groups.
- Promote implementation status only after independent and regression tests pass.

## 11. Minimum Test Criteria

- Simple translation, definition, and calculation select TEXT.
- Explanations of static component relationships consider DIAGRAM.
- Time-dependent explanations select ANIMATION/VIDEO only when available; otherwise use TEXT fallback.
- INTERACTIVE is not marked as completed when variable manipulation is unavailable.
- If a requested format conflicts with a project output schema, report the conflict rather than silently overriding the schema.
- Format routing never promotes verification_status.
- Format routing does not change existing cognitive-operation or verification-routing results.
- Selection, generation, rendering, and functional-test states are validated independently.

## 12. Current Status

- Design document: authored
- Existing runtime integration: not implemented
- New format planner: not implemented
- Renderer integration: not implemented
- Tests: implementation tests for this design not run
- Independent verification: not performed

This document is a design baseline for future implementation. It must not be treated as a runtime capability until implementation and test evidence exist.
