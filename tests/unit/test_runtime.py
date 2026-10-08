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
