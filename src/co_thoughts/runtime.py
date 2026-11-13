"""Provider-neutral cognitive runtime with a safety and epistemic firewall."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Protocol

from execution import MODES, EPISTEMIC_TYPES
from external_tools import ToolRegistry, assess_external_tool_needs
from sara_integration import SARAConnection, SARAv3Connection, validate_assessment_envelopes
from conversation_verification import ConversationLedger, build_plan, claim_ref, normalize_claims, run_plan
from user_documents import load_user_documents
from workflows import build_workflow_request, route_workflow_natural_language
from request_validation import normalize_mode, validate_routing_request


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

    def validate_request(self, request: Mapping[str, Any]) -> dict[str, Any]:
        """Validate ``request`` and return a normalized copy.

        Shared fields follow ``request_validation``: ``context`` and ``mode``
        default to ``{}`` / ``MIXED`` only when absent or ``None``, and ``mode``
        is case-normalized. The returned copy carries the canonical values so
        backends always see a valid ``mode`` and a mapping ``context``.
        """
        mode = normalize_mode(request.get("mode") if isinstance(request, Mapping) else None)
        task, context = validate_routing_request(request)
        if len(task) > self.policy.max_task_chars:
            raise ValueError("TASK_TOO_LARGE")
        if len(repr(context)) > self.policy.max_context_chars:
            raise ValueError("CONTEXT_TOO_LARGE")

        if request.get("execute_tools") and not self.policy.allow_tool_execution:
            raise PermissionError("TOOL_EXECUTION_DISABLED")
        if request.get("external_side_effects") and not self.policy.allow_external_side_effects:
            raise PermissionError("EXTERNAL_SIDE_EFFECTS_DISABLED")

        envelopes = request.get("sara_assessment_envelopes")
        if envelopes is not None:
            validate_assessment_envelopes(envelopes)
            if len(repr(envelopes)) > self.policy.max_context_chars:
                raise ValueError("SARA_ENVELOPES_TOO_LARGE")

        normalized = dict(request)
        normalized["mode"] = mode
        normalized["context"] = context
        return normalized

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
        sara_v3_connection: SARAv3Connection | None = None,
        conversation_ledger: ConversationLedger | None = None,
    ) -> None:
        self.backend = backend
        self.safety_gate = safety_gate or SafetyGate()
        self.tool_registry = tool_registry or ToolRegistry()
        self.sara_connection = sara_connection or SARAConnection()
        # SARA v3 calls external LLM/search providers. It never runs per turn:
        # turns are recorded locally and sent only by verify_conversation().
        self.sara_v3_connection = sara_v3_connection
        self.conversation_ledger = conversation_ledger or ConversationLedger()

    def run(self, request: Mapping[str, Any]) -> dict[str, Any]:
        if not isinstance(request, Mapping):
            raise TypeError("REQUEST_MUST_BE_MAPPING")

        request = self.safety_gate.validate_request(request)
        # Envelopes from an earlier turn reach the backend as context, but the
        # copies kept here stay authoritative over anything the backend echoes.
        prior_envelopes = validate_assessment_envelopes(request.get("sara_assessment_envelopes", []))
        request_user_claims = normalize_claims(request.get("user_claims"), prefix="UC", error="USER_CLAIMS_INVALID",
                                               allow_sources=True)
        raw = self.backend.generate(request)
        if not isinstance(raw, Mapping):
            raise TypeError("BACKEND_RESPONSE_MUST_BE_MAPPING")

        self.safety_gate.validate_response(raw)
        output = self.safety_gate.sanitize_response(raw)
        if prior_envelopes or "sara_assessment_envelopes" in raw:
            echoed = raw.get("sara_assessment_envelopes", prior_envelopes)
            output["sara_envelope_integrity"] = (
                "PRESERVED" if echoed == prior_envelopes else "BACKEND_MODIFICATION_DISCARDED"
            )
            output["sara_assessment_envelopes"] = prior_envelopes
        output["sara_assessment"] = self.sara_connection.assess_output(output)
        if self.sara_v3_connection is not None:
            output["conversation_verification"] = self._record_turn(request, output, request_user_claims)
        output.setdefault("runtime_revision", self.runtime_revision)
        output.setdefault("request_id", request.get("request_id"))
        return output

    def _record_turn(self, request: Mapping[str, Any], output: Mapping[str, Any],
                     request_user_claims: list[dict[str, str]]) -> dict[str, Any]:
        """Keep this turn for a later, user-requested verification; send nothing now."""
        request_id = str(request.get("request_id") or output.get("request_id") or "").strip()
        conversation_id = str(request.get("conversation_id") or request_id).strip()
        turn_id = str(request.get("turn_id") or request_id).strip()
        if not conversation_id or not turn_id:
            return {"status": "NOT_RECORDED", "reason_code": "TURN_IDENTIFIERS_REQUIRED",
                    "verification_status": "UNVERIFIED"}
        # The host's explicit user claims win; otherwise the backend may extract them.
        # A malformed backend list must not fail the conversation turn itself.
        warnings: list[str] = []
        user_claims = request_user_claims
        if not user_claims:
            try:
                user_claims = normalize_claims(output.get("user_claims"), prefix="UC",
                                               error="BACKEND_USER_CLAIMS_INVALID")
            except ValueError as exc:
                user_claims, warnings = [], [str(exc)]
        assistant_claims = normalize_claims(
            [item for item in output.get("claims", []) if isinstance(item, Mapping)
             and isinstance(item.get("text"), str) and item["text"].strip()],
            prefix="CLAIM", error="CLAIMS_INVALID")
        task = request.get("task")
        response = output.get("response")
        utterances: dict[str, dict[str, Any]] = {}
        if user_claims and isinstance(task, str) and task.strip():
            utterances["USER"] = {"content": task.strip(), "claims": user_claims}
        if assistant_claims:
            body = response.strip() if isinstance(response, str) and response.strip() else "\n".join(
                item["text"] for item in assistant_claims)
            utterances["ASSISTANT"] = {"content": body, "claims": assistant_claims}
        self.conversation_ledger.record(conversation_id, turn_id, utterances)
        recorded = {
            "status": "NOT_REQUESTED", "verification_status": "UNVERIFIED",
            "conversation_id": conversation_id, "turn_id": turn_id,
            "recorded_claim_refs": [claim_ref(turn_id, role, claim["id"])
                                    for role, item in utterances.items() for claim in item["claims"]],
        }
        if warnings:
            recorded["warnings"] = warnings
        return recorded

    def plan_conversation_verification(self, conversation_id: str, *, turn_ids=None, claim_refs=None,
                                       user_documents=None) -> dict[str, Any]:
        """Preview what a verification run would send. Nothing leaves the process.

        ``user_documents`` is ``[{"path", "cites", "claim_refs"?}, ...]``: files the user
        obtained for sources SARA can read only in part. The preview lists each file's
        name, cited URL, digest and size, never its text.
        """
        return self._plan(conversation_id, turn_ids, claim_refs, load_user_documents(user_documents))[0]

    def _plan(self, conversation_id, turn_ids, claim_refs, documents):
        if self.sara_v3_connection is None:
            raise RuntimeError("SARA_V3_NOT_CONFIGURED")
        plan = build_plan(self.conversation_ledger, conversation_id,
                          max_claims_per_call=self.sara_v3_connection.max_claims,
                          turn_ids=turn_ids, claim_refs=claim_refs, documents=documents)
        return plan, documents

    def verify_conversation(self, conversation_id: str, *, confirmation: str, turn_ids=None,
                            claim_refs=None, user_documents=None) -> dict[str, Any]:
        """Run the user-requested verification after the user confirmed the plan.

        ``confirmation`` must equal the ``plan_id`` of a plan built for the same
        selection and documents; a changed conversation, selection or file yields
        a different id.
        """
        plan, documents = self._plan(conversation_id, turn_ids, claim_refs, load_user_documents(user_documents))
        if not isinstance(confirmation, str) or confirmation != plan["plan_id"]:
            raise PermissionError("VERIFICATION_PLAN_NOT_CONFIRMED")
        return run_plan(plan, self.sara_v3_connection, documents)

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
