"""On-demand, single-call cognitive workflow clusters."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping


@dataclass(frozen=True)
class WorkflowDefinition:
    name: str
    purpose: str
    stages: tuple[str, ...]
    operations: tuple[str, ...]


_WORKFLOWS: dict[str, WorkflowDefinition] = {
    "problem_diagnosis": WorkflowDefinition(
        name="problem_diagnosis",
        purpose="Clarify the problem, competing causes, stakeholder frames, and important assumptions.",
        stages=("problem_framing", "competing_cause_hypotheses", "stakeholder_frames", "fact_value_inference_separation"),
        operations=("EXPLORE", "EXAMINE", "COMPETE"),
    ),
    "solution_design": WorkflowDefinition(
        name="solution_design",
        purpose="Produce a concrete provisional solution and compare it with alternatives and failure paths.",
        stages=("provisional_solution", "alternative_comparison", "assumptions_and_failure_paths"),
        operations=("SYNTHESIZE", "EXAMINE", "COUNTER"),
    ),
    "feasibility_review": WorkflowDefinition(
        name="feasibility_review",
        purpose="Review constraints, consequences, risks, and measures for a proposed solution.",
        stages=("authority_resources_operations", "consequences_and_risk_transfer", "evaluation_measures"),
        operations=("EXAMINE", "VERIFY", "COUNTER"),
    ),
    "hypothesis_delta": WorkflowDefinition(
        name="hypothesis_delta",
        purpose="Compare user and AI hypotheses, identify unique variables, and revise the working view.",
        stages=("compare_hypotheses", "surface_unique_variables", "evaluate_support_symmetrically", "revise_or_checkpoint"),
        operations=("COMPETE", "COUNTER", "REVISE"),
    ),
}

_NATURAL_LANGUAGE_TRIGGERS: dict[str, tuple[str, ...]] = {
    "problem_diagnosis": (
        "문제 진단", "문제를 구조화", "문제 프레이밍", "원인 가설을 정리", "원인을 분석해줘",
        "diagnose the problem", "problem diagnosis", "frame the problem", "root cause analysis",
    ),
    "solution_design": (
        "해결안 설계", "해결책을 제안", "해결 방안을 제안", "잠정 해결안", "대안을 설계",
        "design a solution", "propose a solution", "solution design", "recommend a solution",
    ),
    "feasibility_review": (
        "실행 가능성 검토", "실행 가능성을 검토", "실현 가능성 검토", "위험과 부작용 검토",
        "feasibility review", "assess feasibility", "evaluate feasibility", "assess risks and side effects",
    ),
    "hypothesis_delta": (
        "가설 비교", "내 가설과 비교", "가설 차이", "누락 변수 찾기", "human-ai hypothesis delta",
        "compare hypotheses", "compare my hypothesis", "find missing variables",
    ),
}


def list_workflows() -> tuple[WorkflowDefinition, ...]:
    """Return the available workflow clusters in stable order."""
    return tuple(_WORKFLOWS.values())


def route_workflow_natural_language(task: str) -> dict[str, Any]:
    """Resolve explicit Korean or English workflow phrases without execution."""
    if not isinstance(task, str) or not task.strip():
        raise ValueError("TASK_REQUIRED")
    normalized = task.casefold()
    candidates = [
        name for name, phrases in _NATURAL_LANGUAGE_TRIGGERS.items()
        if any(phrase.casefold() in normalized for phrase in phrases)
    ]
    return {
        "status": "NO_MATCH" if not candidates else "MATCHED" if len(candidates) == 1 else "AMBIGUOUS",
        "workflow": candidates[0] if len(candidates) == 1 else None,
        "candidates": candidates,
        "execution": "NOT_RUN",
    }


def build_workflow_request(name: str, request: Mapping[str, Any]) -> dict[str, Any]:
    """Attach one explicitly selected workflow to a normal runtime request."""
    if name not in _WORKFLOWS:
        raise ValueError("WORKFLOW_NOT_FOUND")
    if not isinstance(request, Mapping):
        raise TypeError("REQUEST_MUST_BE_MAPPING")

    definition = _WORKFLOWS[name]
    result = dict(request)
    result["workflow"] = {
        "name": definition.name,
        "purpose": definition.purpose,
        "stages": list(definition.stages),
        "operations": list(definition.operations),
        "execution_policy": "ON_DEMAND_SINGLE_BACKEND_CALL",
        "verification_status": "UNVERIFIED",
        "external_tool_execution": "EXPLICIT_CALL_ONLY",
    }
    return result
