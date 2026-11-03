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
