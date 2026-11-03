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


@pytest.mark.parametrize("task", [
    "Give me the big picture of inflation",
    "What are the drawbacks of remote work",
    "Why is a virus considered inanimate?",
    "그림자 금융이란?",
    "영상의학과 진료 범위 설명",
])
def test_keyword_false_positives_stay_text(task):
    result = route_explanation_format({"task": task})
    assert result["capability_status"]["requested"] == ["TEXT"]
    assert result["format_plan"]["selection_status"] == "SELECTED"


@pytest.mark.parametrize("task, expected", [
    ("Show me images of cells", "IMAGE"),
    ("Show the simulated outcomes", "SIMULATION"),
    ("Create flowcharts for onboarding", "DIAGRAM"),
    ("시스템 구조도를 보여줘", "DIAGRAM"),
])
def test_keyword_inflections_and_korean_particles_still_match(task, expected):
    result = route_explanation_format({"task": task})
    assert result["capability_status"]["requested"] == [expected]


def test_invalid_context_signal_is_rejected_even_with_explicit_request():
    with pytest.raises(ValueError, match="CONTEXT_SIGNAL_INVALID:visual_subject"):
        route_explanation_format({
            "task": "Explain",
            "context": {"visual_subject": "yes"},
            "output_intent": {"requested_format": "TEXT"},
        })


def test_unknown_capability_key_is_rejected():
    with pytest.raises(ValueError, match="CAPABILITY_UNKNOWN:Diagram"):
        route_explanation_format({
            "task": "Explain",
            "capabilities": {"Diagram": True},
        })


def test_fallback_uncertainty_distinguishes_declared_false_from_undeclared():
    declared = route_explanation_format({
        "task": "Summarize",
        "output_intent": {"requested_format": "VIDEO"},
        "capabilities": {"video": False},
    })
    undeclared = route_explanation_format({
        "task": "Summarize",
        "output_intent": {"requested_format": "VIDEO"},
        "capabilities": {"diagram": True},
    })
    assert "The host explicitly declared VIDEO unavailable" in declared["format_plan"]["uncertainties"]
    assert "The host did not declare VIDEO capability" in undeclared["format_plan"]["uncertainties"]


def test_explicit_text_request_has_no_fallback():
    result = route_explanation_format({
        "task": "Draw a diagram",
        "output_intent": {"requested_format": "text"},
    })
    assert result["format_plan"]["primary"] == "TEXT"
    assert result["format_plan"]["fallback"] is None


@pytest.mark.parametrize("field, value, error", [
    ("context", [], "CONTEXT_INVALID"),
    ("context", "", "CONTEXT_INVALID"),
    ("output_intent", [], "OUTPUT_INTENT_INVALID"),
    ("output_intent", "", "OUTPUT_INTENT_INVALID"),
])
def test_falsey_non_mapping_fields_are_rejected(field, value, error):
    with pytest.raises(ValueError, match=error):
        route_explanation_format({"task": "Explain", field: value})


def test_draw_a_flowchart_selects_diagram_not_image():
    result = route_explanation_format({
        "task": "Draw a flowchart of the approval process",
        "capabilities": {"diagram": True},
    })
    assert result["format_plan"]["primary"] == "DIAGRAM"
    assert result["format_plan"]["selection_status"] == "SELECTED"


def test_fallback_rationale_matches_declaration_state():
    undeclared = route_explanation_format({"task": "Show an image of the cell"})
    declared_false = route_explanation_format({
        "task": "Show an image of the cell",
        "capabilities": {"image": False},
    })
    assert undeclared["format_plan"]["rationale"][-1] == (
        "IMAGE capability was not declared by the host; using TEXT"
    )
    assert declared_false["format_plan"]["rationale"][-1] == (
        "IMAGE is declared unavailable by the host; using TEXT"
    )
