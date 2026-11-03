import pytest

from cognitive_router import CognitiveRouter, route
from explanation_format_router import route_explanation_format
from request_validation import validate_routing_request


@pytest.mark.parametrize("request_value, exc, code", [
    ("not a mapping", TypeError, "REQUEST_MUST_BE_MAPPING"),
    ({"task": 123}, ValueError, "TASK_REQUIRED"),
    ({"task": "   "}, ValueError, "TASK_REQUIRED"),
    ({}, ValueError, "TASK_REQUIRED"),
    ({"task": "Explain", "context": []}, ValueError, "CONTEXT_INVALID"),
    ({"task": "Explain", "context": ""}, ValueError, "CONTEXT_INVALID"),
    ({"task": "Explain", "context": 0}, ValueError, "CONTEXT_INVALID"),
])
def test_shared_rules_reject_identically_in_both_routers(request_value, exc, code):
    for validator in (
        validate_routing_request,
        route_explanation_format,
        CognitiveRouter().route,
    ):
        with pytest.raises(exc, match=code):
            validator(request_value)


@pytest.mark.parametrize("context", [None, {}])
def test_absent_or_none_context_defaults_to_empty_mapping(context):
    request = {"task": "Explain", "context": context}
    assert validate_routing_request(request) == ("Explain", {})
    assert CognitiveRouter().route(request).operations


def test_missing_context_key_defaults_to_empty_mapping():
    assert validate_routing_request({"task": "Explain"}) == ("Explain", {})


@pytest.mark.parametrize("mode, expected", [
    (None, "MIXED"),
    ("fast", "FAST"),
    (" Deep ", "DEEP"),
])
def test_mode_defaults_and_normalization(mode, expected):
    request = {"task": "Explain", "mode": mode}
    assert CognitiveRouter().route(request).mode == expected


@pytest.mark.parametrize("mode", [1, "TURBO", ""])
def test_invalid_mode_is_rejected(mode):
    with pytest.raises(ValueError, match="INVALID_MODE"):
        CognitiveRouter().route({"task": "Explain", "mode": mode})


def test_public_route_rejects_falsey_context_consistently():
    # Previously cognitive routing accepted context=[] via `or {}` while
    # format routing reported INVALID_INPUT; both now reject it up front.
    with pytest.raises(ValueError, match="CONTEXT_INVALID"):
        route({"task": "Summarize", "mode": "FAST", "context": []})


# --- runtime SafetyGate uses the same rules --------------------------------

from runtime import CognitiveRuntime, SafetyGate, SafetyPolicy  # noqa: E402


class _RecordingBackend:
    def __init__(self):
        self.seen = None

    def generate(self, request):
        self.seen = request
        return {
            "execution_id": "EXEC-V",
            "status": "SUCCEEDED",
            "mode": request["mode"],
            "claims": [],
            "epistemic_states": [],
            "reasoning_artifact": {},
        }


@pytest.mark.parametrize("request_value, exc, code", [
    ("not a mapping", TypeError, "REQUEST_MUST_BE_MAPPING"),
    ({"task": 123}, ValueError, "TASK_REQUIRED"),
    ({"task": "   "}, ValueError, "TASK_REQUIRED"),
    ({"task": "Explain", "context": []}, ValueError, "CONTEXT_INVALID"),
    ({"task": "Explain", "context": ""}, ValueError, "CONTEXT_INVALID"),
    ({"task": "Explain", "mode": 1}, ValueError, "INVALID_MODE"),
    ({"task": "Explain", "mode": "TURBO"}, ValueError, "INVALID_MODE"),
])
def test_safety_gate_rejects_like_the_routers(request_value, exc, code):
    with pytest.raises(exc, match=code):
        SafetyGate().validate_request(request_value)
    with pytest.raises(exc, match=code):
        CognitiveRouter().route(request_value)


@pytest.mark.parametrize("extra, expected_mode", [
    ({}, "MIXED"),
    ({"mode": None, "context": None}, "MIXED"),
    ({"mode": " fast "}, "FAST"),
    ({"mode": "deep"}, "DEEP"),
])
def test_runtime_passes_normalized_request_to_backend(extra, expected_mode):
    backend = _RecordingBackend()
    request = {"request_id": "REQ-V", "task": "Explore", **extra}
    result = CognitiveRuntime(backend).run(request)
    assert backend.seen["mode"] == expected_mode
    assert backend.seen["context"] == {}
    assert result["mode"] == expected_mode
    assert result["verification_status"] == "UNVERIFIED"
    # The caller's mapping is not mutated.
    assert request.get("mode") == extra.get("mode")


def test_safety_gate_size_limits_still_apply():
    gate = SafetyGate(SafetyPolicy(max_task_chars=5, max_context_chars=10))
    with pytest.raises(ValueError, match="TASK_TOO_LARGE"):
        gate.validate_request({"task": "too long task"})
    with pytest.raises(ValueError, match="CONTEXT_TOO_LARGE"):
        gate.validate_request({"task": "ok", "context": {"k": "x" * 50}})
