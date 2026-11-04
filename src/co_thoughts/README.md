# Co-thoughts runtime

Active executable implementation. Keep runtime modules here; add corresponding tests under `tests/`.

## Explanation format planning

- `explanation_format_router.py` provides deterministic, capability-aware presentation planning.
- `cognitive_router.route()` exposes the plan as `format_routing`; invalid format input yields `selection_status=INVALID_INPUT` instead of raising.
- Planning does not generate media, render output, or verify claims.
- `format_host.py` is the Host/Adapter reference layer: `RendererRegistry` (explicit renderers, none by default), `FormatHost.prepare_request()` (capabilities only from registered renderers, project `output_schema`), and `FormatHost.deliver()` (per-stage generation/render/functional-test/accessibility record, TEXT fallback, never verifies or marks evidence). No real renderer is connected.

## Request validation

- `request_validation.py` validates shared routing fields (`request`, `task`, `context`) with one rule set used by `cognitive_router`, `explanation_format_router`, and `runtime.SafetyGate`; `normalize_mode()` gives the shared `mode` rule. `execution.CoThoughtsExecutionRequest` reuses `require_mapping()`, `validate_task()`, and `normalize_mode(required=True)`, keeping `mode` and `request_id` required per the execution contract. The runtime passes the normalized request copy to backends.
