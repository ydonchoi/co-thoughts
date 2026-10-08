"""Minimal HTTPS JSON cognitive backend.

The backend is deliberately provider-neutral. A compatible endpoint must accept
the request JSON and return a CognitiveRuntime-compatible response JSON.
"""

from __future__ import annotations

import json
import urllib.error
import urllib.request
from typing import Any, Mapping


class _NoRedirectHandler(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise RuntimeError("PROVIDER_REDIRECT_BLOCKED")


class JsonHttpCognitiveBackend:
    """Call a configured HTTPS JSON endpoint with conservative defaults."""

    def __init__(
        self,
        endpoint: str,
        *,
        api_key: str | None = None,
        timeout_seconds: float = 30.0,
        max_response_bytes: int = 2_000_000,
        allow_insecure_localhost: bool = False,
    ) -> None:
        if not endpoint.startswith(("https://", "http://")):
            raise ValueError("ENDPOINT_SCHEME_INVALID")
        if endpoint.startswith("http://") and not (
            allow_insecure_localhost and endpoint.startswith("http://localhost")
        ):
            raise ValueError("HTTPS_REQUIRED")
        if timeout_seconds <= 0:
            raise ValueError("TIMEOUT_INVALID")
        if max_response_bytes <= 0:
            raise ValueError("MAX_RESPONSE_BYTES_INVALID")

        self.endpoint = endpoint
        self.api_key = api_key
        self.timeout_seconds = timeout_seconds
        self.max_response_bytes = max_response_bytes

    def generate(self, request: Mapping[str, Any]) -> Mapping[str, Any]:
        body = json.dumps(dict(request), ensure_ascii=False).encode("utf-8")
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        http_request = urllib.request.Request(
            self.endpoint,
            data=body,
            headers=headers,
            method="POST",
        )

        try:
            opener = urllib.request.build_opener(_NoRedirectHandler)
            with opener.open(
                http_request,
                timeout=self.timeout_seconds,
            ) as response:
                content_length = response.headers.get("Content-Length")
                if content_length and int(content_length) > self.max_response_bytes:
                    raise ValueError("RESPONSE_TOO_LARGE")
                payload = response.read(self.max_response_bytes + 1)
        except urllib.error.HTTPError as exc:
            raise RuntimeError(f"PROVIDER_HTTP_ERROR_{exc.code}") from exc
        except urllib.error.URLError as exc:
            raise RuntimeError("PROVIDER_CONNECTION_ERROR") from exc

        if len(payload) > self.max_response_bytes:
            raise ValueError("RESPONSE_TOO_LARGE")

        try:
            decoded = json.loads(payload.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("PROVIDER_RESPONSE_NOT_JSON") from exc

        if not isinstance(decoded, Mapping):
            raise TypeError("PROVIDER_RESPONSE_MUST_BE_MAPPING")
        return decoded
