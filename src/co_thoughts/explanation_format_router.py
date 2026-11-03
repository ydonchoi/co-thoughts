"""Deterministic, capability-aware explanation-format planning.

This module plans presentation only. It does not generate media, render output,
or verify claims and never changes epistemic or verification status.
"""
from __future__ import annotations

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

_FORMAT_KEYWORDS: dict[str, tuple[str, ...]] = {
    "SIMULATION": (
        "simulation", "simulate", "시뮬레이션", "모의실험", "가정별 결과",
    ),
    "INTERACTIVE": (
        "interactive", "interactivity", "slider", "manipulate variables",
        "대화형", "인터랙티브", "변수 조작", "직접 조작", "상호작용",
    ),
    "ANIMATION": (
        "animation", "animated", "animate", "애니메이션", "움직이는 설명",
        "동작을 움직임으로",
    ),
    "VIDEO": (
        "video", "movie", "영상", "동영상", "설명 영상",
    ),
    "IMAGE": (
        "image", "illustration", "draw", "picture", "이미지", "그림",
        "일러스트", "삽화", "외관을 그려",
    ),
    "DIAGRAM": (
        "diagram", "flowchart", "process flow", "architecture diagram",
        "structure diagram", "도식", "다이어그램", "흐름도", "구조도",
        "관계도", "순서도", "절차도", "개념도",
    ),
}

_CONTEXT_SIGNALS = {
    "simulation_required": "SIMULATION",
    "requires_interaction": "INTERACTIVE",
    "time_dependent_behavior": "ANIMATION",
    "visual_subject": "IMAGE",
    "process_or_structure": "DIAGRAM",
    "has_competing_hypotheses": "DIAGRAM",
}


def _normalize_requested_format(value: Any) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str) or not value.strip():
        raise ValueError("REQUESTED_FORMAT_INVALID")
    normalized = value.strip().upper()
    if normalized not in FORMATS:
        raise ValueError("REQUESTED_FORMAT_UNSUPPORTED")
    return normalized


def _infer_format(task: str, context: Mapping[str, Any]) -> tuple[str, str]:
    normalized = task.casefold()
    # Explicit, typed context signals take precedence over lexical hints.
    for signal, format_name in _CONTEXT_SIGNALS.items():
        value = context.get(signal, False)
        if not isinstance(value, bool):
            raise ValueError(f"CONTEXT_SIGNAL_INVALID:{signal}")
        if value:
            return format_name, f"context signal: {signal}"

    for format_name, keywords in _FORMAT_KEYWORDS.items():
        if any(keyword.casefold() in normalized for keyword in keywords):
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

    context = request.get("context") or {}
    if not isinstance(context, Mapping):
        raise ValueError("CONTEXT_INVALID")

    output_intent = request.get("output_intent") or {}
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

    if candidate in available:
        primary = candidate
        selection_status = "SELECTED"
        fallback = "TEXT" if candidate != "TEXT" else None
        if candidate != "TEXT":
            rationale.append("host capability explicitly declares this format available")
    else:
        primary = "TEXT"
        selection_status = "FALLBACK"
        fallback = "TEXT"
        rationale.append(
            f"{candidate} is unavailable in the declared host capabilities; using TEXT"
        )

    uncertainties = []
    if capabilities is None:
        uncertainties.append(
            "Only TEXT is assumed available because the host supplied no capability map"
        )
    if selection_status == "FALLBACK":
        uncertainties.append(
            "Media generation and rendering capability were not declared by the host"
        )

    return {
        "format_plan": {
            "primary": primary,
            "secondary": [],
            "rationale": rationale,
            "excluded_formats": [],
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
