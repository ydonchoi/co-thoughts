# Co-thoughts runtime

Active executable implementation. Keep runtime modules here; add corresponding tests under `tests/`.

## Explanation format planning

- `explanation_format_router.py` provides deterministic, capability-aware presentation planning.
- `cognitive_router.route()` exposes the plan as `format_routing`; invalid format input yields `selection_status=INVALID_INPUT` instead of raising.
- Planning does not generate media, render output, or verify claims.
