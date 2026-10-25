from cognitive_router import CognitiveRouter, route, route_verification_domains
from epistemic_state import Claim, Premise, revise_claim
from context import attribution_firewall
import pytest

def test_fast_path_does_not_expand():
    p=CognitiveRouter().route({"task":"summarize this","mode":"FAST","context":{}})
    assert p.operations==("SYNTHESIZE",)

def test_domain_routing_flags_temporal_and_high_risk_needs():
    result = route_verification_domains("Check current housing law and safety requirements")
    scan = result["pre_hypothesis_scan"]
    assert "law_regulation" in scan["domains"]
    assert "spatial_housing_urban" in scan["domains"]
    assert "law_regulation" in scan["high_risk_tags"]
    assert "health_safety" in scan["high_risk_tags"]
    assert scan["temporal_sensitive"] is True
    assert result["verification_status"] == "UNVERIFIED"

def test_post_solution_scan_surfaces_new_domains_and_claim_units():
    result = route_verification_domains(
        "Improve neighborhood access",
        proposed_solution="Fund a health clinic and evaluate the budget",
        claims=[{"id": "C1", "text": "Current medical guidance supports this treatment"}],
    )
    assert result["pre_hypothesis_scan"]["domains"] == ["spatial_housing_urban"]
    assert "health" in result["new_domains"]
    assert "economics_finance_operations" in result["new_domains"]
    assert result["claim_units"][0]["id"] == "C1"
    assert result["claim_units"][0]["temporal_sensitive"] is True
    assert result["claim_units"][0]["status"] == "UNVERIFIED"

def test_domain_router_does_not_force_domains_for_simple_tasks():
    result = route_verification_domains("Summarize this paragraph")
    assert result["pre_hypothesis_scan"]["domains"] == []
    assert result["pre_hypothesis_scan"]["primary_domain"] is None

def test_public_route_includes_domain_plan_without_claiming_verification():
    result = route({"task": "Review current public policy", "mode": "MIXED", "context": {}})
    assert "public_policy" in result["verification_routing"]["pre_hypothesis_scan"]["domains"]
    assert result["verification_status"] == "UNVERIFIED"
    assert result["is_evidence"] is False

def test_domain_router_rejects_malformed_claims():
    with pytest.raises(ValueError, match="CLAIM_TEXT_INVALID"):
        route_verification_domains("Assess policy", claims=[{"text": 42}])

def test_natural_language_router_recognizes_korean_and_english_workflow_cues():
    assert route({"task": "실행 가능성 검토 부탁해", "mode": "DEEP"})["workflow_routing"]["workflow"] == "feasibility_review"
    assert route({"task": "Please compare my hypothesis with yours", "mode": "DEEP"})["workflow_routing"]["workflow"] == "hypothesis_delta"

def test_natural_language_router_reports_ambiguous_multi_cluster_request():
    routing = route({"task": "문제 진단 후 해결안 설계해줘", "mode": "DEEP"})["workflow_routing"]
    assert routing["status"] == "AMBIGUOUS"
    assert routing["workflow"] is None
    assert set(routing["candidates"]) == {"problem_diagnosis", "solution_design"}

def test_deep_source_and_premise_route():
    p=CognitiveRouter().route({"task":"deeply examine the paper premise and verify evidence","mode":"DEEP","context":{}})
    assert "DEPTH" in p.operations
    assert "EXAMINE" in p.operations
    assert "VERIFY" in p.operations

def test_premise_is_independent_from_claim():
    c=Claim("C1","claim",premises=(Premise("P1","premise",verification_status="CONTRADICTED"),))
    assert c.verification_status=="UNVERIFIED"
    assert c.premises[0].verification_status=="CONTRADICTED"

def test_non_monotonic_revision():
    c=Claim("C1","claim",verification_status="PARTIALLY VERIFIED")
    updated,rev=revise_claim(c,"CONTRADICTED","new evidence")
    assert updated.verification_status=="CONTRADICTED"
    assert rev.previous_status=="PARTIALLY VERIFIED"

def test_modern_interpretation_cannot_be_author_explicit_without_source():
    with pytest.raises(PermissionError):
        attribution_firewall(target_attribution="AUTHOR_EXPLICIT",source_evidence=False,temporal_status="HISTORICAL")
