"""Provider-neutral cognitive runtime with a safety and epistemic firewall."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Protocol

from execution import MODES, EPISTEMIC_TYPES
from external_tools import ToolRegistry, assess_external_tool_needs
from sara_integration import SARAConnection
from workflows import build_workflow_request, route_workflow_natural_language


class CognitiveBackend(Protocol):
    def generate(self, request: Mapping[str, Any]) -> Mapping[str, Any]: ...


@dataclass(frozen=True)
class SafetyPolicy:
    max_task_chars: int = 12000
    max_context_chars: int = 50000
    allow_external_side_effects: bool = False
    allow_tool_execution: bool = False
    max_tool_payload_chars: int = 50000
    max_tool_output_chars: int = 50000


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

    def validate_tool_execution(self, payload: Mapping[str, Any], *, side_effects: bool) -> None:
        if not self.policy.allow_tool_execution:
            raise PermissionError("TOOL_EXECUTION_DISABLED")
        if side_effects and not self.policy.allow_external_side_effects:
            raise PermissionError("EXTERNAL_SIDE_EFFECTS_DISABLED")
        if not isinstance(payload, Mapping):
            raise TypeError("TOOL_PAYLOAD_MUST_BE_MAPPING")
        if len(repr(payload)) > self.policy.max_tool_payload_chars:
            raise ValueError("TOOL_PAYLOAD_TOO_LARGE")

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
        claims = output.get("claims", [])
        if isinstance(claims, (list, tuple)):
            sanitized_claims = []
            for item in claims:
                if not isinstance(item, Mapping):
                    sanitized_claims.append(item)
                    continue
                claim = dict(item)
                claim["verification_status"] = "UNVERIFIED"
                premises = claim.get("premises")
                if isinstance(premises, (list, tuple)):
                    claim["premises"] = [
                        {**dict(premise), "verification_status": "UNVERIFIED"}
                        if isinstance(premise, Mapping) else premise
                        for premise in premises
                    ]
                sanitized_claims.append(claim)
            output["claims"] = sanitized_claims
        premises = output.get("premises")
        if isinstance(premises, (list, tuple)):
            output["premises"] = [
                {**dict(premise), "verification_status": "UNVERIFIED"}
                if isinstance(premise, Mapping) else premise
                for premise in premises
            ]
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
        tool_registry: ToolRegistry | None = None,
        sara_connection: SARAConnection | None = None,
    ) -> None:
        self.backend = backend
        self.safety_gate = safety_gate or SafetyGate()
        self.tool_registry = tool_registry or ToolRegistry()
        self.sara_connection = sara_connection or SARAConnection()

    def run(self, request: Mapping[str, Any]) -> dict[str, Any]:
        if not isinstance(request, Mapping):
            raise TypeError("REQUEST_MUST_BE_MAPPING")

        self.safety_gate.validate_request(request)
        raw = self.backend.generate(request)
        if not isinstance(raw, Mapping):
            raise TypeError("BACKEND_RESPONSE_MUST_BE_MAPPING")

        self.safety_gate.validate_response(raw)
        output = self.safety_gate.sanitize_response(raw)
        output["sara_assessment"] = self.sara_connection.assess_output(output)
        output.setdefault("runtime_revision", self.runtime_revision)
        output.setdefault("request_id", request.get("request_id"))
        return output

    def run_workflow(self, workflow: str, request: Mapping[str, Any]) -> dict[str, Any]:
        """Run exactly one selected workflow cluster in one backend call."""
        workflow_request = build_workflow_request(workflow, request)
        workflow_request["workflow"]["external_tool_plan"] = self.plan_workflow_tools(workflow, request)
        result = self.run(workflow_request)
        # Keep the returned selection authoritative even if a backend echoes
        # different metadata. Workflow selection does not imply verification.
        result["workflow"] = workflow_request["workflow"]
        return result

    def plan_workflow_tools(self, workflow: str, request: Mapping[str, Any]) -> dict[str, Any]:
        """Inspect external-tool requirements and connector availability without running anything."""
        build_workflow_request(workflow, request)  # Validate the workflow name and request shape.
        task = request.get("task", "")
        if not isinstance(task, str) or not task.strip():
            raise ValueError("TASK_REQUIRED")
        return assess_external_tool_needs(
            task,
            workflow=workflow,
            connected_capabilities=self.tool_registry.capabilities(),
        )

    def plan_natural_language(self, request: Mapping[str, Any]) -> dict[str, Any]:
        """Resolve the NL workflow and show tool needs before any backend/tool call."""
        if not isinstance(request, Mapping):
            raise TypeError("REQUEST_MUST_BE_MAPPING")
        routing = route_workflow_natural_language(request.get("task", ""))
        if routing["status"] == "MATCHED":
            routing["external_tool_plan"] = self.plan_workflow_tools(routing["workflow"], request)
        return routing

    def invoke_external_tool(self, capability: str, payload: Mapping[str, Any]) -> dict[str, Any]:
        """Invoke a registered connector under the runtime's explicit safety policy."""
        binding = self.tool_registry.binding(capability)
        side_effects = binding.side_effects if binding else False
        self.safety_gate.validate_tool_execution(payload, side_effects=side_effects)
        return self.tool_registry.invoke(
            capability,
            payload,
            allow_tool_execution=self.safety_gate.policy.allow_tool_execution,
            allow_external_side_effects=self.safety_gate.policy.allow_external_side_effects,
            max_payload_chars=self.safety_gate.policy.max_tool_payload_chars,
            max_output_chars=self.safety_gate.policy.max_tool_output_chars,
        )

    def run_natural_language(self, request: Mapping[str, Any]) -> dict[str, Any]:
        """Route explicit natural-language cues to one workflow, or use run()."""
        if not isinstance(request, Mapping):
            raise TypeError("REQUEST_MUST_BE_MAPPING")
        routing = self.plan_natural_language(request)
        if routing["status"] == "AMBIGUOUS":
            names = ",".join(routing["candidates"])
            raise ValueError(f"WORKFLOW_AMBIGUOUS:{names}")
        if routing["status"] == "MATCHED":
            return self.run_workflow(routing["workflow"], request)
        return self.run(request)
