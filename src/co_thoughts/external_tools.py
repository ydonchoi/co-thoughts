"""Capability planning and explicit adapters for read-only external tools."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Protocol

from cognitive_router import route_verification_domains


class ExternalToolAdapter(Protocol):
    def invoke(self, payload: Mapping[str, Any]) -> Mapping[str, Any]: ...


@dataclass(frozen=True)
class ToolBinding:
    capability: str
    adapter: ExternalToolAdapter
    side_effects: bool = False


class ToolRegistry:
    """Register explicit capability adapters; nothing is connected by default."""

    def __init__(self) -> None:
        self._bindings: dict[str, ToolBinding] = {}

    def register(
        self,
        capability: str,
        adapter: ExternalToolAdapter,
        *,
        side_effects: bool = False,
        replace: bool = False,
    ) -> None:
        if not isinstance(capability, str) or not capability.strip():
            raise ValueError("TOOL_CAPABILITY_INVALID")
        if not callable(getattr(adapter, "invoke", None)):
            raise TypeError("TOOL_ADAPTER_MUST_IMPLEMENT_INVOKE")
        name = capability.strip().casefold()
        if name in self._bindings and not replace:
            raise ValueError("TOOL_CAPABILITY_ALREADY_REGISTERED")
        self._bindings[name] = ToolBinding(name, adapter, bool(side_effects))

    def capabilities(self) -> tuple[str, ...]:
        return tuple(sorted(self._bindings))

    def binding(self, capability: str) -> ToolBinding | None:
        return self._bindings.get(str(capability).casefold())

    def invoke(
        self,
        capability: str,
        payload: Mapping[str, Any],
        *,
        allow_tool_execution: bool,
        allow_external_side_effects: bool,
        max_payload_chars: int,
        max_output_chars: int,
    ) -> dict[str, Any]:
        if not allow_tool_execution:
            raise PermissionError("TOOL_EXECUTION_DISABLED")
        binding = self.binding(capability)
        if binding is None:
            raise LookupError("TOOL_NOT_CONNECTED")
        if binding.side_effects and not allow_external_side_effects:
            raise PermissionError("EXTERNAL_SIDE_EFFECTS_DISABLED")
        if not isinstance(payload, Mapping):
            raise TypeError("TOOL_PAYLOAD_MUST_BE_MAPPING")
        if len(repr(payload)) > max_payload_chars:
            raise ValueError("TOOL_PAYLOAD_TOO_LARGE")

        output = binding.adapter.invoke(payload)
        if not isinstance(output, Mapping):
            raise TypeError("TOOL_OUTPUT_MUST_BE_MAPPING")
        if len(repr(output)) > max_output_chars:
            raise ValueError("TOOL_OUTPUT_TOO_LARGE")
        untrusted_output = dict(output)
        for field in ("verification_status", "is_evidence", "verified", "is_verified"):
            untrusted_output.pop(field, None)
        # Tool output is retained as an observation, never promoted to evidence
        # or a verification result by this adapter layer.
        return {
            "capability": binding.capability,
            "status": "SUCCEEDED",
            "output": untrusted_output,
            "verification_status": "UNVERIFIED",
            "is_evidence": False,
        }


_TOOL_CATALOG: dict[str, str] = {
    "web_search": "Search the web or authoritative sources for current and externally verifiable claims.",
    "calculator": "Compute explicit numerical, budget, rate, or sensitivity calculations.",
    "data_analysis": "Inspect caller-provided datasets and statistical analyses.",
    "spatial_lookup": "Resolve locations, maps, routes, or spatial constraints.",
}

_CURRENT_OR_HIGH_RISK = (
    "current", "currently", "latest", "today", "as of", "citation", "source", "evidence",
    "fact check", "현재", "현행", "최신", "오늘", "근거", "출처", "인용", "사실 확인",
)
_CALCULATION_CUES = (
    "calculate", "calculation", "estimate", "percentage", "budget", "cost", "forecast", "sensitivity",
    "계산", "산출", "추정", "비율", "예산", "비용", "재정", "민감도",
)
_DATA_CUES = (
    "dataset", "data analysis", "statistics", "regression", "csv", "표본", "데이터 분석", "통계", "회귀분석",
)
_SPATIAL_CUES = ("map", "route", "address", "location-specific", "geocode", "지도", "경로", "주소", "위치별", "공간 분석")


def assess_external_tool_needs(
    task: str,
    *,
    workflow: str | None = None,
    connected_capabilities: tuple[str, ...] = (),
) -> dict[str, Any]:
    """Plan tool needs from explicit task signals; never invokes a connector."""
    if not isinstance(task, str) or not task.strip():
        raise ValueError("TASK_REQUIRED")
    normalized = task.casefold()
    domain = route_verification_domains(task)["pre_hypothesis_scan"]
    needed: dict[str, str] = {}

    if (
        domain["temporal_sensitive"]
        or domain["high_risk_tags"]
        or "health" in domain["domains"]
        or any(cue in normalized for cue in _CURRENT_OR_HIGH_RISK)
    ):
        needed["web_search"] = "Current, high-risk, or explicitly evidence-seeking claims need external source lookup."
    if any(cue in normalized for cue in _CALCULATION_CUES):
        needed["calculator"] = "The task contains an explicit numerical or cost-calculation signal."
    if any(cue in normalized for cue in _DATA_CUES):
        needed["data_analysis"] = "The task signals dataset or statistical analysis."
    if any(cue in normalized for cue in _SPATIAL_CUES):
        needed["spatial_lookup"] = "The task asks for location, map, route, or spatial lookup."

    suggested: dict[str, str] = {}
    if workflow == "feasibility_review" and "web_search" not in needed:
        suggested["web_search"] = "Feasibility reviews often depend on external rules or operational facts."
    if workflow == "solution_design" and any(cue in normalized for cue in ("effect", "evidence", "효과", "근거")):
        suggested.setdefault("web_search", "Check external support for predicted solution effects.")

    connected = {name.casefold() for name in connected_capabilities}

    def describe(items: Mapping[str, str]) -> list[dict[str, Any]]:
        return [
            {
                "capability": name,
                "purpose": _TOOL_CATALOG[name],
                "reason": reason,
                "connection_status": "CONNECTED" if name in connected else "NOT_CONNECTED",
                "execution_status": "NOT_RUN",
            }
            for name, reason in items.items()
        ]

    return {
        "required": describe(needed),
        "recommended": describe({name: reason for name, reason in suggested.items() if name not in needed}),
        "execution_status": "NOT_RUN",
        "verification_status": "UNVERIFIED",
    }
