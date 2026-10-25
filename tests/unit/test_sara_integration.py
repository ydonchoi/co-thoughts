import pytest

from runtime import CognitiveRuntime
from sara_integration import SARAConnection, default_sara_root


class FakeSARAAdapter:
    def __init__(self):
        self.payloads = []

    def evaluate(self, payload):
        self.payloads.append(payload)
        return {
            "adapter_revision": "fake-sara-v24",
            "claim_id": payload["claim"]["id"],
            "verification_status": payload["claim"]["verification_status"],
            "is_evidence": False,
        }


def test_sara_connection_forces_backend_claims_to_unverified_before_assessment():
    adapter = FakeSARAAdapter()
    connection = SARAConnection(adapter=adapter)
    result = connection.assess_output({
        "claims": [{"id": "C1", "text": "Claim text", "verification_status": "VERIFIED"}],
        "evidence": [],
    })

    assert adapter.payloads[0]["claim"]["verification_status"] == "UNVERIFIED"
    assert result["execution_status"] == "SUCCEEDED"
    assert result["verification_status"] == "UNVERIFIED"
    assert result["fact_verification_performed"] is False
    assert result["is_evidence"] is False


def test_sara_connection_reports_not_connected_without_adapter():
    connection = SARAConnection(root="C:/path/that/does/not/exist")
    result = connection.assess_output({"claims": []})
    assert connection.connected is False
    assert result["connection_status"] == "NOT_CONNECTED"
    assert result["verification_status"] == "UNVERIFIED"


def test_sara_state_adapter_is_called_by_runtime_after_generation():
    adapter = FakeSARAAdapter()

    class Backend:
        def generate(self, request):
            return {
                "execution_id": "E1", "status": "SUCCEEDED", "mode": request["mode"],
                "claims": [{
                    "id": "C1", "text": "Claim text", "verification_status": "CONTRADICTED",
                    "premises": [{"id": "P1", "text": "Premise", "verification_status": "VERIFIED"}],
                }],
                "premises": [{"id": "P2", "text": "Another premise", "verification_status": "VERIFIED"}],
                "epistemic_states": ["FACT"], "reasoning_artifact": {},
            }

    result = CognitiveRuntime(
        Backend(),
        sara_connection=SARAConnection(adapter=adapter),
    ).run({"task": "Review this claim", "mode": "DEEP", "context": {}})

    assert result["sara_assessment"]["connection_status"] == "CONNECTED"
    assert result["sara_assessment"]["execution_status"] == "SUCCEEDED"
    assert result["verification_status"] == "UNVERIFIED"
    assert adapter.payloads[0]["claim"]["verification_status"] == "UNVERIFIED"
    assert result["claims"][0]["verification_status"] == "UNVERIFIED"
    assert result["claims"][0]["premises"][0]["verification_status"] == "UNVERIFIED"
    assert result["premises"][0]["verification_status"] == "UNVERIFIED"


@pytest.mark.skipif(not default_sara_root().is_dir(), reason="Sibling SARA v2.4 checkout is not present")
def test_default_sara_connection_loads_sibling_adapter():
    connection = SARAConnection()
    assert connection.connected is True
    result = connection.assess_output({
        "claims": [{"id": "C1", "text": "Example claim"}],
        "evidence": [],
    })
    assert result["execution_status"] == "SUCCEEDED"
    assert result["claim_assessments"][0]["result"]["adapter_revision"] == "co-thoughts-v2.0/sara-v2.4"
    assert result["verification_status"] == "UNVERIFIED"
