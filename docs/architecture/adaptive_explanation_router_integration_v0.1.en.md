# Adaptive Explanation Format Router Integration Design v0.1

> Status: PARTIALLY IMPLEMENTED — planner and Cognitive Router integration are on `main` (PRs #2–#18, #25–#26); Host/Adapter interface has a reference implementation (`format_host.py`); a DIAGRAM renderer (`diagram_renderer.py`, Mermaid flowchart subset → SVG) is connected; no other renderer is
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

The rule-based planner and its Cognitive Router connection are on `main` (PR #2, with follow-up improvements #3–#18). Actual rendering, media generation, and UI integration are not implemented. CI results are tracked per commit in GitHub Actions and are not recorded here, so this document does not go stale.

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

### 4.2 Explanation Format Router (implemented: rule-based planner)

- The v0.1 implementation evaluates explicit format requests, a limited set of task keywords, predefined boolean context signals, and host capability declarations.
- It does not semantically assess user expertise, detail level, risk, or data quality. Those remain future evaluation and improvement targets.
- Selects the least complex format that serves the task.
- Adds secondary formats only when useful.
- Does not report unsupported or unverified capabilities as generated.
- Returns rationale, exclusions, assumptions, uncertainty, and fallback.

### 4.3 Project Adapter / Host

- Applies project-specific `OUTPUT_SCHEMA`, domain rules, user requests, and platform capabilities.
- Checks whether actual renderers and image, video, or web execution capabilities are available.
- Records generation, rendering, functional testing, and source verification separately.

## 5. Input Contract (implementation baseline)

```python
{
    "task": str,                       # required
    "mode": "FAST" | "MIXED" | "DEEP",
    "operations": list[str],           # Cognitive Router output
    "context": Mapping[str, Any],
    "output_intent": {
        "requested_format": str | None,
        "audience": str | None,      # reserved; not used by planner v0.1
        "detail_level": str | None,  # reserved; not used by planner v0.1
        "accessibility": {           # optional; all default False
            "screen_reader": bool,
            "reduced_motion": bool,
            "captions": bool,
            "text_only": bool
        }
    },
    "output_schema": {                 # optional; project adapter constraint
        "allowed_formats": list[str]   # non-empty, must include TEXT
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

## 6. Output Contract (implementation baseline)

```python
{
    "format_plan": {
        "primary": "TEXT",
        "secondary": [],
        "rationale": [],
        "excluded_formats": [],
        "assumptions": [],
        "uncertainties": [],
        "fallback": None,
        "selection_status": "SELECTED",   # SELECTED | FALLBACK | CONFLICT | INVALID_INPUT
        "conflicts": [],
        "accessibility_requirements": []  # e.g. ["TEXT_ALTERNATIVE", "CAPTIONS"]
    },
    "capability_status": {
        "requested": [],
        "available": [],
        "unavailable": []
    },
    "execution_status": "NOT_RUN",
    "render_status": "NOT_RUN",
    "functional_test_status": "NOT_RUN",
    "verification_status": "UNVERIFIED",
    "is_evidence": False
}
```

Plan field semantics: `fallback` is the format to use if rendering `primary` fails and is `None` when `primary` is already TEXT (including FALLBACK and INVALID_INPUT plans). `excluded_formats` lists the candidate that was considered but not selected (FALLBACK), otherwise `[]`. `secondary` is reserved; v0.1 plans a single primary format and returns `[]`. The output schema (`output_schema.allowed_formats`) is a constraint declared by the project adapter; when absent there is no constraint. If the user's explicit `requested_format` is not in the schema, the planner does not override the schema: it returns `selection_status=CONFLICT`, a TEXT plan, `excluded_formats=[requested]`, and records `{"type": "REQUESTED_FORMAT_NOT_IN_OUTPUT_SCHEMA", "requested_format", "allowed_formats"}` in `conflicts`; the user or project owner resolves the conflict. A task-inferred format outside the schema is not a conflict but a `FALLBACK` to TEXT. A schema-allowed format without host capability is a `FALLBACK` as before. With no conflict, `conflicts` is `[]`.

Accessibility input (`output_intent.accessibility`, §7 priority 1) is evaluated before the schema. `text_only` excludes every non-TEXT format and `reduced_motion` excludes ANIMATION and VIDEO. If the user's explicit format is excluded, the requirement is not overridden: the planner returns `CONFLICT` (TEXT plan) with `{"type": "REQUESTED_FORMAT_CONFLICTS_WITH_ACCESSIBILITY", "requested_format", "requirement"}`; an excluded inferred format is a `FALLBACK`. When accessibility and schema conflicts coexist, all are recorded in `conflicts` in priority order (accessibility → schema). `screen_reader` and `captions` exclude nothing; they return obligations the host must meet for the selected `primary` in `accessibility_requirements`: `TEXT_ALTERNATIVE` for a non-TEXT `primary` with `screen_reader`, `CAPTIONS` for VIDEO with `captions`. The planner neither fulfils nor verifies these obligations (rendering and functional tests are Phase 3). Display settings unrelated to format choice (high contrast, font size) are not part of this input (unknown keys are errors). Context signals are evaluated in a fixed precedence: `simulation_required` > `requires_interaction` > `time_dependent_behavior` > `visual_subject` > `process_or_structure` = `has_competing_hypotheses`; any true signal takes precedence over task keywords.

Format identifiers: TEXT, DIAGRAM, IMAGE, INTERACTIVE, ANIMATION, VIDEO, SIMULATION. Non-text capabilities are considered available only when explicitly declared by the host. If no capability map is supplied, only TEXT is assumed available.

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
- Invalid format-planning input (non-boolean context signal, unknown or non-boolean capability key, `text: false`, unsupported `requested_format`, invalid `output_schema` — e.g. `OUTPUT_SCHEMA_INVALID`, `OUTPUT_SCHEMA_UNKNOWN_FIELD:<key>`, `OUTPUT_SCHEMA_ALLOWED_FORMATS_INVALID`, `OUTPUT_SCHEMA_FORMAT_UNSUPPORTED:<format>`, `OUTPUT_SCHEMA_TEXT_REQUIRED`, invalid accessibility input — `ACCESSIBILITY_INVALID`, `ACCESSIBILITY_INVALID:<key>`, `ACCESSIBILITY_UNKNOWN:<key>`): `route_explanation_format()` raises `ValueError` with a stable code (e.g. `CAPABILITY_UNKNOWN:<key>`). The public `cognitive_router.route()` does not propagate it; `format_routing` returns a TEXT plan with `selection_status=INVALID_INPUT` and the code in `error`, so cognitive and verification routing are unaffected.
- Shared request fields (`request` mapping, `task` non-blank string, `context` mapping defaulting to `{}` only when absent or `None`) are validated by `request_validation.validate_routing_request()` in the Cognitive Router, the format planner, and the runtime `SafetyGate`; `mode` likewise defaults to `MIXED` only when absent or `None` and is case-normalized (`normalize_mode()`), and the runtime passes the normalized request to the backend, so invalid shared fields raise `REQUEST_MUST_BE_MAPPING` / `TASK_REQUIRED` / `CONTEXT_INVALID` from `route()` before any routing. `INVALID_INPUT` applies only to format-specific fields.
- Keyword hints: ASCII keywords match whole words (simple plural/past suffixes allowed); Korean keywords match as substrings, with an inflection-aware exclusion list for known collisions (e.g. "big picture", "draws upon", "그림자", "영상의학"). A keyword selects a non-TEXT format only with a request cue (request verb nearby, "as/in/with a …", a leading format noun, an imperative verb keyword, or Korean `로/으로` or particle + request verb); a format word used only as the topic stays TEXT.

## 10. Phased Implementation Plan

### Phase 0 — Design Baseline
- Finalize the design contract and format enum.
- Define input/output schemas.
- Cognitive Router compatibility review (complete).

### Phase 1 — Pure Rule-Based Selector (implemented)
- Deterministic planner added in `src/co_thoughts/explanation_format_router.py`.
- Handles explicit requests, text defaults, and capability fallback.
- Returns rationale, assumptions, uncertainty, and status.
- Does not generate or render non-text media.

### Phase 2 — Cognitive Router Integration (implemented, on `main`)
- Adds `format_routing` to `route()` output.
- Integrates while preserving existing `operations`, `verification_routing`, and `workflow_routing` semantics.
- Adds unit and integration regression tests.
- Shared request validation unified across the Cognitive Router, format planner, runtime `SafetyGate`, and the v1.3 execution request (PRs #6–#8).

### Phase 3 — Host/Adapter Rendering Integration (interface implemented, DIAGRAM renderer connected)
- Connect only renderers that are actually available.
- Record generation, rendering, functional testing, and source verification separately.
- Verify text fallback when rendering fails.

`src/co_thoughts/format_host.py` (reference implementation, unit-tested with fake renderers):

- `RendererRegistry`: renderers are registered explicitly per format; nothing is connected by default and TEXT is not registrable. A renderer implements `render(payload) -> {"artifact": …}`; INTERACTIVE/SIMULATION renderers must also implement `functional_test(artifact) -> {"passed": bool}` to be delivered.
- `FormatHost.prepare_request(request)`: rewrites `capabilities` from registered renderers only (callers cannot claim a capability) and replaces `output_schema` with the host's configured schema (removed if none). An invalid schema fails at host construction, and the schema is kept as an immutable snapshot taken then.
- `FormatHost.deliver(format_routing, content)`: takes `content["text"]` (the TEXT version, always required) plus optional `media` (`{FORMAT: payload}`), `text_alternative`, `captions`, executes the plan, and returns a per-stage record: `generation_status` (content supplied), `render_status`, `functional_test_status`, `accessibility_status` (MET/NOT_MET per obligation), `source_verification_status` (always `NOT_RUN`), `verification_status=UNVERIFIED`, `is_evidence=False`.
- Fallback reasons (`fallback_reason`): `FORMAT_NOT_IN_OUTPUT_SCHEMA` (plans made outside the host are re-checked against the host schema), `MEDIA_CONTENT_MISSING`, `ACCESSIBILITY_REQUIREMENT_NOT_MET:<obligation>` (checked before rendering), `RENDERER_NOT_CONNECTED`, `RENDER_FAILED:<exception>`, `RENDER_OUTPUT_INVALID` (not a mapping, or `artifact` missing or `None`), `FUNCTIONAL_TEST_UNAVAILABLE`, `FUNCTIONAL_TEST_FAILED`, `FUNCTIONAL_TEST_ERROR:<exception>`. In every case `planned_format` (the selection) is preserved and TEXT is delivered.
- Renderer output fields `verification_status`, `is_evidence`, `verified`, `is_verified` are dropped. The plan object is not modified.

DIAGRAM renderer `src/co_thoughts/diagram_renderer.py` (`MermaidFlowchartRenderer`, no external dependencies):

- Supported subset: header `graph`/`flowchart` + `TD`/`TB`/`LR` (including the compact `graph TD; A --> B` form with statements after `;` on the header line); nodes `id`, `id[label]`, `id(label)` (rounded), `id{label}` (decision); edges `-->` (arrow) and `---` (line), labels `-->|label|` and `-- label -->`, chains `A --> B --> C`; `%%` comments, `;` separators (a `;` inside quotes, brackets or `|label|` is label text). Anything else (`subgraph`, `==>`, `&`, circle/cross edges `---o`/`---x`/`-->o`/`-->x`, other diagram types, …) and XML-forbidden control characters (`DIAGRAM_INVALID_CHARACTER`) raise `DiagramSyntaxError` with a stable code (`DIAGRAM_HEADER_UNSUPPORTED`, `DIAGRAM_SYNTAX_UNSUPPORTED:line N`, `DIAGRAM_NODE_REDEFINED:<id>`, …), so the host records `RENDER_FAILED:DiagramSyntaxError` and delivers TEXT. It never guesses a drawing.
- Limits: 200 nodes, 400 edges, 200-character labels, 20,000-character source.
- Layout: deterministic breadth-first layering from nodes without incoming edges (cycles allowed). Only edges between adjacent layers are straight; back, same-layer, self-loop and layer-skipping edges are routed through a dedicated lane beside the diagram (right for TD, below for LR) so they never cross other nodes. Parallel edges between the same two nodes are offset from each other, with staggered labels. Every text block is sized to fit inside its shape (a decision diamond's inscribed rectangle is half its size, so it gets twice the text area). Edge labels also wrap at 120 px; layer, row/column and lane gaps grow to fit them, and the SVG size is the bounding box of everything drawn. Labels wrap by rendered width (wide CJK glyphs counted wider) with boxes sized to fit, and are XML-escaped.
- Accessibility: the SVG has `role="img"`, `aria-labelledby` pointing at per-document unique ids (content hash + per-renderer counter), `<title>` (default "Flowchart", overridable via payload `title`) and `<desc>` (payload `description` or an automatic node/edge summary). The host's `TEXT_ALTERNATIVE` obligation is still checked separately against `content["text_alternative"]`.
- Output: `{"artifact": SVG string, "mime_type": "image/svg+xml", "node_count", "edge_count", "summary"}`. Rendering does not verify the diagram's content.
- Registration: `registry.register("DIAGRAM", MermaidFlowchartRenderer())`. Tests check SVG well-formedness (XML parse), node/edge counts, layout direction, escaping, `<title>`/`<desc>`, and delivery, failure fallback, and accessibility blocking through the host, separately.

### Phase 4 — Evaluation and Promotion
- v0.1 keyword evaluation: `docs/testing/format_routing_keyword_eval_v0.1.en.md` (77 author-labeled tasks; overall 0.623, unnecessary-media rate 0.452 driven by topic mentions, paraphrase recall 0). Request-cue gating (section 7 of that report) brings the held-out set (38 cases) from 0.526 to 0.842 and its unnecessary-media rate from 0.619 to 0.048. Paraphrase recognition (section 8) raises paraphrase recall on a second held-out set (40 cases) from 0/20 to 18/20, with one new false positive in 16 TEXT tasks. Context checks for self-cued phrases (section 9) bring a third held-out set (20 cases) from 8/20 to 20/20, and 11/12 on fresh probes outside every set. Review follow-ups for PRs #13–#18 are in report sections 8.5, 9.5, and 9.6.
- Evaluate selection accuracy, unnecessary media generation, fallback, and accessibility across representative task groups.
- Promote implementation status only after independent and regression tests pass.

## 11. Minimum Test Criteria

- Simple translation, definition, and calculation select TEXT.
- Explanations of static component relationships consider DIAGRAM.
- Time-dependent explanations select ANIMATION/VIDEO only when available; otherwise use TEXT fallback.
- INTERACTIVE is not marked as completed when variable manipulation is unavailable.
- If a requested format conflicts with a project output schema, report the conflict rather than silently overriding the schema. (Implemented and unit-tested: `selection_status=CONFLICT`, `conflicts`.)
- The user's accessibility requirements (`text_only`, `reduced_motion`) take precedence over format selection and are reported when they conflict with an explicit request; `screen_reader`/`captions` pass host obligations in `accessibility_requirements`. (Implemented and unit-tested.)
- Format routing never promotes verification_status.
- Format routing does not change existing cognitive-operation or verification-routing results.
- Selection, generation, rendering, and functional-test states are validated independently.

## 12. Current Status

| Area | Status | Evidence |
|---|---|---|
| Format planner (rule-based) | Implemented, on `main` | PR #2, improvements #3–#18 |
| Cognitive Router integration | Implemented, on `main` | PR #2 |
| Shared request validation | Implemented | PRs #6–#8 |
| Format-selection evaluation | In-project measurement | dev 77/77, held-out v0.1 37/38, v0.2 37/40, v0.3 20/20, fresh probes outside all sets 11/12 (`docs/testing/format_routing_keyword_eval_v0.1.en.md`) |
| Independent evaluation | Not performed (deferred by the project owner, 2026-11-04) | Only the guidelines are on `main` (PR #20); the annotator-A data PR #23 was closed without merging. All sets and labels share one author |
| Output-schema conflict reporting | Implemented (unit-tested) | `output_schema.allowed_formats`, `selection_status=CONFLICT`, `conflicts` (§5, §6). Wiring a real project adapter to declare the schema is Phase 3 scope |
| Accessibility input | Implemented (unit-tested) | `output_intent.accessibility`, `accessibility_requirements`, accessibility conflicts (§5, §6). Fulfilling/verifying the obligations (generating alt text, captions) is Phase 3 and not implemented |
| Secondary formats, `audience`/`detail_level` | Not implemented | §5–§7 |
| Host/Adapter interface (Phase 3) | Reference implementation (unit-tested with fake renderers) | `format_host.py`: renderer registration, capability declaration, per-stage status record, TEXT fallback. The planner's `render_status` is still `NOT_RUN`; execution results live in the host record |
| DIAGRAM renderer | Implemented (unit-tested) | `diagram_renderer.py`: Mermaid flowchart subset → SVG with `<title>`/`<desc>`; unsupported syntax rejected. Display in real browsers/assistive technology not tested |
| Other renderers (IMAGE, ANIMATION, VIDEO, INTERACTIVE, SIMULATION), functional tests | Not implemented / not run | No usable renderer |
| SARA v3 live round trip | Not verified | The live test `test_live_cothoughts_to_sara_v3_round_trip` (real `SARAv3Connection`) is skipped unless `CO_THOUGHTS_SARA_V3_LIVE=1` and a sibling SARA v3 checkout (`SARA_v3/cli.py`) are both present; `SARA_LLM_*` provider settings are a prerequisite for it to pass, not a skip condition (with the flag and checkout but no provider settings it runs and fails). It has not been run in this work. Other integration tests use a fake adapter (`FakeV24Adapter`). |

Evaluation numbers come from sets written by the same author and are not generalization estimates. Per-commit CI results are tracked in GitHub Actions.

## 13. Development Process and Stabilizing the Rule-Based Approach

### 13.1 Independent review before merge

PRs #12–#17 were merged before the automated review (Codex) finished; the review then found new false positives/misses after merge, each needing a follow-up PR (#12: 2, #13: 3, #14: 1, #15: 5, #16: 3, #17: 1). #18 finished review before merge and fixed its one finding in the same PR. From now on:

1. Merge only after CI passes **and** the automated review has completed.
2. After pushing fixes in response to review, request a fresh review of the latest commit with `@codex review`.
3. Reproduce each finding on the pre-fix code before fixing it, and pin the examples in unit tests.
4. Never tune rules on held-out sets; if a held-out error is fixed by a rule change, record that in the report.

### 13.2 When to stop extending the rules

In PRs #12–#18, review found new counterexamples after every rule change. The rules approximate syntax lexically, so **feature growth of keyword/exception rules stops here**; only defect fixes are accepted.

- No new format vocabulary or new exception categories; only fixes for regressions (defects that break existing behavior).
- Further gains should (a) prefer host-declared `output_intent.requested_format` and context signals, and (b) be decided by comparing the rule-based planner with a learned classifier on an independent evaluation set. While independent evaluation is deferred, (b) cannot be done, so only (a) proceeds.
- Reviewer counterexamples are collected into an adversarial regression set (deferred).

### 13.3 Next steps (priority order)

1. Documentation and status sync (including this section)
2. ~~Independent evaluation~~ — **deferred** (project owner's decision, 2026-11-04). The guidelines (`docs/testing/format_routing_independent_eval_guidelines_v0.1.en.md`) are kept; if resumed, a new annotator starts from scratch. Until then, format-selection numbers are reported only on same-author sets.
3. Output-schema conflict reporting and accessibility input — implemented (§7 priorities 1–2, §11)
4. Host/Adapter interface: renderer protocol, separate records for generation/rendering/functional test/source verification, TEXT fallback on failure — reference implementation (`format_host.py`)
5. Real renderer integration, starting with DIAGRAM, with rendering, accessibility, and functional tests verified separately — DIAGRAM implemented (`diagram_renderer.py`); other formats not connected
6. SARA v3 live round trip in a real provider environment: Co-thoughts → SARA → assessment envelope → downstream backend

An external review (2026-11-04) noted that some SARA v3 gates are WAIVED. That is not verified in this repository. Here, the live round-trip test exists but is opt-in and was skipped, so the live round trip remains unverified.
