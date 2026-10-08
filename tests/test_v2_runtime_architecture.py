from cognitive_router import CognitiveRouter
from epistemic_state import Claim, Premise, revise_claim
from context import attribution_firewall
import pytest

def test_fast_path_does_not_expand():
    p=CognitiveRouter().route({"task":"summarize this","mode":"FAST","context":{}})
    assert p.operations==("SYNTHESIZE",)

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
