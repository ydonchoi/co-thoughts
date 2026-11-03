"""Default lazy connection to the sibling SARA v2.4 epistemic adapter, and an
opt-in SARA v3 dialogue-turn connection."""

from __future__ import annotations

import importlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Callable, Mapping, Protocol


class SARAStateAdapter(Protocol):
    def evaluate(self, payload: Mapping[str, Any]) -> Mapping[str, Any]: ...


def default_sara_root() -> Path:
    configured = os.environ.get("CO_THOUGHTS_SARA_V24_ROOT", "").strip()
    if configured:
        return Path(configured).expanduser().resolve()
    # Typical OneDrive layout: Desktop/co-thoughts and Desktop/SARA.
    desktop = Path(__file__).resolve().parents[3]
    return desktop / "SARA" / "SARA_v2.4"


def _load_sara_adapter(root: Path) -> SARAStateAdapter:
    adapter_file = root / "co_thoughts_sara_adapter.py"
    if not adapter_file.is_file() or not (root / "sara_v24_epistemic.py").is_file():
        raise FileNotFoundError("SARA_V24_ADAPTER_NOT_FOUND")
    importlib.invalidate_caches()
    root_text = str(root)
    inserted = root_text not in sys.path
    if inserted:
        sys.path.insert(0, root_text)
    try:
        module = importlib.import_module("co_thoughts_sara_adapter")
        module_file = Path(module.__file__).resolve() if getattr(module, "__file__", None) else None
        if module_file != adapter_file.resolve():
            raise ImportError("SARA_ADAPTER_MODULE_PATH_MISMATCH")
        adapter_type = getattr(module, "CoThoughtsSARAAdapter", None)
        if not callable(adapter_type):
            raise ImportError("SARA_ADAPTER_CLASS_MISSING")
        return adapter_type()
    finally:
        if inserted:
            try:
                sys.path.remove(root_text)
            except ValueError:
                pass


class SARAConnection:
    """Use the SARA v2.4 adapter for epistemic-state and attribution checks."""

    def __init__(
        self,
        adapter: SARAStateAdapter | None = None,
        *,
        root: str | Path | None = None,
    ) -> None:
        self.root = Path(root).expanduser().resolve() if root is not None else default_sara_root()
        self.adapter = adapter
        self.connection_error: str | None = None
        if self.adapter is None:
            try:
                self.adapter = _load_sara_adapter(self.root)
            except Exception as exc:
                self.connection_error = type(exc).__name__

    @property
    def connected(self) -> bool:
        return self.adapter is not None

    def assess_output(self, output: Mapping[str, Any]) -> dict[str, Any]:
        base = {
            "connection_status": "CONNECTED" if self.connected else "NOT_CONNECTED",
            "adapter_revision": "co-thoughts-v2.0/sara-v2.4" if self.connected else None,
            "execution_status": "NOT_RUN",
            "assessment_scope": "EPISTEMIC_STATE_AND_ATTRIBUTION_CONSTRAINTS",
            "fact_verification_performed": False,
            "verification_status": "UNVERIFIED",
            "is_evidence": False,
        }
        if not self.connected:
            base["connection_error"] = self.connection_error or "SARA_ADAPTER_UNAVAILABLE"
        claims = output.get("claims", [])
        if not isinstance(claims, (list, tuple)):
            state_result = {**base, "execution_status": "FAILED", "error_code": "CLAIMS_INVALID"}
        elif not self.connected:
            state_result = {**base, "execution_status": "NOT_CONNECTED", "claim_assessments": []}
        elif not claims:
            state_result = {**base, "execution_status": "NOT_APPLICABLE", "claim_assessments": []}
        else:
            evidence = output.get("evidence", [])
            evidence = evidence if isinstance(evidence, (list, tuple)) else []
            premises = output.get("premises", [])
            premises = premises if isinstance(premises, (list, tuple)) else []
            assessments = []
            for index, item in enumerate(claims):
                claim = dict(item) if isinstance(item, Mapping) else {"text": str(item)}
                claim_id = claim.get("id") or f"CLAIM-{index + 1}"
                claim_text = claim.get("text")
                if not isinstance(claim_text, str) or not claim_text.strip():
                    assessments.append({"claim_id": claim_id, "execution_status": "FAILED", "error_code": "CLAIM_TEXT_REQUIRED"})
                    continue
                # A cognitive backend cannot self-promote a claim's verification state.
                safe_claim = {
                    "id": str(claim_id), "text": claim_text,
                    "verification_status": "UNVERIFIED",
                    "attribution_status": claim.get("attribution_status", "UNKNOWN"),
                    "temporal_status": claim.get("temporal_status", "CONTEMPORARY"),
                    "attribution_evidence_ids": claim.get("attribution_evidence_ids", []),
                }
                claim_premises = claim.get("premises", premises)
                if not isinstance(claim_premises, (list, tuple)):
                    claim_premises = []
                payload = {
                    "claim": safe_claim,
                    "premises": [dict(p) for p in claim_premises if isinstance(p, Mapping)],
                    "evidence": [dict(e) for e in evidence if isinstance(e, Mapping)],
                    "provenance_ids": output.get("provenance_ids", []),
                }
                try:
                    result = self.adapter.evaluate(payload)
                    if not isinstance(result, Mapping):
                        raise TypeError("SARA_ADAPTER_OUTPUT_MUST_BE_MAPPING")
                    assessments.append({"claim_id": str(claim_id), "execution_status": "SUCCEEDED",
                                       "result": dict(result), "result_is_research_evidence": False})
                except Exception as exc:
                    assessments.append({"claim_id": str(claim_id), "execution_status": "FAILED",
                                       "error_code": type(exc).__name__})
            failed = any(item["execution_status"] != "SUCCEEDED" for item in assessments)
            state_result = {**base, "execution_status": "PARTIALLY_FAILED" if failed else "SUCCEEDED",
                            "claim_assessments": assessments}
        return state_result


SARA_V3_RESULT_SCHEMA = "sara.dialogue-result.v3"
SARA_V3_ASSESSMENT_SCHEMA = "sara.assessment.v3"
_ERROR_CODE = re.compile(r"[A-Z0-9_]{1,96}")


class SARAv3Error(RuntimeError):
    """Sanitized SARA v3 bridge error; the message is a stable code."""


def default_sara_v3_root() -> Path:
    configured = os.environ.get("CO_THOUGHTS_SARA_ROOT", "").strip()
    if configured:
        return Path(configured).expanduser().resolve()
    return Path(__file__).resolve().parents[3] / "SARA"


class SubprocessSARAv3Runner:
    """Run `python -m SARA_v3.cli` in the SARA checkout.

    A separate process keeps SARA's module path (which contains names such as
    `execution`) apart from Co-thoughts modules. Provider credentials stay in the
    inherited host environment and are never placed in the request.
    """

    def __init__(self, root: str | Path, *, python: str | None = None) -> None:
        self.root = Path(root).expanduser().resolve()
        if not (self.root / "SARA_v3" / "cli.py").is_file():
            raise FileNotFoundError("SARA_V3_CLI_NOT_FOUND")
        self.python = python or os.environ.get("CO_THOUGHTS_SARA_PYTHON", "").strip() or sys.executable

    def __call__(self, payload: Mapping[str, Any], timeout_seconds: float) -> Mapping[str, Any]:
        env = {**os.environ, "PYTHONIOENCODING": "utf-8"}
        try:
            completed = subprocess.run(
                [self.python, "-m", "SARA_v3.cli", "--timeout-seconds", str(timeout_seconds)],
                input=json.dumps(dict(payload), ensure_ascii=False).encode("utf-8"),
                capture_output=True, cwd=self.root, env=env,
                # SARA applies the deadline per provider call; allow process startup on top.
                timeout=timeout_seconds * 4 + 30,
            )
        except subprocess.TimeoutExpired:
            raise SARAv3Error("SARA_V3_PROCESS_TIMEOUT") from None
        except OSError:
            raise SARAv3Error("SARA_V3_PROCESS_START_FAILED") from None
        if completed.returncode != 0:
            raise SARAv3Error(_cli_error_code(completed.stderr))
        try:
            result = json.loads(completed.stdout.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            raise SARAv3Error("SARA_V3_OUTPUT_NOT_JSON") from None
        if not isinstance(result, Mapping):
            raise SARAv3Error("SARA_V3_OUTPUT_MUST_BE_MAPPING")
        return result


def _cli_error_code(stderr: bytes) -> str:
    # Only the CLI's own JSON error code is surfaced; tracebacks are discarded.
    for line in reversed(stderr.decode("utf-8", errors="replace").splitlines()):
        try:
            payload = json.loads(line)
        except json.JSONDecodeError:
            continue
        code = payload.get("error_code") if isinstance(payload, Mapping) else None
        if isinstance(code, str) and _ERROR_CODE.fullmatch(code):
            return f"SARA_V3_{code}"
    return "SARA_V3_PROCESS_FAILED"


class SARAv3Connection:
    """Send an approved, minimal dialogue turn to SARA v3 and keep its envelopes.

    Only the turn identifiers, the generated response text (or claim texts), and
    explicit claim ids/texts are sent. Request context, task text, backend
    evidence, and backend-asserted statuses are not forwarded.
    """

    adapter_revision = "co-thoughts-v2.0/sara-v3"

    def __init__(
        self,
        process_turn: Callable[[Mapping[str, Any], float], Mapping[str, Any]] | None = None,
        *,
        root: str | Path | None = None,
        timeout_seconds: float = 60.0,
        max_claims: int = 8,
    ) -> None:
        if timeout_seconds <= 0:
            raise ValueError("TIMEOUT_INVALID")
        if max_claims <= 0:
            raise ValueError("MAX_CLAIMS_INVALID")
        self.timeout_seconds = timeout_seconds
        self.max_claims = max_claims
        self.process_turn = process_turn
        self.connection_error: str | None = None
        if self.process_turn is None:
            try:
                self.process_turn = SubprocessSARAv3Runner(root if root is not None else default_sara_v3_root())
            except Exception as exc:
                self.connection_error = str(exc) if _ERROR_CODE.fullmatch(str(exc)) else type(exc).__name__

    @property
    def connected(self) -> bool:
        return self.process_turn is not None

    def build_turn(self, request: Mapping[str, Any], output: Mapping[str, Any]) -> dict[str, Any]:
        request_id = request.get("request_id") or output.get("request_id")
        if not isinstance(request_id, str) or not request_id.strip():
            raise ValueError("REQUEST_ID_REQUIRED")
        candidates = []
        for index, item in enumerate(output.get("claims", []) or []):
            if not isinstance(item, Mapping):
                continue
            text = item.get("text")
            if isinstance(text, str) and text.strip():
                candidates.append({"id": str(item.get("id") or f"CLAIM-{index + 1}"), "text": text.strip()})
        if len(candidates) > self.max_claims:
            raise ValueError("CLAIM_LIMIT_EXCEEDED")
        response_text = output.get("response")
        content = response_text.strip() if isinstance(response_text, str) and response_text.strip() else "\n".join(
            item["text"] for item in candidates)
        return {
            "request_id": request_id.strip(),
            "conversation_id": str(request.get("conversation_id") or request_id).strip(),
            "turn_id": str(request.get("turn_id") or request_id).strip(),
            "content": content,
            "claim_candidates": candidates,
            "evidence": [],
            "provenance_ids": [f"co-thoughts:{output.get('execution_id', request_id)}"],
        }

    def assess_turn(self, request: Mapping[str, Any], output: Mapping[str, Any]) -> dict[str, Any]:
        base = {
            "connection_status": "CONNECTED" if self.connected else "NOT_CONNECTED",
            "adapter_revision": self.adapter_revision if self.connected else None,
            "execution_status": "NOT_RUN",
            "verification_status": "UNVERIFIED",
            "assessment_envelopes": [],
            "external_llm_response": None,
            "truthfulness_status": "UNASSESSED",
            "is_evidence": False,
        }
        if not self.connected:
            return {**base, "execution_status": "NOT_CONNECTED",
                    "connection_error": self.connection_error or "SARA_V3_UNAVAILABLE"}
        try:
            turn = self.build_turn(request, output)
        except ValueError as exc:
            return {**base, "error_code": str(exc)}
        base["sent_scope"] = {
            "claim_ids": [item["id"] for item in turn["claim_candidates"]],
            "content_chars": len(turn["content"]),
            "context_forwarded": False,
        }
        if not turn["claim_candidates"]:
            return {**base, "execution_status": "NOT_APPLICABLE"}
        try:
            result = self.process_turn(turn, self.timeout_seconds)
            envelopes = _validated_v3_result(result, set(base["sent_scope"]["claim_ids"]))
        except Exception as exc:
            code = str(exc)
            return {**base, "execution_status": "FAILED",
                    "error_code": code if isinstance(exc, (SARAv3Error, ValueError)) and _ERROR_CODE.fullmatch(code)
                    else type(exc).__name__.upper()}
        return {
            **base, "execution_status": "SUCCEEDED",
            "verification_status": result["verification_status"],
            "assessment_envelopes": envelopes,
            "external_llm_response": result.get("external_llm_response"),
            "sara_runtime_revision": result.get("runtime_revision"),
        }


def _validated_v3_result(result: Any, sent_claim_ids: set[str]) -> list[dict[str, Any]]:
    if not isinstance(result, Mapping) or result.get("schema_version") != SARA_V3_RESULT_SCHEMA:
        raise ValueError("SARA_V3_RESULT_INVALID")
    if not isinstance(result.get("verification_status"), str) or result.get("truthfulness_status") != "UNASSESSED":
        raise ValueError("SARA_V3_RESULT_INVALID")
    envelopes = validate_assessment_envelopes(result.get("assessment_envelopes"))
    if any(item["claim_id"] not in sent_claim_ids for item in envelopes):
        raise ValueError("SARA_V3_ENVELOPE_CLAIM_NOT_SENT")
    return envelopes


def validate_assessment_envelopes(value: Any) -> list[dict[str, Any]]:
    """Accept only SARA v3 assessment envelopes; return detached copies."""
    if not isinstance(value, (list, tuple)):
        raise ValueError("SARA_ENVELOPES_INVALID")
    envelopes = []
    for item in value:
        if (not isinstance(item, Mapping) or item.get("schema_version") != SARA_V3_ASSESSMENT_SCHEMA
                or not isinstance(item.get("claim_id"), str) or not isinstance(item.get("verification_status"), str)
                or item.get("is_evidence") is not False):
            raise ValueError("SARA_ENVELOPES_INVALID")
        envelopes.append(json.loads(json.dumps(item)))
    return envelopes

