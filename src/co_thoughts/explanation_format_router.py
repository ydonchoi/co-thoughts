"""Deterministic, capability-aware explanation-format planning.

This module plans presentation only. It does not generate media, render output,
or verify claims and never changes epistemic or verification status.

Plan fields:
- ``fallback``: the format to use if rendering ``primary`` fails; ``None`` when
  ``primary`` is already TEXT.
- ``excluded_formats``: the candidate format that was considered but not
  selected (FALLBACK), otherwise empty.
- ``secondary``: reserved; v0.1 plans a single primary format and returns ``[]``.
"""
from __future__ import annotations

import re
from collections.abc import Mapping
from typing import Any

FORMATS = frozenset({
    "TEXT", "DIAGRAM", "IMAGE", "INTERACTIVE", "ANIMATION", "VIDEO", "SIMULATION",
})
_CAPABILITY_KEYS = {
    "TEXT": "text",
    "DIAGRAM": "diagram",
    "IMAGE": "image",
    "INTERACTIVE": "interactive",
    "ANIMATION": "animation",
    "VIDEO": "video",
    "SIMULATION": "simulation",
}

# Checked in order: DIAGRAM precedes IMAGE so specific wording ("draw a
# flowchart") wins over the generic "draw".
_FORMAT_KEYWORDS: dict[str, tuple[str, ...]] = {
    "SIMULATION": (
        "simulation", "simulate", "simulating", "시뮬레이션", "모의실험", "가정별 결과",
    ),
    "INTERACTIVE": (
        "interactive", "interactivity", "slider", "manipulate variables",
        "대화형", "인터랙티브", "변수 조작", "직접 조작", "상호작용",
    ),
    "ANIMATION": (
        "animation", "animated", "animate", "animating", "애니메이션", "움직이는 설명",
        "동작을 움직임으로",
    ),
    "VIDEO": (
        "video", "movie", "영상", "동영상", "설명 영상",
    ),
    "DIAGRAM": (
        "diagram", "flowchart", "process flow", "architecture diagram",
        "structure diagram", "도식", "다이어그램", "흐름도", "구조도",
        "관계도", "순서도", "절차도", "개념도",
    ),
    "IMAGE": (
        "image", "illustration", "draw", "drawing", "picture", "이미지", "그림",
        "일러스트", "삽화", "외관을 그려",
    ),
}

# Phrases whose substrings collide with format keywords but do not request a
# format (e.g. "big picture", "그림자" = shadow, "영상의학" = radiology).
_KEYWORD_EXCLUSIONS: tuple[str, ...] = (
    "big picture", "bigger picture", "draw conclusions", "draw a conclusion",
    "draw on", "draw upon", "그림자", "영상의학",
)


def _keyword_pattern(keyword: str) -> re.Pattern[str]:
    escaped = re.escape(keyword.casefold())
    if keyword.isascii():
        # ASCII keywords must match whole words ("draw" must not match "drawbacks"),
        # allowing simple plural/past suffixes ("images", "simulated").
        return re.compile(rf"(?<![a-z0-9]){escaped}(?:s|es|d|ed)?(?![a-z0-9])")
    # Korean keywords are matched as substrings so particles (e.g. "도식을") still match.
    return re.compile(escaped)


_FORMAT_PATTERNS: tuple[tuple[str, tuple[re.Pattern[str], ...]], ...] = tuple(
    (format_name, tuple(_keyword_pattern(k) for k in keywords))
    for format_name, keywords in _FORMAT_KEYWORDS.items()
)

# Explicit precedence: the first true signal wins. Richer formats that subsume
# simpler ones come first (a simulation is also interactive; an animation of a
# process is also a diagram). Pinned by tests.
_CONTEXT_SIGNAL_PRECEDENCE: tuple[tuple[str, str], ...] = (
    ("simulation_required", "SIMULATION"),
    ("requires_interaction", "INTERACTIVE"),
    ("time_dependent_behavior", "ANIMATION"),
    ("visual_subject", "IMAGE"),
    ("process_or_structure", "DIAGRAM"),
    ("has_competing_hypotheses", "DIAGRAM"),
)


def _normalize_requested_format(value: Any) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str) or not value.strip():
        raise ValueError("REQUESTED_FORMAT_INVALID")
    normalized = value.strip().upper()
    if normalized not in FORMATS:
        raise ValueError("REQUESTED_FORMAT_UNSUPPORTED")
    return normalized


def _validate_context_signals(context: Mapping[str, Any]) -> None:
    for signal, _ in _CONTEXT_SIGNAL_PRECEDENCE:
        value = context.get(signal, False)
        if not isinstance(value, bool):
            raise ValueError(f"CONTEXT_SIGNAL_INVALID:{signal}")


def _normalize_task_text(task: str) -> str:
    normalized = task.casefold()
    for phrase in _KEYWORD_EXCLUSIONS:
        normalized = normalized.replace(phrase, " ")
    return normalized


def _infer_format(task: str, context: Mapping[str, Any]) -> tuple[str, str]:
    # Explicit, typed context signals take precedence over lexical hints.
    for signal, format_name in _CONTEXT_SIGNAL_PRECEDENCE:
        if context.get(signal, False):
            return format_name, f"context signal: {signal}"

    normalized = _normalize_task_text(task)
    for format_name, patterns in _FORMAT_PATTERNS:
        if any(pattern.search(normalized) for pattern in patterns):
            return format_name, f"task wording indicates {format_name.lower()}"

    return "TEXT", "text is the least-complex sufficient default"


def route_explanation_format(request: Mapping[str, Any]) -> dict[str, Any]:
    """Return a provisional explanation-format plan without generating media.

    Only TEXT is assumed available when the host supplies no capability map.
    Non-text formats require an explicit capability declaration from the host.
    """
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
    _validate_context_signals(context)

    output_intent = request.get("output_intent")
    if output_intent is None:
        output_intent = {}
    if not isinstance(output_intent, Mapping):
        raise ValueError("OUTPUT_INTENT_INVALID")

    requested_format = _normalize_requested_format(
        output_intent.get("requested_format")
    )

    capabilities = request.get("capabilities")
    if capabilities is None:
        normalized_capabilities = {"TEXT": True}
    else:
        if not isinstance(capabilities, Mapping):
            raise ValueError("CAPABILITIES_INVALID")
        unknown = sorted(
            str(key) for key in capabilities if key not in _CAPABILITY_KEYS.values()
        )
        if unknown:
            raise ValueError(f"CAPABILITY_UNKNOWN:{unknown[0]}")
        normalized_capabilities = {"TEXT": True}
        for format_name, key in _CAPABILITY_KEYS.items():
            if key in capabilities:
                value = capabilities[key]
                if not isinstance(value, bool):
                    raise ValueError(f"CAPABILITY_INVALID:{key}")
                normalized_capabilities[format_name] = value

    if normalized_capabilities.get("TEXT") is not True:
        raise ValueError("TEXT_CAPABILITY_REQUIRED")

    if requested_format is not None:
        candidate = requested_format
        rationale = [f"user explicitly requested {candidate}"]
    else:
        candidate, reason = _infer_format(task, context)
        rationale = [reason]

    available = sorted(
        name for name, enabled in normalized_capabilities.items() if enabled
    )
    unavailable = [candidate] if candidate not in available else []

    candidate_declared = (
        capabilities is not None and _CAPABILITY_KEYS[candidate] in capabilities
    )

    if candidate in available:
        primary = candidate
        selection_status = "SELECTED"
        fallback = "TEXT" if candidate != "TEXT" else None
        if candidate != "TEXT":
            rationale.append("host capability explicitly declares this format available")
    else:
        primary = "TEXT"
        selection_status = "FALLBACK"
        # primary is already TEXT; there is nothing further to fall back to.
        fallback = None
        if candidate_declared:
            rationale.append(
                f"{candidate} is declared unavailable by the host; using TEXT"
            )
        else:
            rationale.append(
                f"{candidate} capability was not declared by the host; using TEXT"
            )

    uncertainties = []
    if capabilities is None:
        uncertainties.append(
            "Only TEXT is assumed available because the host supplied no capability map"
        )
    if selection_status == "FALLBACK":
        if candidate_declared:
            uncertainties.append(
                f"The host explicitly declared {candidate} unavailable"
            )
        else:
            uncertainties.append(
                f"The host did not declare {candidate} capability"
            )

    return {
        "format_plan": {
            "primary": primary,
            # Reserved: v0.1 plans a single primary format and never fills this.
            "secondary": [],
            "rationale": rationale,
            "excluded_formats": [] if selection_status == "SELECTED" else [candidate],
            "assumptions": ["Format planning does not generate or render media"],
            "uncertainties": uncertainties,
            "fallback": fallback,
            "selection_status": selection_status,
        },
        "capability_status": {
            "requested": [candidate],
            "available": available,
            "unavailable": unavailable,
        },
        "execution_status": "NOT_RUN",
        "render_status": "NOT_RUN",
        "functional_test_status": "NOT_RUN",
        "verification_status": "UNVERIFIED",
        "is_evidence": False,
    }


def plan_explanation_format_safely(request: Mapping[str, Any]) -> dict[str, Any]:
    """Like ``route_explanation_format`` but never raises on invalid format input.

    Used by ``cognitive_router.route()`` so that malformed format-planning input
    (capabilities, output_intent, context signals) cannot break cognitive or
    verification routing. The failure is reported as ``INVALID_INPUT`` with a
    TEXT plan instead.
    """
    try:
        return route_explanation_format(request)
    except (TypeError, ValueError) as exc:
        return {
            "format_plan": {
                "primary": "TEXT",
                "secondary": [],
                "rationale": ["format planning input was invalid; using TEXT"],
                "excluded_formats": [],
                "assumptions": ["Format planning does not generate or render media"],
                "uncertainties": [
                    "Requested format and host capabilities could not be evaluated"
                ],
                "fallback": None,
                "selection_status": "INVALID_INPUT",
            },
            "capability_status": {
                "requested": [],
                "available": ["TEXT"],
                "unavailable": [],
            },
            "error": str(exc),
            "execution_status": "NOT_RUN",
            "render_status": "NOT_RUN",
            "functional_test_status": "NOT_RUN",
            "verification_status": "UNVERIFIED",
            "is_evidence": False,
        }
