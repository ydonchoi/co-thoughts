"""Minimal executable reference harness for Co-Thoughts v1.3.

This module implements the protocol's execution *boundary* rather than an LLM
reasoning engine. It validates and packages caller-supplied cognitive state so
that FAST/MIXED/DEEP, Claim/Epistemic Type, Evidence/Verification,
Revision, Transition, and Checkpoint remain distinguishable.

It does not establish research truth and does not perform external verification.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping


MODES = frozenset({"FAST", "MIXED", "DEEP"})
EPISTEMIC_TYPES = frozenset(
    {"FACT", "INTERPRETATION", "INFERENCE", "HYPOTHESIS", "UNKNOWN"}
)


@dataclass(frozen=True)
class CoThoughtsExecutionRequest:
    task: str
    mode: str
    claims: tuple[Mapping[str, Any], ...] = ()
    evidence: tuple[Mapping[str, Any], ...] = ()
    verification: Mapping[str, Any] | None = None
    revision: Mapping[str, Any] | None = None
    transition: Mapping[str, Any] | None = None
    checkpoint: Mapping[str, Any] | None = None

    @classmethod
    def from_mapping(cls, request: Mapping[str, Any]) -> "CoThoughtsExecutionRequest":
        task = request.get("task")
        mode = request.get("mode")

        if not isinstance(task, str) or not task.strip():
            raise ValueError("CURRENT_TASK_MISSING")
        if mode not in MODES:
            raise ValueError("INVALID_MODE")

        claims = request.get("claims", ())
        evidence = request.get("evidence", ())
        if not isinstance(claims, (list, tuple)):
            raise ValueError("INVALID_CLAIMS")
        if not isinstance(evidence, (list, tuple)):
            raise ValueError("INVALID_EVIDENCE")

        normalized_claims = tuple(
            item for item in claims if isinstance(item, Mapping)
        )
        normalized_evidence = tuple(
            item for item in evidence if isinstance(item, Mapping)
        )

        if len(normalized_claims) != len(claims):
            raise ValueError("INVALID_CLAIM_ENTRY")
        if len(normalized_evidence) != len(evidence):
            raise ValueError("INVALID_EVIDENCE_ENTRY")

        for claim in normalized_claims:
            epistemic_type = claim.get("epistemic_type")
            if epistemic_type is not None and epistemic_type not in EPISTEMIC_TYPES:
                raise ValueError("INVALID_EPISTEMIC_TYPE")

        checkpoint = request.get("checkpoint")
        if checkpoint is not None and not isinstance(checkpoint, Mapping):
            raise ValueError("INVALID_CHECKPOINT")

        if isinstance(checkpoint, Mapping) and checkpoint.get("is_evidence") is True:
            raise ValueError("CHECKPOINT_IS_NOT_EVIDENCE")

        return cls(
            task=task.strip(),
            mode=mode,
            claims=normalized_claims,
            evidence=normalized_evidence,
            verification=request.get("verification"),
            revision=request.get("revision"),
            transition=request.get("transition"),
            checkpoint=checkpoint,
        )


class CoThoughtsReferenceExecutor:
    """Execute the v1.3 boundary contract without inventing reasoning."""

    protocol_version = "v1.3"
    executor_revision = "reference-harness-v0.1"

    def run(self, request: dict[str, Any]) -> dict[str, Any]:
        parsed = CoThoughtsExecutionRequest.from_mapping(request)

        return {
            "kind": "co_thoughts_execution",
            "protocol_version": self.protocol_version,
            "executor_revision": self.executor_revision,
            "task": parsed.task,
            "mode": parsed.mode,
            "claims": tuple(dict(item) for item in parsed.claims),
            "evidence": tuple(dict(item) for item in parsed.evidence),
            "verification": (
                dict(parsed.verification)
                if isinstance(parsed.verification, Mapping)
                else parsed.verification
            ),
            "revision": (
                dict(parsed.revision)
                if isinstance(parsed.revision, Mapping)
                else parsed.revision
            ),
            "transition": (
                dict(parsed.transition)
                if isinstance(parsed.transition, Mapping)
                else parsed.transition
            ),
            "checkpoint": (
                dict(parsed.checkpoint)
                if isinstance(parsed.checkpoint, Mapping)
                else parsed.checkpoint
            ),
            "is_evidence": False,
            "verification_status": "UNVERIFIED",
            "execution_status": "SUCCEEDED",
        }
