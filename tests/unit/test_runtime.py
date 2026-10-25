import pytest

from runtime import CognitiveRuntime


class SafeBackend:
    def generate(self, request):
        return {
            "execution_id": "EXEC-1",
            "status": "SUCCEEDED",
            "mode": request["mode"],
            "claims": [{"text": "A hypothesis", "epistemic_type": "HYPOTHESIS"}],
            "epistemic_states": ["HYPOTHESIS"],
            "reasoning_artifact": {"kind": "backend-result"},
        }


class VerificationClaimingBackend:
    def generate(self, request):
        return {
            "execution_id": "EXEC-2",
            "status": "SUCCEEDED",
            "mode": request["mode"],
            "claims": [],
            "epistemic_states": [],
            "reasoning_artifact": {},
            "verification_status": "ESTABLISHED",
        }


class EvidenceClaimingBackend:
    def generate(self, request):
        return {
            "execution_id": "EXEC-3",
            "status": "SUCCEEDED",
            "mode": request["mode"],
            "claims": [],
            "epistemic_states": [],
            "reasoning_artifact": {},
            "is_evidence": True,
        }


def request(**extra):
    value = {
        "request_id": "REQ-1",
        "task": "Explore a hypothesis",
        "mode": "DEEP",
        "context": {},
    }
    value.update(extra)
    return value


def test_runtime_sanitizes_successful_cognitive_output():
    result = CognitiveRuntime(SafeBackend()).run(request())
    assert result["status"] == "SUCCEEDED"
    assert result["verification_status"] == "UNVERIFIED"
    assert result["is_evidence"] is False
    assert result["runtime_revision"] == "cognitive-runtime-v0.1"


def test_run_workflow_calls_backend_once_with_only_selected_cluster():
    class CountingBackend(SafeBackend):
        def __init__(self):
            self.calls = []

        def generate(self, request):
            self.calls.append(request)
            return super().generate(request)

    backend = CountingBackend()
    result = CognitiveRuntime(backend).run_workflow("solution_design", request())

    assert len(backend.calls) == 1
    selected = backend.calls[0]["workflow"]
    assert selected["name"] == "solution_design"
    assert selected["operations"] == ["SYNTHESIZE", "EXAMINE", "COUNTER"]
    assert selected["execution_policy"] == "ON_DEMAND_SINGLE_BACKEND_CALL"
    assert result["workflow"] == selected
    assert result["verification_status"] == "UNVERIFIED"


def test_run_workflow_rejects_unknown_cluster_before_backend_call():
    class CountingBackend(SafeBackend):
        def __init__(self):
            self.calls = 0

        def generate(self, request):
            self.calls += 1
            return super().generate(request)

    backend = CountingBackend()
    try:
        CognitiveRuntime(backend).run_workflow("everything_automatically", request())
    except ValueError as exc:
        assert str(exc) == "WORKFLOW_NOT_FOUND"
    else:
        raise AssertionError("expected invalid workflow rejection")
    assert backend.calls == 0


def test_natural_language_entry_routes_one_cluster_or_falls_back_to_normal_run():
    class CountingBackend(SafeBackend):
        def __init__(self):
            self.calls = []

        def generate(self, request):
            self.calls.append(request)
            return super().generate(request)

    backend = CountingBackend()
    runtime = CognitiveRuntime(backend)
    workflow_result = runtime.run_natural_language(request(task="잠정 해결안을 제안해줘"))
    regular_result = runtime.run_natural_language(request(task="Summarize this paragraph"))

    assert len(backend.calls) == 2
    assert backend.calls[0]["workflow"]["name"] == "solution_design"
    assert "workflow" not in backend.calls[1]
    assert workflow_result["workflow"]["name"] == "solution_design"
    assert regular_result["verification_status"] == "UNVERIFIED"


def test_natural_language_entry_rejects_ambiguous_request_without_calling_backend():
    class CountingBackend(SafeBackend):
        def __init__(self):
            self.calls = 0

        def generate(self, request):
            self.calls += 1
            return super().generate(request)

    backend = CountingBackend()
    with pytest.raises(ValueError, match="WORKFLOW_AMBIGUOUS"):
        CognitiveRuntime(backend).run_natural_language(request(task="문제 진단하고 해결안 설계"))
    assert backend.calls == 0


def test_runtime_rejects_backend_self_verification():
    try:
        CognitiveRuntime(VerificationClaimingBackend()).run(request())
    except ValueError as exc:
        assert str(exc) == "COGNITIVE_BACKEND_CANNOT_VERIFY"
    else:
        raise AssertionError("expected epistemic firewall rejection")


def test_runtime_rejects_backend_evidence_promotion():
    try:
        CognitiveRuntime(EvidenceClaimingBackend()).run(request())
    except ValueError as exc:
        assert str(exc) == "COGNITIVE_BACKEND_CANNOT_PROMOTE_EVIDENCE"
    else:
        raise AssertionError("expected evidence firewall rejection")


def test_runtime_denies_tool_execution_by_default():
    try:
        CognitiveRuntime(SafeBackend()).run(request(execute_tools=True))
    except PermissionError as exc:
        assert str(exc) == "TOOL_EXECUTION_DISABLED"
    else:
        raise AssertionError("expected default-deny tool policy")


def test_runtime_denies_external_side_effects_by_default():
    try:
        CognitiveRuntime(SafeBackend()).run(request(external_side_effects=True))
    except PermissionError as exc:
        assert str(exc) == "EXTERNAL_SIDE_EFFECTS_DISABLED"
    else:
        raise AssertionError("expected default-deny side-effect policy")
