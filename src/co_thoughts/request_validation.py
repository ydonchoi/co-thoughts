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

Used by the Cognitive Router, the explanation format planner, and the runtime
``SafetyGate``.
"""
from __future__ import annotations

from collections.abc import Mapping
from typing import Any

MODES = frozenset({"FAST", "MIXED", "DEEP"})
DEFAULT_MODE = "MIXED"


def validate_routing_request(request: Any) -> tuple[str, Mapping[str, Any]]:
    """Return ``(task, context)`` after validating the shared request fields."""
    if not isinstance(request, Mapping):
        raise TypeError("REQUEST_MUST_BE_MAPPING")

    task = request.get("task")
    if not isinstance(task, str) or not task.strip():
        raise ValueError("TASK_REQUIRED")

    context = request.get("context")
    if context is None:
        context = {}
    if not isinstance(context, Mapping):
        raise ValueError("CONTEXT_INVALID")

    return task, context


def normalize_mode(value: Any) -> str:
    """Return the canonical mode for ``value`` (``None`` means the default)."""
    if value is None:
        return DEFAULT_MODE
    if not isinstance(value, str) or value.strip().upper() not in MODES:
        raise ValueError("INVALID_MODE")
    return value.strip().upper()
