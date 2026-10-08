# Cognitive Runtime Safety Contract v0.1

Status: IMPLEMENTED / PROVIDER-NEUTRAL

## Purpose

runtime.py provides a callable Cognitive/THINK runtime boundary that can wrap
an actual LLM backend without granting the backend epistemic authority or
default external side effects.

## Safety invariants

1. THINK != VERIFY.
2. Execution Success != Research Validity.
3. Model output != Evidence.
4. Tool execution is default-deny.
5. External side effects are default-deny.
6. Backend self-declaration cannot establish verification.
7. Oversized task/context input is rejected.
8. Epistemic states are constrained to the protocol vocabulary.

## Runtime flow

Request
  -> SafetyGate(request)
  -> Provider-neutral backend
  -> SafetyGate(response)
  -> Epistemic firewall
  -> UNVERIFIED / is_evidence=false
  -> downstream consumer

## Provider integration

A provider is supplied through CognitiveBackend.generate().
The runtime does not assume OpenAI, Gemini, Claude, local models, HTTP, MCP,
or CLI. A concrete provider must be integrated separately and must pass the
same request/response and safety tests.

## Default-deny boundaries

The runtime does not execute tools or external side effects unless an explicit
policy enables them. Enabling those capabilities is a separate security
review concern and must never be inferred from backend output.

## Epistemic firewall

A backend returning verification_status=ESTABLISHED or is_evidence=true is
rejected before downstream use.

Even valid cognitive output is normalized to:

- verification_status=UNVERIFIED
- is_evidence=false

Verification belongs to an independent verification layer.

## Promotion gate

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
