"""Source, temporal and attribution boundaries for Co-thoughts v2.0."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any

TEMPORAL = {"HISTORICAL","POST_PUBLICATION","CONTEMPORARY"}
INTERPRETIVE = {"AUTHOR_EXPLICIT","AUTHOR_SUPPORTED","SOURCE_INFERRED","FIELD_INTERPRETATION","MODERN_INTERPRETATION","SPECULATIVE","UNKNOWN"}
RELATIONS = {"SUPPORTING","CHALLENGING","NEUTRAL"}

@dataclass(frozen=True)
class ContextItem:
    id: str
    text: str
    temporal_status: str = "CONTEMPORARY"
    interpretive_status: str = "UNKNOWN"
    relation: str = "NEUTRAL"
    source_id: str | None = None

    def __post_init__(self):
        if self.temporal_status not in TEMPORAL: raise ValueError("INVALID_TEMPORAL_STATUS")
        if self.interpretive_status not in INTERPRETIVE: raise ValueError("INVALID_INTERPRETIVE_STATUS")
        if self.relation not in RELATIONS: raise ValueError("INVALID_CONTEXT_RELATION")

def attribution_firewall(*, target_attribution: str, source_evidence: bool, temporal_status: str, source_temporal_status: str | None = None) -> None:
    if target_attribution == "AUTHOR_EXPLICIT" and not source_evidence:
        raise PermissionError("AUTHOR_ATTRIBUTION_REQUIRES_SOURCE_EVIDENCE")
    if target_attribution == "AUTHOR_EXPLICIT" and temporal_status != "HISTORICAL":
        raise PermissionError("AUTHOR_EXPLICIT_REQUIRES_HISTORICAL_CONTEXT")
    if source_temporal_status == "HISTORICAL" and temporal_status in {"POST_PUBLICATION","CONTEMPORARY"}:
        raise PermissionError("TEMPORAL_CONTEXT_CANNOT_BE_SILENTLY_RECAST")
