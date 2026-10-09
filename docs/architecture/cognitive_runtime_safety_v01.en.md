# Cognitive Runtime Safety Contract v0.1

Status: **IMPLEMENTED / PROVIDER-NEUTRAL**

## Purpose

`runtime.py` provides a callable Cognitive/THINK runtime boundary that can wrap an actual LLM backend without granting that backend epistemic authority or default external side effects.

## Safety Invariants

1. THINK ≠ VERIFY.
2. Execution Success ≠ Research Validity.
3. Model Output ≠ Evidence.
4. Tool execution is default-deny.
5. External side effects are default-deny.
6. A backend's self-declaration cannot establish verification.
7. Oversized task/context input is rejected.
8. Epistemic states are constrained to the protocol vocabulary.

## Runtime Flow

Request  
→ SafetyGate(request)  
→ Provider-neutral backend  
→ SafetyGate(response)  
→ Epistemic firewall  
→ UNVERIFIED / is_evidence=false

A backend returning `verification_status=ESTABLISHED` or `is_evidence=true` is rejected before downstream use.

Even valid cognitive output is normalized to:
- `verification_status=UNVERIFIED`
- `is_evidence=false`

Verification belongs to an independent verification layer.

## Promotion Gate

A concrete provider may be considered for integration only after:

1. real provider execution;
2. artifact retention;
3. request/response provenance;
4. timeout/error handling;
5. prompt/context isolation tests;
6. adversarial output tests;
7. tool/side-effect boundary tests;
8. CI evidence.

Passing this runtime contract does not establish research truth.

---

[Korean source](cognitive_runtime_safety_v01.md)
