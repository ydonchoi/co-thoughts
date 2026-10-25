"""Default lazy connection to the sibling SARA v2.4 epistemic adapter."""

from __future__ import annotations

import importlib
import os
import sys
from pathlib import Path
from typing import Any, Mapping, Protocol


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

