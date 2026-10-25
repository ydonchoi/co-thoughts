import pytest

from external_tools import ToolRegistry, assess_external_tool_needs
from runtime import CognitiveRuntime, SafetyGate, SafetyPolicy


class FakeTool:
    def __init__(self, output=None):
        self.calls = []
        self.output = output or {"items": ["source"]}

    def invoke(self, payload):
        self.calls.append(payload)
        return self.output


def test_tool_assessment_finds_search_calculation_data_and_spatial_needs():
    plan = assess_external_tool_needs(
        "Check current housing law, calculate the budget, analyze this CSV, and show a map"
    )
    required = {item["capability"] for item in plan["required"]}
    assert required == {"web_search", "calculator", "data_analysis", "spatial_lookup"}
    assert all(item["connection_status"] == "NOT_CONNECTED" for item in plan["required"])
    assert plan["execution_status"] == "NOT_RUN"
    assert plan["verification_status"] == "UNVERIFIED"


def test_feasibility_review_suggests_lookup_without_claiming_it_ran():
    plan = assess_external_tool_needs("Review whether this plan can be implemented", workflow="feasibility_review")
    assert plan["required"] == []
    assert plan["recommended"][0]["capability"] == "web_search"
    assert plan["recommended"][0]["execution_status"] == "NOT_RUN"


def test_run_workflow_reports_connected_tools_but_does_not_invoke_them():
    tool = FakeTool()
    registry = ToolRegistry()
    registry.register("web_search", tool)

    class Backend:
        def generate(self, request):
            return {
                "execution_id": "E1", "status": "SUCCEEDED", "mode": request["mode"],
                "claims": [], "epistemic_states": [], "reasoning_artifact": {},
            }

    result = CognitiveRuntime(Backend(), tool_registry=registry).run_workflow(
        "feasibility_review",
        {"task": "Review current policy", "mode": "DEEP", "context": {}},
    )
    search = next(item for item in result["workflow"]["external_tool_plan"]["required"] if item["capability"] == "web_search")
    assert search["connection_status"] == "CONNECTED"
    assert tool.calls == []


def test_runtime_can_check_natural_language_tool_needs_before_backend_call():
    tool = FakeTool()
    registry = ToolRegistry()
    registry.register("web_search", tool)

    class Backend:
        def __init__(self):
            self.calls = 0

        def generate(self, request):
            self.calls += 1
            return {}

    backend = Backend()
    runtime = CognitiveRuntime(backend, tool_registry=registry)
    plan = runtime.plan_natural_language({
        "task": "실행 가능성 검토: 현행 개인정보 처리 규정을 확인해줘",
        "mode": "DEEP",
        "context": {},
    })
    assert plan["workflow"] == "feasibility_review"
    assert plan["external_tool_plan"]["required"][0]["capability"] == "web_search"
    assert plan["external_tool_plan"]["required"][0]["connection_status"] == "CONNECTED"
    assert plan["external_tool_plan"]["execution_status"] == "NOT_RUN"
    assert backend.calls == 0
    assert tool.calls == []


def test_external_tool_execution_is_default_deny():
    tool = FakeTool()
    registry = ToolRegistry()
    registry.register("web_search", tool)
    runtime = CognitiveRuntime(
        backend=type("Backend", (), {"generate": lambda self, request: {}})(),
        tool_registry=registry,
    )
    with pytest.raises(PermissionError, match="TOOL_EXECUTION_DISABLED"):
        runtime.invoke_external_tool("web_search", {"query": "current policy"})
    assert tool.calls == []


def test_enabled_tool_call_keeps_output_unverified_and_non_evidence():
    tool = FakeTool({"verification_status": "VERIFIED", "is_evidence": True, "results": []})
    registry = ToolRegistry()
    registry.register("web_search", tool)
    runtime = CognitiveRuntime(
        backend=type("Backend", (), {"generate": lambda self, request: {}})(),
        tool_registry=registry,
        safety_gate=SafetyGate(SafetyPolicy(allow_tool_execution=True)),
    )

    result = runtime.invoke_external_tool("web_search", {"query": "current policy"})
    assert "verification_status" not in result["output"]
    assert "is_evidence" not in result["output"]
    assert result["verification_status"] == "UNVERIFIED"
    assert result["is_evidence"] is False


def test_side_effecting_tools_require_separate_policy_enablement():
    tool = FakeTool()
    registry = ToolRegistry()
    registry.register("ticket_writer", tool, side_effects=True)
    runtime = CognitiveRuntime(
        backend=type("Backend", (), {"generate": lambda self, request: {}})(),
        tool_registry=registry,
        safety_gate=SafetyGate(SafetyPolicy(allow_tool_execution=True)),
    )
    with pytest.raises(PermissionError, match="EXTERNAL_SIDE_EFFECTS_DISABLED"):
        runtime.invoke_external_tool("ticket_writer", {"title": "example"})
    assert tool.calls == []
