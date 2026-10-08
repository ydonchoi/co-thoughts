import json

import pytest

from switchable_backend import (
    SwitchableCognitiveBackend,
    UserInputCognitiveBackend,
)


REQUEST = {
    "request_id": "REQ-1",
    "task": "Explore a hypothesis",
    "mode": "DEEP",
    "context": {"x": 1},
}


class Provider:
    def __init__(self):
        self.called = False

    def generate(self, request):
        self.called = True
        return {
            "execution_id": "PROVIDER-1",
            "status": "SUCCEEDED",
            "mode": request["mode"],
            "claims": [],
            "epistemic_states": [],
            "reasoning_artifact": {},
        }


def user_response(prompt):
    assert "do_not_claim_research_verification" in prompt
    return json.dumps({
        "execution_id": "USER-1",
        "status": "SUCCEEDED",
        "mode": "DEEP",
        "claims": [],
        "epistemic_states": [],
        "reasoning_artifact": {"kind": "pasted-llm"},
    })


def test_auto_prefers_external_provider():
    provider = Provider()
    backend = SwitchableCognitiveBackend(
        provider=provider,
        user_input_backend=UserInputCognitiveBackend(user_response),
    )
    result = backend.generate(REQUEST)
    assert provider.called is True
    assert result["execution_id"] == "PROVIDER-1"


def test_auto_falls_back_to_user_input_when_provider_missing():
    backend = SwitchableCognitiveBackend(
        user_input_backend=UserInputCognitiveBackend(user_response),
    )
    result = backend.generate(REQUEST)
    assert result["source"] == "USER_INPUT"
    assert result["provider_id"] == "user-mediated-general-llm"


def test_explicit_modes_are_supported():
    provider = Provider()
    assert SwitchableCognitiveBackend(provider=provider, mode="PROVIDER").generate(REQUEST)["execution_id"] == "PROVIDER-1"
    assert SwitchableCognitiveBackend(
        user_input_backend=UserInputCognitiveBackend(user_response),
        mode="USER_INPUT",
    ).generate(REQUEST)["execution_id"] == "USER-1"


def test_provider_mode_requires_provider():
    with pytest.raises(ValueError, match="PROVIDER_BACKEND_MISSING"):
        SwitchableCognitiveBackend(mode="PROVIDER")


def test_user_input_rejects_non_json():
    backend = UserInputCognitiveBackend(lambda prompt: "not json")
    with pytest.raises(ValueError, match="USER_LLM_RESPONSE_NOT_JSON"):
        backend.generate(REQUEST)
