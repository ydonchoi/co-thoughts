"""Co-thoughts v2.0 epistemic objects and non-monotonic revision."""
from __future__ import annotations
from dataclasses import dataclass, field, replace
from typing import Any

TYPES = {"FACT","INTERPRETATION","INFERENCE","HYPOTHESIS","SIMULATION"}
VERIFICATION = {"VERIFIED","PARTIALLY VERIFIED","UNVERIFIED","CONTRADICTED"}
ATTRIBUTION = {
    "AUTHOR_EXPLICIT","AUTHOR_SUPPORTED","SOURCE_INFERRED",
    "FIELD_INTERPRETATION","MODERN_INTERPRETATION","SPECULATIVE","UNKNOWN",
}
TEMPORAL = {"HISTORICAL","POST_PUBLICATION","CONTEMPORARY"}

@dataclass(frozen=True)
class Premise:
    id: str
    text: str
    type: str = "HYPOTHESIS"
    verification_status: str = "UNVERIFIED"
    provenance_ids: tuple[str, ...] = ()

    def __post_init__(self):
        if self.type not in TYPES: raise ValueError("INVALID_EPISTEMIC_TYPE")
        if self.verification_status not in VERIFICATION: raise ValueError("INVALID_VERIFICATION_STATUS")

@dataclass(frozen=True)
class Claim:
    id: str
    text: str
    type: str = "INFERENCE"
    verification_status: str = "UNVERIFIED"
    attribution_status: str = "UNKNOWN"
    temporal_status: str = "CONTEMPORARY"
    premises: tuple[Premise, ...] = ()
    provenance_ids: tuple[str, ...] = ()

    def __post_init__(self):
        if self.type not in TYPES: raise ValueError("INVALID_EPISTEMIC_TYPE")
        if self.verification_status not in VERIFICATION: raise ValueError("INVALID_VERIFICATION_STATUS")
        if self.attribution_status not in ATTRIBUTION: raise ValueError("INVALID_ATTRIBUTION_STATUS")
        if self.temporal_status not in TEMPORAL: raise ValueError("INVALID_TEMPORAL_STATUS")
        if self.attribution_status == "AUTHOR_EXPLICIT" and self.type == "SIMULATION":
            raise ValueError("SIMULATION_CANNOT_BE_AUTHOR_EXPLICIT")

@dataclass(frozen=True)
class EvidenceAlignment:
    evidence_id: str
    relation: str
    target_id: str
    status: str = "UNASSESSED"

@dataclass(frozen=True)
class Revision:
    claim_id: str
    previous_status: str
    new_status: str
    reason: str
    provenance_ids: tuple[str, ...] = ()

def revise_claim(claim: Claim, new_status: str, reason: str, provenance_ids: tuple[str, ...] = ()) -> tuple[Claim, Revision]:
    if new_status not in VERIFICATION:
        raise ValueError("INVALID_VERIFICATION_STATUS")
    revision = Revision(claim.id, claim.verification_status, new_status, reason, provenance_ids)
    return replace(claim, verification_status=new_status, provenance_ids=tuple(dict.fromkeys(claim.provenance_ids + provenance_ids))), revision
