# Co-thoughts runtime

Active executable implementation. Keep runtime modules here; add corresponding tests under `tests/`.

## Explanation format planning

- `explanation_format_router.py` provides deterministic, capability-aware presentation planning.
- `cognitive_router.route()` exposes the plan as `format_routing`.
- Planning does not generate media, render output, or verify claims.
