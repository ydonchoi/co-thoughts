from execution import CoThoughtsReferenceExecutor


def test_reference_executor_preserves_v13_separations():
    result = CoThoughtsReferenceExecutor().run(
        {
            "request_id": "REQ-CO-1",
            "task": "Evaluate a research hypothesis",
            "mode": "DEEP",
            "claims": [
                {
                    "id": "C1",
                    "text": "The hypothesis may explain the observation.",
                    "epistemic_type": "HYPOTHESIS",
                }
            ],
            "evidence": [{"id": "E1", "status": "UNVERIFIED"}],
            "verification": {"status": "UNVERIFIED"},
            "revision": {"changed": True},
            "transition": {"continue": True, "reason": "NEW_EVIDENCE"},
            "checkpoint": {
                "claim": "C1",
                "status": "HYPOTHESIS",
                "is_evidence": False,
            },
        }
    )

    assert result["protocol_version"] == "v1.3"
    assert result["mode"] == "DEEP"
    assert result["claims"][0]["epistemic_type"] == "HYPOTHESIS"
    assert result["checkpoint"]["is_evidence"] is False
    assert result["is_evidence"] is False
    assert result["verification_status"] == "UNVERIFIED"
    assert result["execution_status"] == "SUCCEEDED"


def test_fast_path_does_not_require_deep_stages():
    result = CoThoughtsReferenceExecutor().run(
        {
            "request_id": "REQ-FAST-1",
            "task": "Convert one hour to minutes",
            "mode": "FAST",
        }
    )

    assert result["mode"] == "FAST"
    assert result["claims"] == ()
    assert result["verification"] is None
    assert result["checkpoint"] is None


def test_invalid_mode_is_rejected():
    try:
        CoThoughtsReferenceExecutor().run(
            {"request_id": "REQ-INVALID", "task": "A task", "mode": "INVALID"}
        )
    except ValueError as exc:
        assert str(exc) == "INVALID_MODE"
    else:
        raise AssertionError("invalid mode must be rejected")


def test_checkpoint_cannot_be_marked_as_evidence():
    try:
        CoThoughtsReferenceExecutor().run(
            {
                "request_id": "REQ-CHK",
                "task": "A task",
                "mode": "MIXED",
                "checkpoint": {"is_evidence": True},
            }
        )
    except ValueError as exc:
        assert str(exc) == "CHECKPOINT_IS_NOT_EVIDENCE"
    else:
        raise AssertionError("checkpoint/evidence conflation must be rejected")
