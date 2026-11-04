import pytest

from cognitive_router import route
from explanation_format_router import route_explanation_format
from format_host import FormatHost, RendererRegistry


class FakeRenderer:
    def __init__(self, output=None, error=None):
        self.output = output if output is not None else {"artifact": "<svg/>"}
        self.error = error
        self.calls = []

    def render(self, payload):
        self.calls.append(payload)
        if self.error is not None:
            raise self.error
        return self.output


class FakeInteractiveRenderer(FakeRenderer):
    def __init__(self, passed=True, error=None, **kwargs):
        super().__init__(**kwargs)
        self.passed = passed
        self.test_error = error
        self.error = None

    def functional_test(self, artifact):
        if self.test_error is not None:
            raise self.test_error
        return {"passed": self.passed}


def _host(**renderers):
    registry = RendererRegistry()
    for name, renderer in renderers.items():
        registry.register(name, renderer)
    return FormatHost(registry)


def _plan(host, request):
    return route_explanation_format(host.prepare_request(request))


TEXT = {"text": "Plain explanation."}


# --- Registry and host declarations ---

def test_nothing_is_connected_by_default():
    host = FormatHost()
    caps = host.capabilities()
    assert caps["text"] is True
    assert not any(value for key, value in caps.items() if key != "text")


def test_capabilities_come_only_from_registered_renderers():
    host = _host(DIAGRAM=FakeRenderer())
    prepared = host.prepare_request({
        "task": "Explain",
        "capabilities": {"video": True},          # caller cannot claim this
        "output_schema": {"allowed_formats": ["TEXT", "VIDEO"]},
    })
    assert prepared["capabilities"]["diagram"] is True
    assert prepared["capabilities"]["video"] is False
    assert "output_schema" not in prepared


def test_host_output_schema_replaces_caller_schema():
    host = FormatHost(output_schema={"allowed_formats": ["TEXT"]})
    prepared = host.prepare_request({
        "task": "Explain", "output_schema": {"allowed_formats": ["TEXT", "VIDEO"]},
    })
    assert prepared["output_schema"] == {"allowed_formats": ["TEXT"]}


@pytest.mark.parametrize("name", ["TEXT", "HOLOGRAM", "", 3])
def test_registry_rejects_invalid_formats(name):
    with pytest.raises(ValueError, match="RENDERER_FORMAT_INVALID"):
        RendererRegistry().register(name, FakeRenderer())


def test_registry_requires_render_and_rejects_duplicates():
    registry = RendererRegistry()
    with pytest.raises(TypeError, match="RENDERER_MUST_IMPLEMENT_RENDER"):
        registry.register("DIAGRAM", object())
    registry.register("diagram", FakeRenderer())
    with pytest.raises(ValueError, match="RENDERER_ALREADY_REGISTERED"):
        registry.register("DIAGRAM", FakeRenderer())
    registry.register("DIAGRAM", FakeRenderer(), replace=True)
    assert registry.formats() == ("DIAGRAM",)


# --- Delivery ---

def test_text_plan_delivers_text_without_rendering():
    host = _host(DIAGRAM=FakeRenderer())
    record = host.deliver(_plan(host, {"task": "Define entropy"}), TEXT)
    assert record["planned_format"] == "TEXT"
    assert record["delivered_format"] == "TEXT"
    assert record["generation_status"] == "NOT_APPLICABLE"
    assert record["render_status"] == "NOT_APPLICABLE"
    assert record["fallback_used"] is False


def test_diagram_renders_and_records_stages_separately():
    renderer = FakeRenderer(output={"artifact": "<svg/>", "engine": "fake", "verification_status": "VERIFIED"})
    host = _host(DIAGRAM=renderer)
    plan = _plan(host, {"task": "Draw a flowchart of the approval process"})
    record = host.deliver(plan, {"text": "Steps...", "media": {"DIAGRAM": "graph TD; A-->B"}})
    assert renderer.calls == ["graph TD; A-->B"]
    assert record["delivered_format"] == "DIAGRAM"
    assert record["artifact"] == "<svg/>"
    assert record["generation_status"] == "SUCCEEDED"
    assert record["render_status"] == "SUCCEEDED"
    assert record["functional_test_status"] == "NOT_APPLICABLE"
    assert record["source_verification_status"] == "NOT_RUN"
    # Rendering never verifies anything, whatever the renderer claims.
    assert record["verification_status"] == "UNVERIFIED"
    assert record["is_evidence"] is False
    assert record["renderer_metadata"] == {"engine": "fake"}
    assert record["text"] == "Steps..."


def test_missing_media_content_falls_back_to_text():
    renderer = FakeRenderer()
    host = _host(DIAGRAM=renderer)
    record = host.deliver(_plan(host, {"task": "Draw a flowchart"}), TEXT)
    assert record["delivered_format"] == "TEXT"
    assert record["generation_status"] == "NOT_RUN"
    assert record["render_status"] == "NOT_RUN"
    assert record["fallback_reason"] == "MEDIA_CONTENT_MISSING"
    assert renderer.calls == []


def test_render_exception_is_recorded_and_falls_back():
    host = _host(DIAGRAM=FakeRenderer(error=RuntimeError("boom")))
    record = host.deliver(
        _plan(host, {"task": "Draw a flowchart"}),
        {"text": "Steps...", "media": {"DIAGRAM": "graph"}},
    )
    assert record["render_status"] == "FAILED"
    assert record["fallback_reason"] == "RENDER_FAILED:RuntimeError"
    assert record["delivered_format"] == "TEXT"
    assert record["artifact"] is None
    assert record["planned_format"] == "DIAGRAM"   # selection is preserved


@pytest.mark.parametrize("output", [["<svg/>"], {"svg": "<svg/>"}])
def test_invalid_render_output_falls_back(output):
    host = _host(DIAGRAM=FakeRenderer(output=output))
    record = host.deliver(
        _plan(host, {"task": "Draw a flowchart"}),
        {"text": "Steps...", "media": {"DIAGRAM": "graph"}},
    )
    assert record["render_status"] == "FAILED"
    assert record["fallback_reason"] == "RENDER_OUTPUT_INVALID"


def test_plan_for_unconnected_renderer_falls_back():
    # A plan made elsewhere (caller-declared capability) still cannot render.
    plan = route_explanation_format({
        "task": "Explain", "output_intent": {"requested_format": "VIDEO"},
        "capabilities": {"video": True},
    })
    record = FormatHost().deliver(plan, {"text": "T", "media": {"VIDEO": "script"}})
    assert record["fallback_reason"] == "RENDERER_NOT_CONNECTED"
    assert record["delivered_format"] == "TEXT"


def test_interactive_requires_passing_functional_test():
    ok = _host(INTERACTIVE=FakeInteractiveRenderer(passed=True))
    request = {"task": "Explain", "output_intent": {"requested_format": "INTERACTIVE"}}
    content = {"text": "T", "media": {"INTERACTIVE": {"widget": 1}}}
    record = ok.deliver(_plan(ok, request), content)
    assert record["functional_test_status"] == "PASSED"
    assert record["delivered_format"] == "INTERACTIVE"

    failing = _host(INTERACTIVE=FakeInteractiveRenderer(passed=False))
    record = failing.deliver(_plan(failing, request), content)
    assert record["render_status"] == "SUCCEEDED"
    assert record["functional_test_status"] == "FAILED"
    assert record["fallback_reason"] == "FUNCTIONAL_TEST_FAILED"
    assert record["delivered_format"] == "TEXT"

    erroring = _host(INTERACTIVE=FakeInteractiveRenderer(error=ValueError("x")))
    record = erroring.deliver(_plan(erroring, request), content)
    assert record["functional_test_status"] == "FAILED"
    assert record["fallback_reason"] == "FUNCTIONAL_TEST_ERROR:ValueError"


def test_interactive_without_functional_test_is_not_delivered():
    host = _host(SIMULATION=FakeRenderer())
    record = host.deliver(
        _plan(host, {"task": "Explain", "output_intent": {"requested_format": "SIMULATION"}}),
        {"text": "T", "media": {"SIMULATION": {"model": 1}}},
    )
    assert record["render_status"] == "SUCCEEDED"
    assert record["functional_test_status"] == "NOT_RUN"
    assert record["fallback_reason"] == "FUNCTIONAL_TEST_UNAVAILABLE"
    assert record["delivered_format"] == "TEXT"


# --- Accessibility obligations ---

def test_text_alternative_obligation_met():
    host = _host(DIAGRAM=FakeRenderer())
    plan = _plan(host, {
        "task": "Draw a flowchart",
        "output_intent": {"accessibility": {"screen_reader": True}},
    })
    record = host.deliver(plan, {
        "text": "T", "media": {"DIAGRAM": "g"}, "text_alternative": "A flowchart with two steps.",
    })
    assert record["accessibility_status"] == {"TEXT_ALTERNATIVE": "MET"}
    assert record["delivered_format"] == "DIAGRAM"
    assert record["accessibility"]["text_alternative"] == "A flowchart with two steps."


def test_unmet_obligation_blocks_media_before_rendering():
    renderer = FakeRenderer()
    host = _host(VIDEO=renderer)
    plan = _plan(host, {
        "task": "Explain",
        "output_intent": {"requested_format": "VIDEO", "accessibility": {"captions": True}},
    })
    record = host.deliver(plan, {"text": "T", "media": {"VIDEO": "clip"}, "captions": "  "})
    assert record["accessibility_status"] == {"CAPTIONS": "NOT_MET"}
    assert record["fallback_reason"] == "ACCESSIBILITY_REQUIREMENT_NOT_MET:CAPTIONS"
    assert record["render_status"] == "NOT_RUN"
    assert renderer.calls == []


# --- Input validation and integration ---

@pytest.mark.parametrize("routing", [None, {}, {"format_plan": {"primary": "HOLOGRAM"}},
                                     {"format_plan": {"primary": "TEXT", "accessibility_requirements": "x"}},
                                     {"format_plan": {"primary": []}},
                                     {"format_plan": {"primary": "DIAGRAM", "accessibility_requirements": [{}]}}])
def test_invalid_format_routing_is_rejected(routing):
    with pytest.raises(ValueError, match="FORMAT_ROUTING_INVALID"):
        FormatHost().deliver(routing, TEXT)


@pytest.mark.parametrize("content, error", [
    (None, "CONTENT_INVALID"),
    ({}, "TEXT_CONTENT_REQUIRED"),
    ({"text": " "}, "TEXT_CONTENT_REQUIRED"),
])
def test_text_content_is_always_required(content, error):
    with pytest.raises(ValueError, match=error):
        FormatHost().deliver({"format_plan": {"primary": "TEXT"}}, content)


def test_media_must_be_a_mapping():
    host = _host(DIAGRAM=FakeRenderer())
    with pytest.raises(ValueError, match="CONTENT_MEDIA_INVALID"):
        host.deliver(_plan(host, {"task": "Draw a flowchart"}), {"text": "T", "media": ["g"]})


def test_host_with_cognitive_router_end_to_end():
    host = _host(DIAGRAM=FakeRenderer())
    routed = route(host.prepare_request({"task": "Draw a flowchart of the approval process"}))
    record = host.deliver(routed["format_routing"], {"text": "T", "media": {"DIAGRAM": "g"}})
    assert record["delivered_format"] == "DIAGRAM"
    assert routed["format_routing"]["format_plan"]["primary"] == "DIAGRAM"


def test_deliver_does_not_mutate_the_plan():
    host = _host(DIAGRAM=FakeRenderer(error=RuntimeError()))
    plan = _plan(host, {"task": "Draw a flowchart"})
    before = repr(plan)
    host.deliver(plan, {"text": "T", "media": {"DIAGRAM": "g"}})
    assert repr(plan) == before


def test_invalid_host_output_schema_fails_at_construction():
    with pytest.raises(ValueError, match="OUTPUT_SCHEMA_TEXT_REQUIRED"):
        FormatHost(output_schema={"allowed_formats": ["DIAGRAM"]})


# --- Review follow-ups (PR #27) ---

def test_null_artifact_is_invalid_render_output():
    host = _host(DIAGRAM=FakeRenderer(output={"artifact": None}))
    record = host.deliver(
        _plan(host, {"task": "Draw a flowchart"}),
        {"text": "T", "media": {"DIAGRAM": "g"}},
    )
    assert record["render_status"] == "FAILED"
    assert record["fallback_reason"] == "RENDER_OUTPUT_INVALID"
    assert record["delivered_format"] == "TEXT"


def test_host_schema_is_snapshotted():
    schema = {"allowed_formats": ["TEXT"]}
    registry = RendererRegistry()
    registry.register("DIAGRAM", FakeRenderer())
    host = FormatHost(registry, output_schema=schema)
    schema["allowed_formats"].append("DIAGRAM")              # caller mutates config
    prepared = host.prepare_request({"task": "x"})
    prepared["output_schema"]["allowed_formats"].append("DIAGRAM")  # or a prepared copy
    assert host.prepare_request({"task": "x"})["output_schema"] == {"allowed_formats": ["TEXT"]}


def test_deliver_enforces_host_schema_on_outside_plans():
    registry = RendererRegistry()
    renderer = FakeRenderer()
    registry.register("DIAGRAM", renderer)
    host = FormatHost(registry, output_schema={"allowed_formats": ["TEXT"]})
    outside_plan = route_explanation_format({
        "task": "Draw a flowchart", "capabilities": {"diagram": True},
    })
    record = host.deliver(outside_plan, {"text": "T", "media": {"DIAGRAM": "g"}})
    assert record["delivered_format"] == "TEXT"
    assert record["fallback_reason"] == "FORMAT_NOT_IN_OUTPUT_SCHEMA"
    assert renderer.calls == []


@pytest.mark.parametrize("schema, content, reason", [
    ({"allowed_formats": ["TEXT"]}, {"text": "T", "media": {"DIAGRAM": "g"}, "text_alternative": "alt"},
     "FORMAT_NOT_IN_OUTPUT_SCHEMA"),
    (None, {"text": "T", "text_alternative": "alt"}, "MEDIA_CONTENT_MISSING"),
])
def test_accessibility_status_is_evaluated_on_early_fallbacks(schema, content, reason):
    registry = RendererRegistry()
    registry.register("DIAGRAM", FakeRenderer())
    host = FormatHost(registry, output_schema=schema)
    plan = {"format_plan": {"primary": "DIAGRAM", "accessibility_requirements": ["TEXT_ALTERNATIVE"]}}
    record = host.deliver(plan, content)
    assert record["fallback_reason"] == reason
    assert record["accessibility_status"] == {"TEXT_ALTERNATIVE": "MET"}
