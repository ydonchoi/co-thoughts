"""Switchable cognitive backends.

AUTO uses an external provider when configured; otherwise it falls back to a
user-mediated general-LLM path. The fallback never claims that the pasted
answer came from a verified provider.
"""

from __future__ import annotations

import json
from typing import Any, Callable, Mapping, Protocol


class BackendLike(Protocol):
    def generate(self, request: Mapping[str, Any]) -> Mapping[str, Any]: ...


class UserInputCognitiveBackend:
    """Prepare a portable prompt and accept a user-supplied LLM response."""

    backend_revision = "user-input-bridge-v0.1"

    def __init__(self, input_fn: Callable[[str], str]) -> None:
        self.input_fn = input_fn

    def build_prompt(self, request: Mapping[str, Any]) -> str:
        envelope = {
            "protocol": "co-thoughts-v1.3",
            "task": request["task"],
            "mode": request["mode"],
            "context": request.get("context", {}),
            "constraints": {
                "do_not_claim_research_verification": True,
                "do_not_claim_evidence_status": True,
                "return_json_only": True,
                "epistemic_types": [
                    "FACT",
                    "INTERPRETATION",
                    "INFERENCE",
                    "HYPOTHESIS",
                    "UNKNOWN",
                ],
            },
            "required_response": {
                "execution_id": "string",
                "status": "SUCCEEDED|FAILED|REJECTED",
                "mode": request["mode"],
                "claims": "array",
                "epistemic_states": "array",
                "reasoning_artifact": "object",
            },
        }
        return (
            "You are a cognitive reasoning backend for Co-Thoughts. "
            "Return only JSON matching the supplied contract. "
            "Do not claim verification or evidence status.\\n\\n"
            + json.dumps(envelope, ensure_ascii=False, indent=2)
        )

    def generate(self, request: Mapping[str, Any]) -> Mapping[str, Any]:
        prompt = self.build_prompt(request)
        raw = self.input_fn(prompt)
        if not isinstance(raw, str) or not raw.strip():
            raise ValueError("USER_LLM_RESPONSE_EMPTY")

        try:
            response = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise ValueError("USER_LLM_RESPONSE_NOT_JSON") from exc

        if not isinstance(response, Mapping):
            raise TypeError("USER_LLM_RESPONSE_MUST_BE_MAPPING")

        output = dict(response)
        output.setdefault("execution_id", f"user-input:{request.get('request_id', 'unknown')}")
        output.setdefault("mode", request["mode"])
        output.setdefault("provider_id", "user-mediated-general-llm")
        output.setdefault("backend_revision", self.backend_revision)
        output["source"] = "USER_INPUT"
        return output


class SwitchableCognitiveBackend:
    """AUTO -> external provider when available, otherwise user-mediated LLM."""

    backend_revision = "switchable-cognitive-backend-v0.1"

    def __init__(
        self,
        *,
        provider: BackendLike | None = None,
        user_input_backend: UserInputCognitiveBackend | None = None,
        mode: str = "AUTO",
    ) -> None:
        if mode not in {"AUTO", "PROVIDER", "USER_INPUT"}:
            raise ValueError("INVALID_BACKEND_MODE")
        if mode == "PROVIDER" and provider is None:
            raise ValueError("PROVIDER_BACKEND_MISSING")
        if mode == "USER_INPUT" and user_input_backend is None:
            raise ValueError("USER_INPUT_BACKEND_MISSING")

        self.provider = provider
        self.user_input_backend = user_input_backend
        self.mode = mode

    def generate(self, request: Mapping[str, Any]) -> Mapping[str, Any]:
        if self.mode == "PROVIDER":
            return self.provider.generate(request)

        if self.mode == "USER_INPUT":
            return self.user_input_backend.generate(request)

        if self.provider is not None:
            return self.provider.generate(request)

        if self.user_input_backend is not None:
            return self.user_input_backend.generate(request)

        raise RuntimeError("NO_COGNITIVE_BACKEND_AVAILABLE")
