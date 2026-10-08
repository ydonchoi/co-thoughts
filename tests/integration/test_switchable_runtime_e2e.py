from runtime import CognitiveRuntime
from switchable_backend import SwitchableCognitiveBackend, UserInputCognitiveBackend


def test_auto_falls_back_to_user_input_through_safety_firewall():
    captured = {}

    def user_input(prompt):
        captured["prompt"] = prompt
        return """{"execution_id":"USER-EXEC-1","status":"SUCCEEDED","mode":"DEEP","claims":["test claim"],"epistemic_states":["HYPOTHESIS"],"reasoning_artifact":{"source":"general-llm"}}"""

    backend = SwitchableCognitiveBackend(
        user_input_backend=UserInputCognitiveBackend(user_input),
        mode="AUTO",
    )
    result = CognitiveRuntime(backend).run(
        {
            "request_id": "REQ-USER-1",
            "task": "Assess a hypothesis",
            "mode": "DEEP",
            "context": {"source": "test"},
        }
    )

    assert "co-thoughts-v1.3" in captured["prompt"]
    assert result["execution_id"] == "USER-EXEC-1"
    assert result["status"] == "SUCCEEDED"
    assert result["source"] == "USER_INPUT"
    assert result["verification_status"] == "UNVERIFIED"
    assert result["is_evidence"] is False
    assert result["safety_policy"] == "default-deny"


def test_auto_prefers_provider_over_user_input():
    calls = []

    class Provider:
        def generate(self, request):
            calls.append("provider")
            return {
                "execution_id": "PROVIDER-EXEC-1",
                "status": "SUCCEEDED",
                "mode": request["mode"],
                "claims": [],
                "epistemic_states": ["UNKNOWN"],
                "reasoning_artifact": {},
            }

    def user_input(prompt):
        calls.append("user")
        raise AssertionError("user input fallback must not run")

    backend = SwitchableCognitiveBackend(
        provider=Provider(),
        user_input_backend=UserInputCognitiveBackend(user_input),
        mode="AUTO",
    )
    result = CognitiveRuntime(backend).run(
        {
            "request_id": "REQ-PROVIDER-1",
            "task": "Assess a hypothesis",
            "mode": "FAST",
            "context": {},
        }
    )

    assert calls == ["provider"]
    assert result["execution_id"] == "PROVIDER-EXEC-1"
    assert result["verification_status"] == "UNVERIFIED"
    assert result["is_evidence"] is False
