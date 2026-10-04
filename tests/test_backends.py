import json

import pytest

from backends import JsonHttpCognitiveBackend


class FakeResponse:
    def __init__(self, payload, headers=None):
        self.payload = payload
        self.headers = headers or {}

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def read(self, size=-1):
        return self.payload


def test_https_backend_sends_json_and_bearer(monkeypatch):
    seen = {}

    def fake_urlopen(request, timeout):
        seen["url"] = request.full_url
        seen["body"] = json.loads(request.data.decode("utf-8"))
        seen["auth"] = request.headers["Authorization"]
        seen["timeout"] = timeout
        return FakeResponse(b'{"execution_id":"E","status":"SUCCEEDED","mode":"FAST","claims":[],"epistemic_states":[],"reasoning_artifact":{}}')

    class FakeOpener:
        def open(self, request, timeout):
            return fake_urlopen(request, timeout)

    monkeypatch.setattr("urllib.request.build_opener", lambda handler: FakeOpener())

    result = JsonHttpCognitiveBackend(
        "https://example.test/cognitive",
        api_key="secret",
        timeout_seconds=7,
    ).generate({"request_id": "R", "task": "x", "mode": "FAST"})

    assert result["execution_id"] == "E"
    assert seen["url"] == "https://example.test/cognitive"
    assert seen["body"]["request_id"] == "R"
    assert seen["auth"] == "Bearer secret"
    assert seen["timeout"] == 7


def test_backend_rejects_plain_http_by_default():
    with pytest.raises(ValueError, match="HTTPS_REQUIRED"):
        JsonHttpCognitiveBackend("http://example.test/cognitive")


def test_backend_allows_local_http_only_when_explicit():
    JsonHttpCognitiveBackend(
        "http://localhost:8080/cognitive",
        allow_insecure_localhost=True,
    )


def test_backend_rejects_oversized_response(monkeypatch):
    def fake_urlopen(request, timeout):
        return FakeResponse(b"x" * 20)

    monkeypatch.setattr("urllib.request.urlopen", fake_urlopen)

    with pytest.raises(ValueError, match="RESPONSE_TOO_LARGE"):
        JsonHttpCognitiveBackend(
            "https://example.test/cognitive",
            max_response_bytes=10,
        ).generate({"task": "x", "mode": "FAST"})
