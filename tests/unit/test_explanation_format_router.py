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
        "task": "Show the system architecture diagram",
        "capabilities": {"diagram": True},
    })
    assert result["format_plan"]["primary"] == "DIAGRAM"
    assert result["format_plan"]["selection_status"] == "SELECTED"


def test_unsupported_inferred_format_falls_back_to_text():
    result = route_explanation_format({"task": "Draw an illustration of the concept"})
    assert result["format_plan"]["primary"] == "TEXT"
    assert result["format_plan"]["selection_status"] == "FALLBACK"
    assert result["capability_status"]["unavailable"] == ["IMAGE"]
    assert result["format_plan"]["fallback"] is None
    assert result["format_plan"]["excluded_formats"] == ["IMAGE"]


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


def test_selected_non_text_keeps_text_fallback_and_no_exclusions():
    result = route_explanation_format({
        "task": "Show a diagram",
        "capabilities": {"diagram": True},
    })
    plan = result["format_plan"]
    assert plan["primary"] == "DIAGRAM"
    assert plan["fallback"] == "TEXT"
    assert plan["excluded_formats"] == []
    assert plan["secondary"] == []


@pytest.mark.parametrize("value", ["diagram", " Diagram ", "DIAGRAM"])
def test_requested_format_is_case_and_whitespace_insensitive(value):
    result = route_explanation_format({
        "task": "Summarize",
        "output_intent": {"requested_format": value},
        "capabilities": {"diagram": True},
    })
    assert result["format_plan"]["primary"] == "DIAGRAM"


@pytest.mark.parametrize("signals, expected", [
    ({"simulation_required": True, "requires_interaction": True}, "SIMULATION"),
    ({"requires_interaction": True, "time_dependent_behavior": True}, "INTERACTIVE"),
    ({"time_dependent_behavior": True, "visual_subject": True}, "ANIMATION"),
    ({"visual_subject": True, "process_or_structure": True}, "IMAGE"),
    ({"process_or_structure": True, "has_competing_hypotheses": True}, "DIAGRAM"),
])
def test_context_signal_precedence_is_pinned(signals, expected):
    result = route_explanation_format({"task": "Explain", "context": signals})
    assert result["capability_status"]["requested"] == [expected]


def test_context_signal_overrides_task_keyword():
    result = route_explanation_format({
        "task": "Make a video",
        "context": {"process_or_structure": True},
    })
    assert result["capability_status"]["requested"] == ["DIAGRAM"]


# --- request-cue gating -----------------------------------------------------

@pytest.mark.parametrize("task", [
    "Explain how image compression works in JPEG",
    "What is the simulation hypothesis?",
    "Summarize the plot of the movie Inception",
    "Explain the system architecture diagram",
    "Is the election result a draw?",
    "기업 이미지 관리 전략을 정리해줘",
    "약물 상호작용의 위험성을 설명해줘",
    "영상 압축 코덱의 원리를 설명해줘",
])
def test_format_word_as_topic_stays_text(task):
    result = route_explanation_format({"task": task})
    assert result["capability_status"]["requested"] == ["TEXT"]


@pytest.mark.parametrize("task, expected", [
    ("Show me a picture of the front panel", "IMAGE"),
    ("Make a short video explaining compound interest", "VIDEO"),
    ("Explain recursion as a diagram", "DIAGRAM"),
    ("Draw the water cycle", "IMAGE"),
    ("Can you simulate three growth scenarios?", "SIMULATION"),
    ("I want an animation of a piston", "ANIMATION"),
    ("회원가입 절차를 흐름도로 그려줘", "DIAGRAM"),
    ("심장 박동을 애니메이션으로 보여줘", "ANIMATION"),
    ("변수 조작이 가능한 인터랙티브 설명을 만들어줘", "INTERACTIVE"),
    ("금리 시뮬레이션을 돌려줘", "SIMULATION"),
])
def test_requested_format_wording_selects_format(task, expected):
    result = route_explanation_format({"task": task})
    assert result["capability_status"]["requested"] == [expected]


@pytest.mark.parametrize("task", [
    "This argument draws upon Kant's ethics; explain it",
    "She is drawing on prior research",
    "Give me the bigger picture of the reform",
])
def test_exclusions_cover_inflected_forms(task):
    result = route_explanation_format({"task": task})
    assert result["capability_status"]["requested"] == ["TEXT"]


@pytest.mark.parametrize("task, expected", [
    ("Diagram of the TCP handshake, please", "DIAGRAM"),
    ("A video about photosynthesis", "VIDEO"),
    ("Flowchart for the refund process", "DIAGRAM"),
    ("흐름도 부탁해", "DIAGRAM"),
    ("구조도 필요해", "DIAGRAM"),
])
def test_terse_verbless_requests_still_select_format(task, expected):
    result = route_explanation_format({"task": task})
    assert result["capability_status"]["requested"] == [expected]


@pytest.mark.parametrize("task", [
    # Request verb governs a different verb / clause (Codex review on #12).
    "I need to understand video codecs",
    "We need to discuss image compression in JPEG",
    "Show how video codecs work",
    # "in a <format> <noun>" is a topic noun phrase, not an output form.
    "Explain the rules in a video game",
    "What happens in a video codec?",
])
def test_cue_must_govern_the_format_word(task):
    result = route_explanation_format({"task": task})
    assert result["capability_status"]["requested"] == ["TEXT"]


@pytest.mark.parametrize("task, expected", [
    ("Explain it in a short video", "VIDEO"),
    ("Explain the piston with an animation of the stroke", "ANIMATION"),
    ("I need a video about photosynthesis", "VIDEO"),
])
def test_governing_cues_still_select_format(task, expected):
    result = route_explanation_format({"task": task})
    assert result["capability_status"]["requested"] == [expected]


# --- paraphrased requests ---------------------------------------------------

@pytest.mark.parametrize("task, expected", [
    ("Visualize the request lifecycle", "DIAGRAM"),
    ("Make a chart of quarterly sales", "DIAGRAM"),
    ("Graph y = x squared", "DIAGRAM"),
    ("Show me a photo of a lighthouse", "IMAGE"),
    ("Make a short clip about the proof", "VIDEO"),
    ("Let me tweak the friction and see what happens", "INTERACTIVE"),
    ("Model what happens to demand if prices double", "SIMULATION"),
    ("Show the gears in motion", "ANIMATION"),
    ("매출 추이를 그래프로 보여줘", "DIAGRAM"),
    ("등대 사진을 보여줘", "IMAGE"),
    ("과정을 녹화해서 보여줘", "VIDEO"),
    ("값을 바꿔가며 확인하게 해줘", "INTERACTIVE"),
])
def test_paraphrased_requests_select_format(task, expected):
    result = route_explanation_format({"task": task})
    assert result["capability_status"]["requested"] == [expected]


@pytest.mark.parametrize("task", [
    "What is a bipartite graph?",
    "Explain how stock charts are read",
    "Who owns the copyright of a photo?",
    "Explain the timeline of the Roman Empire's fall",
    "Explain Newton's laws of motion",
    "그래프 이론의 응용 분야를 알려줘",
    "사진 촬영 기법의 역사를 정리해줘",
])
def test_paraphrase_vocabulary_as_topic_stays_text(task):
    result = route_explanation_format({"task": task})
    assert result["capability_status"]["requested"] == ["TEXT"]


# --- Codex review on #13 ----------------------------------------------------

@pytest.mark.parametrize("task", [
    "Graph theory is an important branch of mathematics",
    "Chart of accounts is a ledger structure",
    "힘이 물체를 움직이게 하는 이유를 설명해줘",
])
def test_noun_or_causal_uses_of_paraphrase_words_stay_text(task):
    result = route_explanation_format({"task": task})
    assert result["capability_status"]["requested"] == ["TEXT"]


@pytest.mark.parametrize("task, expected", [
    ("Show me clip art of a lighthouse", "IMAGE"),
    ("Create clip art for an invitation", "IMAGE"),
    ("Make a short clip about the proof", "VIDEO"),
    ("Chart the monthly revenue", "DIAGRAM"),
    ("톱니바퀴가 돌아가는 모습을 움직이게 보여줘", "ANIMATION"),
])
def test_review_fixes_keep_intended_selections(task, expected):
    result = route_explanation_format({"task": task})
    assert result["capability_status"]["requested"] == [expected]


@pytest.mark.parametrize("task", [
    # Codex review on #14: wh-word object clauses are still commands.
    "Chart what is happening to revenue over time",
    "Chart who is buying",
])
def test_verb_keyword_with_wh_object_clause_is_a_command(task):
    result = route_explanation_format({"task": task})
    assert result["capability_status"]["requested"] == ["DIAGRAM"]


# --- self-cued phrases need context ------------------------------------------

@pytest.mark.parametrize("task", [
    "Let me change my password, how do I do it?",
    "Let me play with the idea for a second. Is free will an illusion?",
    "Researchers model what happens inside black holes",
    "I drew boxes and arrows on the whiteboard; summarize the meeting",
    "숫자를 바꿔가며 외우는 방법을 알려줘",
    "조명을 조절하면서 사진 찍는 요령을 알려줘",
])
def test_self_cued_phrases_in_non_request_sense_stay_text(task):
    result = route_explanation_format({"task": task})
    assert result["capability_status"]["requested"] == ["TEXT"]


@pytest.mark.parametrize("task, expected", [
    ("Let me adjust the learning rate and compare the loss curves", "INTERACTIVE"),
    ("Please model what happens if the bridge loses one support", "SIMULATION"),
    ("Show the data pipeline using boxes and arrows", "DIAGRAM"),
    ("반지름을 바꿔가며 넓이가 어떻게 변하는지 보여줘", "INTERACTIVE"),
    ("심장이 뛰는 과정을 움직이는 모습으로 그려줘", "ANIMATION"),
])
def test_self_cued_phrases_in_request_context_select_format(task, expected):
    result = route_explanation_format({"task": task})
    assert result["capability_status"]["requested"] == [expected]


# --- Codex review on #15 ----------------------------------------------------

@pytest.mark.parametrize("task", [
    "He has boxes and arrows on his whiteboard; summarize the meeting",
    "He has a video of the launch; summarize what happened",
    "Explain why researchers need to model what happens to wages when minimum wage rises",
    "식단을 조절하면서 체중 변화를 확인하는 방법을 알려줘",
])
def test_review_15_non_requests_stay_text(task):
    result = route_explanation_format({"task": task})
    assert result["capability_status"]["requested"] == ["TEXT"]


@pytest.mark.parametrize("task, expected", [
    ("Would you be able to model what happens if one lane closes?", "SIMULATION"),
    ("I want you to model what happens if rates rise", "SIMULATION"),
    ("피스톤 동작을 움직이는 모습으로 간단히 보여줘", "ANIMATION"),
    ("온도를 조절하면서 결과를 확인할 수 있게 해주고, 그 원리도 설명해줘", "INTERACTIVE"),
])
def test_review_15_requests_select_format(task, expected):
    result = route_explanation_format({"task": task})
    assert result["capability_status"]["requested"] == [expected]


# --- Codex review on #16 ----------------------------------------------------

@pytest.mark.parametrize("task", [
    "온도를 조절하면서 결과를 확인할 수 있게 해주는 원리를 설명해줘",
    "심장이 뛰는 과정을 움직이는 모습으로 간단히 보여주는 방법을 알려줘",
    # same root cause in the general Korean cue: attributive verb forms
    "흐름도를 그려주는 프로그램을 추천해줘",
    "구조도를 만들어주는 도구가 뭐가 있어?",
    "흐름도로 그려주는 프로그램을 추천해줘",
    "구조도가 필요한 이유를 설명해줘",
])
def test_korean_attributive_verb_forms_are_not_requests(task):
    result = route_explanation_format({"task": task})
    assert result["capability_status"]["requested"] == ["TEXT"]


@pytest.mark.parametrize("task", [
    "I want to model what happens if interest rates double",
    "I need to model what happens if the server fails",
])
def test_first_person_model_requests_select_simulation(task):
    result = route_explanation_format({"task": task})
    assert result["capability_status"]["requested"] == ["SIMULATION"]
