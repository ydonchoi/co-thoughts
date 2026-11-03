# Tests

Executable regression tests. Unit and integration tests are separated by scope.

## Explanation format routing tests

- `unit/test_explanation_format_router.py`: planner defaults, explicit requests, capability fallback, validation, and epistemic invariants.
- `unit/test_cognitive_format_routing.py`: public route integration and preservation of cognitive/verification outputs.
- `unit/test_request_validation.py`: shared request-field validation applied identically by both routers.
