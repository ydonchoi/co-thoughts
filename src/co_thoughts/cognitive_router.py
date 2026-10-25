"""Co-thoughts v2.0 cognitive router.

Selects the smallest useful cognitive operation set from task demand.
The router does not verify claims and never promotes cognitive output to evidence.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Mapping
from workflows import route_workflow_natural_language

MODES = {"FAST", "MIXED", "DEEP"}
OPERATIONS = {
    "EXPLORE", "DEPTH", "EXAMINE", "COUNTER", "COMPETE",
    "VERIFY", "SYNTHESIZE", "REVISE",
}

# Heuristic routing hints only. These labels identify likely verification needs;
# they do not extract claims, select evidence, or perform verification.
_DOMAIN_KEYWORDS: dict[str, tuple[str, ...]] = {
    "natural_sciences": ("science", "scientific", "physics", "chemistry", "biology", "climate", "과학", "물리", "화학", "생명과학", "기후"),
    "health": ("health", "medical", "medicine", "clinical", "disease", "treatment", "건강", "의학", "의료", "질병", "치료", "임상"),
    "engineering_technology": ("engineering", "software", "technology", "system design", "technical", "공학", "소프트웨어", "기술", "시스템 설계"),
    "statistics_data": ("statistics", "statistical", "dataset", "data analysis", "sample size", "통계", "표본", "데이터", "자료 분석"),
    "social_sciences": ("social science", "psychology", "sociology", "education", "behavior", "사회과학", "심리", "사회학", "교육", "행동"),
    "economics_finance_operations": ("economic", "economics", "budget", "finance", "cost", "funding", "operations", "예산", "재정", "금융", "비용", "재원", "운영", "경제"),
    "law_regulation": ("legal", "law", "regulation", "jurisdiction", "authority", "liability", "법률", "법적", "법", "규정", "규제", "관할", "권한", "책임"),
    "public_policy": ("public policy", "policy", "government", "public administration", "정책", "행정", "공공", "정부"),
    "humanities_history_culture": ("history", "historical", "language", "culture", "textual", "역사", "언어", "문화", "문헌", "원문"),
    "ethics_normative": ("ethics", "ethical", "justice", "fairness", "rights", "윤리", "정의", "공정성", "권리", "정당성"),
    "spatial_housing_urban": ("spatial", "urban", "housing", "zoning", "land use", "neighborhood", "accessibility", "도시", "주거", "공간", "토지", "용도지역", "근린", "접근성"),
}

_HIGH_RISK_KEYWORDS: dict[str, tuple[str, ...]] = {
    "law_regulation": _DOMAIN_KEYWORDS["law_regulation"],
    "health_safety": ("safety", "harm", "risk to life", "안전", "위해", "생명 위험", "사고"),
    "privacy": ("privacy", "personal data", "personal information", "개인정보", "프라이버시"),
    "rights": ("rights", "human rights", "권리", "인권"),
}

_TEMPORAL_KEYWORDS = (
    "current", "currently", "latest", "as of", "today", "this year", "price", "rate", "law", "regulation",
    "현재", "현행", "최신", "오늘", "올해", "가격", "요금", "법령", "규정", "통계",
)

_EVIDENCE_STRATEGIES: dict[str, str] = {
    "natural_sciences": "Match primary studies and authoritative public scientific sources to the claim type.",
    "health": "Prefer clinical guidance, systematic reviews, primary studies, and public health authorities appropriate to the claim.",
    "engineering_technology": "Check technical specifications, standards, reproducible measurements, and implementation evidence.",
    "statistics_data": "Check source data, definitions, sampling, measurement, methods, uncertainty, and reproducibility.",
    "social_sciences": "Check study design, population, context, alternative explanations, and external validity.",
    "economics_finance_operations": "Check assumptions, cost and funding sources, recurring and opportunity costs, and sensitivity.",
    "law_regulation": "Check jurisdiction and date against current primary law and authoritative interpretation.",
    "public_policy": "Check official policy materials and evaluate implementation evidence, outcomes, and context.",
    "humanities_history_culture": "Check original texts, editions, historical context, and source provenance.",
    "ethics_normative": "State normative premises and criteria; verify empirical premises separately.",
    "spatial_housing_urban": "Separate spatial conditions, applicable rules, observed conditions, and design assumptions.",
}


def route_verification_domains(
    task: str,
    proposed_solution: str | None = None,
    claims: list[Mapping[str, Any]] | None = None,
) -> dict[str, Any]:
    """Return deterministic domain-routing hints without claiming verification.

    ``claims`` is optional caller-supplied claim material. The router does not
    infer or validate claims from prose. Supplying a proposed solution enables
    a post-solution scan so newly introduced domains can be surfaced.
    """
    if not isinstance(task, str) or not task.strip():
        raise ValueError("TASK_REQUIRED")
    if proposed_solution is not None and not isinstance(proposed_solution, str):
        raise ValueError("PROPOSED_SOLUTION_INVALID")
    if claims is not None and (not isinstance(claims, list) or any(not isinstance(c, Mapping) for c in claims)):
        raise ValueError("CLAIMS_INVALID")

    def scan(text: str) -> dict[str, Any]:
        normalized = text.casefold()
        domain_scores = {
            name: sum(word.casefold() in normalized for word in words)
            for name, words in _DOMAIN_KEYWORDS.items()
        }
        domains = [name for name, score in domain_scores.items() if score]
        # Prefer the domain with the most matching signals; taxonomy order
        # gives a deterministic tie break without claiming semantic certainty.
        domains.sort(key=lambda name: -domain_scores[name])
        risks = [name for name, words in _HIGH_RISK_KEYWORDS.items()
                 if any(word.casefold() in normalized for word in words)]
        return {
            "primary_domain": domains[0] if domains else None,
            "secondary_domains": domains[1:],
            "domains": domains,
            "high_risk_tags": risks,
            "temporal_sensitive": any(word.casefold() in normalized for word in _TEMPORAL_KEYWORDS),
            "evidence_strategies": {domain: _EVIDENCE_STRATEGIES[domain] for domain in domains},
            "status": "UNVERIFIED",
        }

    pre = scan(task)
    result: dict[str, Any] = {"pre_hypothesis_scan": pre, "post_hypothesis_scan": None,
                              "new_domains": [], "claim_units": [], "verification_status": "UNVERIFIED"}
    if proposed_solution is not None:
        post = scan(task + " " + proposed_solution)
        result["post_hypothesis_scan"] = post
        result["new_domains"] = [domain for domain in post["domains"] if domain not in pre["domains"]]
    if claims is not None:
        for index, claim in enumerate(claims):
            claim_text = claim.get("text", "")
            if not isinstance(claim_text, str):
                raise ValueError("CLAIM_TEXT_INVALID")
            claim_scan = scan(claim_text)
            result["claim_units"].append({
                "id": claim.get("id", f"claim-{index + 1}"),
                "domains": claim_scan["domains"],
                "high_risk_tags": claim_scan["high_risk_tags"],
                "temporal_sensitive": claim_scan["temporal_sensitive"],
                "status": "UNVERIFIED",
            })
    return result

@dataclass(frozen=True)
class CognitivePlan:
    mode: str
    operations: tuple[str, ...]
    reasons: tuple[str, ...] = ()
    information_gain_required: bool = True
    workflow_routing: Mapping[str, Any] | None = None

@dataclass(frozen=True)
class RouterConfig:
    deep_threshold: int = 2
    max_operations: int = 4

class CognitiveRouter:
    """Deterministic first-pass router; semantic ambiguity remains explicit."""

    def __init__(self, config: RouterConfig | None = None):
        self.config = config or RouterConfig()

    def route(self, request: Mapping[str, Any]) -> CognitivePlan:
        mode = str(request.get("mode", "MIXED")).upper()
        if mode not in MODES:
            raise ValueError("INVALID_MODE")

        task = str(request.get("task", "")).strip()
        context = request.get("context") or {}
        if not task:
            raise ValueError("TASK_REQUIRED")
        if not isinstance(context, Mapping):
            raise ValueError("CONTEXT_INVALID")

        text = " ".join([task, repr(context)]).lower()
        ops: list[str] = []
        reasons: list[str] = []

        def add(op: str, reason: str) -> None:
            if op not in ops and len(ops) < self.config.max_operations:
                ops.append(op); reasons.append(reason)

        if mode == "FAST":
            if any(k in text for k in ("verify", "fact check", "citation", "근거", "검증")):
                add("VERIFY", "explicit verification demand")
            else:
                add("SYNTHESIZE", "fast-path direct response")
        else:
            if any(k in text for k in ("explore", "alternatives", "가능성", "탐색", "범위")):
                add("EXPLORE", "breadth demand")
            if any(k in text for k in ("source", "paper", "article", "논문", "책", "보고서", "원문")):
                add("DEPTH", "source-depth demand")
            if any(k in text for k in ("premise", "assumption", "전제", "가정", "소크라테스")):
                add("EXAMINE", "premise examination demand")
            if any(k in text for k in ("counter", "counterargument", "반론", "반례")):
                add("COUNTER", "counterargument demand")
            if any(k in text for k in ("competing", "alternative explanation", "경쟁 설명", "대안 설명")):
                add("COMPETE", "competing explanation demand")
            if any(k in text for k in ("verify", "evidence", "citation", "검증", "근거", "출처")):
                add("VERIFY", "verification demand")

            if not ops:
                add("SYNTHESIZE", "no specialized operation detected")

            if mode == "DEEP" and "REVISE" not in ops and any(
                k in text for k in ("contradict", "new evidence", "수정", "반증", "충돌")
            ):
                add("REVISE", "revision demand")

        if mode == "MIXED" and len(ops) > 2:
            ops = ops[:2]
            reasons = reasons[:2]

        return CognitivePlan(
            mode,
            tuple(ops),
            tuple(reasons),
            workflow_routing=route_workflow_natural_language(task),
        )

def route(request: Mapping[str, Any]) -> dict[str, Any]:
    plan = CognitiveRouter().route(request)
    task = str(request.get("task", ""))
    solution = request.get("proposed_solution")
    return {
        "mode": plan.mode,
        "operations": list(plan.operations),
        "reasons": list(plan.reasons),
        "information_gain_required": plan.information_gain_required,
        "verification_status": "UNVERIFIED",
        "is_evidence": False,
        "workflow_routing": plan.workflow_routing,
        "verification_routing": route_verification_domains(
            task,
            proposed_solution=solution,
            claims=request.get("claims"),
        ),
    }
