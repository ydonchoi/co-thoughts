import pytest

from explanation_format_router import route_explanation_format


def test_simple_task_defaults_to_text_without_capability_claims():
    result = route_explanation_format({"task": "Define opportunity cost"})
    assert result["format_plan"]["primary"] == "TEXT"
    assert result["format_plan"]["selection_status"] == "SELECTED"
    assert result["capability_status"]["available"] == ["TEXT"]
    assert result["execution_status"] == "NOT_RUN"


def test_static_relationship_selects_diagram_when_host_supports_it():
    result = route_explanation_format({
        "task": "Explain the system architecture diagram",
        "capabilities": {"diagram": True},
    })
    assert result["format_plan"]["primary"] == "DIAGRAM"
    assert result["format_plan"]["selection_status"] == "SELECTED"


def test_unsupported_inferred_format_falls_back_to_text():
    result = route_explanation_format({"task": "Draw an illustration of the concept"})
    assert result["format_plan"]["primary"] == "TEXT"
    assert result["format_plan"]["selection_status"] == "FALLBACK"
    assert result["capability_status"]["unavailable"] == ["IMAGE"]
    assert result["format_plan"]["fallback"] == "TEXT"


def test_explicit_requested_format_takes_priority_when_available():
    result = route_explanation_format({
        "task": "Summarize this paragraph",
        "output_intent": {"requested_format": "DIAGRAM"},
        "capabilities": {"diagram": True},
    })
    assert result["format_plan"]["primary"] == "DIAGRAM"
    assert "user explicitly requested DIAGRAM" in result["format_plan"]["rationale"][0]


def test_explicit_unavailable_request_falls_back_to_text():
    result = route_explanation_format({
        "task": "Summarize this paragraph",
        "output_intent": {"requested_format": "VIDEO"},
        "capabilities": {"video": False},
    })
    assert result["format_plan"]["primary"] == "TEXT"
    assert result["capability_status"]["unavailable"] == ["VIDEO"]


def test_context_signal_can_select_interactive_format():
    result = route_explanation_format({
        "task": "Explore the model",
        "context": {"requires_interaction": True},
        "capabilities": {"interactive": True},
    })
    assert result["format_plan"]["primary"] == "INTERACTIVE"


def test_simulation_requires_explicit_host_capability():
    result = route_explanation_format({
        "task": "Run a simulation of alternative assumptions",
        "capabilities": {"simulation": True},
    })
    assert result["format_plan"]["primary"] == "SIMULATION"


def test_invalid_requested_format_is_rejected():
    with pytest.raises(ValueError, match="REQUESTED_FORMAT_UNSUPPORTED"):
        route_explanation_format({
            "task": "Explain this",
            "output_intent": {"requested_format": "HOLOGRAM"},
        })


def test_invalid_capability_type_is_rejected():
    with pytest.raises(ValueError, match="CAPABILITY_INVALID:diagram"):
        route_explanation_format({
            "task": "Explain a diagram",
            "capabilities": {"diagram": "yes"},
        })


def test_format_selection_never_promotes_verification_or_evidence():
    result = route_explanation_format({
        "task": "Create a flowchart of the process",
        "capabilities": {"diagram": True},
    })
    assert result["verification_status"] == "UNVERIFIED"
    assert result["is_evidence"] is False
    assert result["render_status"] == "NOT_RUN"
    assert result["functional_test_status"] == "NOT_RUN"


def test_non_mapping_context_is_rejected():
    with pytest.raises(ValueError, match="CONTEXT_INVALID"):
        route_explanation_format({"task": "Explain", "context": "not a mapping"})


def test_text_capability_cannot_be_disabled():
    with pytest.raises(ValueError, match="TEXT_CAPABILITY_REQUIRED"):
        route_explanation_format({
            "task": "Explain",
            "capabilities": {"text": False},
        })
