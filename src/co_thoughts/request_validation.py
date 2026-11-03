"""Shared input validation for routing requests.

Both ``cognitive_router`` and ``explanation_format_router`` validate the common
request fields with the same rules, so a request accepted by one is never
silently reinterpreted by the other.

Rules:
- ``request`` must be a mapping (``REQUEST_MUST_BE_MAPPING``).
- ``task`` must be a non-blank string; it is not coerced (``TASK_REQUIRED``).
- ``context`` defaults to ``{}`` only when absent or ``None``; any other
  non-mapping value, including falsey ones such as ``[]`` or ``""``, is
  rejected (``CONTEXT_INVALID``).
- ``mode`` defaults to ``MIXED`` only when absent or ``None``; it must otherwise
  be a string naming one of FAST/MIXED/DEEP, case- and whitespace-insensitive
  (``INVALID_MODE``).

Used by the Cognitive Router, the explanation format planner, the runtime
``SafetyGate``, and (for ``request``/``task``/``mode``) the v1.3 reference
executor. The executor has no ``context`` field and keeps ``mode`` required, as
its execution contract demands a selected mode.
"""
from __future__ import annotations

from collections.abc import Mapping
from typing import Any

MODES = frozenset({"FAST", "MIXED", "DEEP"})
DEFAULT_MODE = "MIXED"


def require_mapping(request: Any) -> Mapping[str, Any]:
    """Reject non-mapping requests with ``REQUEST_MUST_BE_MAPPING``."""
    if not isinstance(request, Mapping):
        raise TypeError("REQUEST_MUST_BE_MAPPING")
    return request


def validate_task(request: Mapping[str, Any]) -> str:
    """Return ``request["task"]`` if it is a non-blank string (no coercion)."""
    task = request.get("task")
    if not isinstance(task, str) or not task.strip():
        raise ValueError("TASK_REQUIRED")
    return task


def validate_routing_request(request: Any) -> tuple[str, Mapping[str, Any]]:
    """Return ``(task, context)`` after validating the shared request fields."""
    require_mapping(request)
    task = validate_task(request)

    context = request.get("context")
    if context is None:
        context = {}
    if not isinstance(context, Mapping):
        raise ValueError("CONTEXT_INVALID")

    return task, context


def normalize_mode(value: Any, *, required: bool = False) -> str:
    """Return the canonical mode for ``value``.

    ``None`` means the default (``MIXED``) unless ``required`` is true, in
    which case it is ``INVALID_MODE``. The execution contract requires a
    selected mode, so the reference executor passes ``required=True``.
    """
    if value is None:
        if required:
            raise ValueError("INVALID_MODE")
        return DEFAULT_MODE
    if not isinstance(value, str) or value.strip().upper() not in MODES:
        raise ValueError("INVALID_MODE")
    return value.strip().upper()
