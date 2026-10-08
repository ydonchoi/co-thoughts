"""Co-thoughts v2.0 cognitive router.

Selects the smallest useful cognitive operation set from task demand.
The router does not verify claims and never promotes cognitive output to evidence.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Mapping

MODES = {"FAST", "MIXED", "DEEP"}
OPERATIONS = {
    "EXPLORE", "DEPTH", "EXAMINE", "COUNTER", "COMPETE",
    "VERIFY", "SYNTHESIZE", "REVISE",
}

@dataclass(frozen=True)
class CognitivePlan:
    mode: str
    operations: tuple[str, ...]
    reasons: tuple[str, ...] = ()
    information_gain_required: bool = True

@dataclass(frozen=True)
class RouterConfig:
    deep_threshold: int = 2
    max_operations: int = 4

class CognitiveRouter:
    """Deterministic first-pass router; semantic ambiguity remains explicit."""

    def __init__(self, config: RouterConfig | None = None):
        self.config = config or RouterConfig()

    def route(self, request: Mapping[str, Any]) -> CognitivePlan:
        mode = str(request.get("mode", "MIXED")).upper()
        if mode not in MODES:
            raise ValueError("INVALID_MODE")

        task = str(request.get("task", "")).strip()
        context = request.get("context") or {}
        if not task:
            raise ValueError("TASK_REQUIRED")
        if not isinstance(context, Mapping):
            raise ValueError("CONTEXT_INVALID")

        text = " ".join([task, repr(context)]).lower()
        ops: list[str] = []
        reasons: list[str] = []

        def add(op: str, reason: str) -> None:
            if op not in ops and len(ops) < self.config.max_operations:
                ops.append(op); reasons.append(reason)

        if mode == "FAST":
            if any(k in text for k in ("verify", "fact check", "citation", "근거", "검증")):
                add("VERIFY", "explicit verification demand")
            else:
                add("SYNTHESIZE", "fast-path direct response")
        else:
            if any(k in text for k in ("explore", "alternatives", "가능성", "탐색", "범위")):
                add("EXPLORE", "breadth demand")
            if any(k in text for k in ("source", "paper", "article", "논문", "책", "보고서", "원문")):
                add("DEPTH", "source-depth demand")
            if any(k in text for k in ("premise", "assumption", "전제", "가정", "소크라테스")):
                add("EXAMINE", "premise examination demand")
            if any(k in text for k in ("counter", "counterargument", "반론", "반례")):
                add("COUNTER", "counterargument demand")
            if any(k in text for k in ("competing", "alternative explanation", "경쟁 설명", "대안 설명")):
                add("COMPETE", "competing explanation demand")
            if any(k in text for k in ("verify", "evidence", "citation", "검증", "근거", "출처")):
                add("VERIFY", "verification demand")

            if not ops:
                add("SYNTHESIZE", "no specialized operation detected")

            if mode == "DEEP" and "REVISE" not in ops and any(
                k in text for k in ("contradict", "new evidence", "수정", "반증", "충돌")
            ):
                add("REVISE", "revision demand")

        if mode == "MIXED" and len(ops) > 2:
            ops = ops[:2]
            reasons = reasons[:2]

        return CognitivePlan(mode, tuple(ops), tuple(reasons))

def route(request: Mapping[str, Any]) -> dict[str, Any]:
    plan = CognitiveRouter().route(request)
    return {
        "mode": plan.mode,
        "operations": list(plan.operations),
        "reasons": list(plan.reasons),
        "information_gain_required": plan.information_gain_required,
        "verification_status": "UNVERIFIED",
        "is_evidence": False,
    }
