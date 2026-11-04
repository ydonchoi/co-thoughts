"""Host/Adapter layer between a format plan and real renderers (Phase 3).

The format planner (``explanation_format_router``) only *selects* a format.
This module is the host side: it declares which formats can actually be
rendered, applies the project's output schema, calls explicitly registered
renderers, and records each stage separately (design doc §4.3, §8, §9):

- ``generation_status``: was content for the planned format supplied?
- ``render_status``: did the renderer turn it into an artifact?
- ``functional_test_status``: did an interactive/simulation artifact work?
- ``accessibility_status``: were the plan's accessibility obligations met?
- ``source_verification_status``: always ``NOT_RUN`` here; the host does not
  verify sources or claims.

Any failure falls back to the TEXT content, which is always required.
Nothing is connected by default, rendering never verifies anything, and
renderer output cannot raise ``verification_status`` or ``is_evidence``.
"""
from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Protocol

from explanation_format_router import FORMATS, _CAPABILITY_KEYS, _normalize_output_schema

# Formats whose artifact must work, not just display (§8 invariant 5).
_FUNCTIONAL_FORMATS = frozenset({"INTERACTIVE", "SIMULATION"})
_UNTRUSTED_FIELDS = ("verification_status", "is_evidence", "verified", "is_verified")


class FormatRenderer(Protocol):
    """Renders the content for one format into an artifact.

    ``render`` returns a mapping with an ``artifact`` key. A renderer for
    INTERACTIVE or SIMULATION may also define ``functional_test(artifact)``
    returning a mapping with a boolean ``passed``.
    """

    def render(self, payload: Mapping[str, Any]) -> Mapping[str, Any]: ...


class RendererRegistry:
    """Explicit renderer registration; nothing is connected by default."""

    def __init__(self) -> None:
        self._renderers: dict[str, FormatRenderer] = {}

    def register(
        self, format_name: str, renderer: FormatRenderer, *, replace: bool = False
    ) -> None:
        if not isinstance(format_name, str):
            raise ValueError("RENDERER_FORMAT_INVALID")
        name = format_name.strip().upper()
        if name not in FORMATS or name == "TEXT":
            raise ValueError("RENDERER_FORMAT_INVALID")
        if not callable(getattr(renderer, "render", None)):
            raise TypeError("RENDERER_MUST_IMPLEMENT_RENDER")
        if name in self._renderers and not replace:
            raise ValueError("RENDERER_ALREADY_REGISTERED")
        self._renderers[name] = renderer

    def formats(self) -> tuple[str, ...]:
        return tuple(sorted(self._renderers))

    def get(self, format_name: str) -> FormatRenderer | None:
        return self._renderers.get(format_name)


class FormatHost:
    """Project adapter/host for explanation formats.

    ``prepare_request`` makes the host the source of truth for what the
    planner may assume: ``capabilities`` come only from registered renderers
    and ``output_schema`` from the project. ``deliver`` executes a plan.
    """

    def __init__(
        self,
        registry: RendererRegistry | None = None,
        *,
        output_schema: Mapping[str, Any] | None = None,
    ) -> None:
        self._registry = registry if registry is not None else RendererRegistry()
        # Fail at construction, not at the first request, on a bad schema.
        _normalize_output_schema(output_schema)
        self._output_schema = dict(output_schema) if output_schema is not None else None

    def capabilities(self) -> dict[str, bool]:
        """Declare every format: available only if a renderer is registered."""
        registered = set(self._registry.formats())
        return {
            key: (name == "TEXT" or name in registered)
            for name, key in _CAPABILITY_KEYS.items()
        }

    def prepare_request(self, request: Mapping[str, Any]) -> dict[str, Any]:
        """Return a copy of ``request`` with the host's declarations applied.

        Caller-supplied ``capabilities``/``output_schema`` are replaced, so a
        request cannot claim a renderer the host does not have.
        """
        if not isinstance(request, Mapping):
            raise ValueError("REQUEST_MUST_BE_MAPPING")
        prepared = dict(request)
        prepared["capabilities"] = self.capabilities()
        if self._output_schema is None:
            prepared.pop("output_schema", None)
        else:
            prepared["output_schema"] = dict(self._output_schema)
        return prepared

    def deliver(
        self, format_routing: Mapping[str, Any], content: Mapping[str, Any]
    ) -> dict[str, Any]:
        """Execute a format plan and record each stage separately.

        ``content`` must contain ``text`` (the TEXT version, always required
        as the fallback). It may contain ``media`` (``{FORMAT: payload}``),
        ``text_alternative`` and ``captions``.
        """
        plan = _validate_format_routing(format_routing)
        text = _validate_content(content)
        planned = plan["primary"]
        requirements = list(plan.get("accessibility_requirements") or [])

        record = _base_record(plan, text)
        if planned == "TEXT":
            return record

        record["accessibility_status"] = {req: "NOT_MET" for req in requirements}
        media = content.get("media") or {}
        if not isinstance(media, Mapping):
            raise ValueError("CONTENT_MEDIA_INVALID")
        payload = media.get(planned)
        if payload is None:
            record["generation_status"] = "NOT_RUN"
            return _fall_back(record, "MEDIA_CONTENT_MISSING")
        record["generation_status"] = "SUCCEEDED"

        unmet = _check_accessibility(requirements, content)
        for req in requirements:
            record["accessibility_status"][req] = "NOT_MET" if req in unmet else "MET"
        if unmet:
            # §7 priority 1: never deliver media that breaks an accessibility
            # obligation; deliver the TEXT version instead.
            return _fall_back(record, f"ACCESSIBILITY_REQUIREMENT_NOT_MET:{unmet[0]}")

        renderer = self._registry.get(planned)
        if renderer is None:
            return _fall_back(record, "RENDERER_NOT_CONNECTED")

        try:
            output = renderer.render(payload)
        except Exception as exc:  # renderer failures must not escape the host
            record["render_status"] = "FAILED"
            return _fall_back(record, f"RENDER_FAILED:{type(exc).__name__}")
        if not isinstance(output, Mapping) or "artifact" not in output:
            record["render_status"] = "FAILED"
            return _fall_back(record, "RENDER_OUTPUT_INVALID")
        record["render_status"] = "SUCCEEDED"
        artifact = output["artifact"]

        if planned in _FUNCTIONAL_FORMATS:
            test = getattr(renderer, "functional_test", None)
            if not callable(test):
                record["functional_test_status"] = "NOT_RUN"
                return _fall_back(record, "FUNCTIONAL_TEST_UNAVAILABLE")
            try:
                result = test(artifact)
            except Exception as exc:
                record["functional_test_status"] = "FAILED"
                return _fall_back(record, f"FUNCTIONAL_TEST_ERROR:{type(exc).__name__}")
            passed = isinstance(result, Mapping) and result.get("passed") is True
            record["functional_test_status"] = "PASSED" if passed else "FAILED"
            if not passed:
                return _fall_back(record, "FUNCTIONAL_TEST_FAILED")

        record["delivered_format"] = planned
        record["artifact"] = artifact
        record["renderer_metadata"] = {
            key: value for key, value in output.items()
            if key != "artifact" and key not in _UNTRUSTED_FIELDS
        }
        if requirements:
            record["accessibility"] = {
                "text_alternative": content.get("text_alternative"),
                "captions": content.get("captions"),
            }
        return record


def _validate_format_routing(format_routing: Any) -> Mapping[str, Any]:
    if not isinstance(format_routing, Mapping):
        raise ValueError("FORMAT_ROUTING_INVALID")
    plan = format_routing.get("format_plan")
    if not isinstance(plan, Mapping) or plan.get("primary") not in FORMATS:
        raise ValueError("FORMAT_ROUTING_INVALID")
    requirements = plan.get("accessibility_requirements", [])
    if not isinstance(requirements, (list, tuple)):
        raise ValueError("FORMAT_ROUTING_INVALID")
    return plan


def _validate_content(content: Any) -> str:
    if not isinstance(content, Mapping):
        raise ValueError("CONTENT_INVALID")
    text = content.get("text")
    if not isinstance(text, str) or not text.strip():
        raise ValueError("TEXT_CONTENT_REQUIRED")
    return text


def _check_accessibility(requirements: list[str], content: Mapping[str, Any]) -> list[str]:
    unmet = []
    for req in requirements:
        if req == "TEXT_ALTERNATIVE":
            value = content.get("text_alternative")
        elif req == "CAPTIONS":
            value = content.get("captions")
        else:
            # Unknown obligation: the host cannot show it is met.
            value = None
        if not (isinstance(value, str) and value.strip()):
            unmet.append(req)
    return unmet


def _base_record(plan: Mapping[str, Any], text: str) -> dict[str, Any]:
    planned = plan["primary"]
    is_text = planned == "TEXT"
    return {
        "planned_format": planned,
        "selection_status": plan.get("selection_status"),
        "delivered_format": "TEXT",
        "text": text,
        "artifact": None,
        "renderer_metadata": {},
        "accessibility": None,
        "fallback_used": False,
        "fallback_reason": None,
        "generation_status": "NOT_APPLICABLE" if is_text else "NOT_RUN",
        "render_status": "NOT_APPLICABLE" if is_text else "NOT_RUN",
        "functional_test_status": (
            "NOT_RUN" if planned in _FUNCTIONAL_FORMATS else "NOT_APPLICABLE"
        ),
        "accessibility_status": {},
        "source_verification_status": "NOT_RUN",
        "verification_status": "UNVERIFIED",
        "is_evidence": False,
    }


def _fall_back(record: dict[str, Any], reason: str) -> dict[str, Any]:
    record["delivered_format"] = "TEXT"
    record["artifact"] = None
    record["renderer_metadata"] = {}
    record["fallback_used"] = True
    record["fallback_reason"] = reason
    return record
