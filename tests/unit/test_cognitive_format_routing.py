from cognitive_router import route


def test_public_route_includes_format_plan_without_changing_cognitive_or_verification_fields():
    result = route({
        "task": "Explain the system architecture diagram and verify its assumptions",
        "mode": "DEEP",
        "context": {},
        "capabilities": {"diagram": True},
    })
    assert result["format_routing"]["format_plan"]["primary"] == "DIAGRAM"
    assert "VERIFY" in result["operations"]
    assert result["verification_status"] == "UNVERIFIED"
    assert result["is_evidence"] is False
    assert result["verification_routing"]["verification_status"] == "UNVERIFIED"


def test_format_request_falls_back_without_affecting_existing_routes():
    result = route({
        "task": "Summarize this paragraph",
        "mode": "FAST",
        "context": {},
        "output_intent": {"requested_format": "VIDEO"},
    })
    assert result["operations"] == ["SYNTHESIZE"]
    assert result["format_routing"]["format_plan"]["primary"] == "TEXT"
    assert result["format_routing"]["format_plan"]["selection_status"] == "FALLBACK"
    assert result["workflow_routing"]["status"] == "NO_MATCH"
