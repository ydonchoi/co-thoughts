"""Provider-neutral cognitive runtime with a safety and epistemic firewall."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Protocol

from execution import MODES, EPISTEMIC_TYPES


class CognitiveBackend(Protocol):
    def generate(self, request: Mapping[str, Any]) -> Mapping[str, Any]: ...


@dataclass(frozen=True)
class SafetyPolicy:
    max_task_chars: int = 12000
    max_context_chars: int = 50000
    allow_external_side_effects: bool = False
    allow_tool_execution: bool = False


class SafetyGate:
    """Enforce runtime safety and THINK/VERIFY separation."""

    def __init__(self, policy: SafetyPolicy | None = None) -> None:
        self.policy = policy or SafetyPolicy()

    def validate_request(self, request: Mapping[str, Any]) -> None:
        task = request.get("task")
        if not isinstance(task, str) or not task.strip():
            raise ValueError("TASK_REQUIRED")
        if len(task) > self.policy.max_task_chars:
            raise ValueError("TASK_TOO_LARGE")
        if request.get("mode") not in MODES:
            raise ValueError("INVALID_MODE")

        context = request.get("context", {})
        if not isinstance(context, Mapping):
            raise ValueError("CONTEXT_INVALID")
        if len(repr(context)) > self.policy.max_context_chars:
            raise ValueError("CONTEXT_TOO_LARGE")

        if request.get("execute_tools") and not self.policy.allow_tool_execution:
            raise PermissionError("TOOL_EXECUTION_DISABLED")
        if request.get("external_side_effects") and not self.policy.allow_external_side_effects:
            raise PermissionError("EXTERNAL_SIDE_EFFECTS_DISABLED")

    def validate_response(self, response: Mapping[str, Any]) -> None:
        required = (
            "execution_id", "status", "mode", "claims",
            "epistemic_states", "reasoning_artifact",
        )
        for field in required:
            if field not in response:
                raise ValueError(f"RESPONSE_{field.upper()}_REQUIRED")

        if response["status"] not in {"SUCCEEDED", "FAILED", "REJECTED"}:
            raise ValueError("INVALID_STATUS")
        if response["mode"] not in MODES:
            raise ValueError("INVALID_MODE")
        if not isinstance(response["claims"], (list, tuple)):
            raise ValueError("CLAIMS_INVALID")
        if not isinstance(response["epistemic_states"], (list, tuple)):
            raise ValueError("EPISTEMIC_STATES_INVALID")

        for state in response["epistemic_states"]:
            if state not in EPISTEMIC_TYPES:
                raise ValueError("INVALID_EPISTEMIC_TYPE")

        if response.get("verification_status") not in (None, "UNVERIFIED"):
            raise ValueError("COGNITIVE_BACKEND_CANNOT_VERIFY")
        if response.get("is_evidence") not in (None, False):
            raise ValueError("COGNITIVE_BACKEND_CANNOT_PROMOTE_EVIDENCE")

    def sanitize_response(self, response: Mapping[str, Any]) -> dict[str, Any]:
        output = dict(response)
        output["verification_status"] = "UNVERIFIED"
        output["is_evidence"] = False
        output["safety_policy"] = "default-deny"
        return output


class CognitiveRuntime:
    """Run a concrete backend behind the safety/epistemic firewall."""

    runtime_revision = "cognitive-runtime-v0.1"

    def __init__(
        self,
        backend: CognitiveBackend,
        *,
        safety_gate: SafetyGate | None = None,
    ) -> None:
        self.backend = backend
        self.safety_gate = safety_gate or SafetyGate()

    def run(self, request: Mapping[str, Any]) -> dict[str, Any]:
        if not isinstance(request, Mapping):
            raise TypeError("REQUEST_MUST_BE_MAPPING")

        self.safety_gate.validate_request(request)
        raw = self.backend.generate(request)
        if not isinstance(raw, Mapping):
            raise TypeError("BACKEND_RESPONSE_MUST_BE_MAPPING")

        self.safety_gate.validate_response(raw)
        output = self.safety_gate.sanitize_response(raw)
        output.setdefault("runtime_revision", self.runtime_revision)
        output.setdefault("request_id", request.get("request_id"))
        return output
