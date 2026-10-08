# Switchable Cognitive Backend Contract v0.1

## Modes

The backend supports three explicit modes:

- AUTO: use an external provider when configured; otherwise use user-mediated general LLM input.
- PROVIDER: require and use an external provider.
- USER_INPUT: require the user-mediated general LLM path.

## Fallback semantics

The USER_INPUT path does not pretend to be a native provider call. It records the source as USER_INPUT and identifies the backend as user-mediated-general-llm.

The user may paste the JSON response produced by a general-purpose LLM into the runtime. The response is still subjected to the same CognitiveRuntime safety and epistemic firewall.

## Safety boundary

A pasted response cannot establish research verification, evidence status, external citation truth, or scientific validity.

The user-input prompt explicitly instructs the general LLM not to claim these properties, and CognitiveRuntime independently rejects such claims if they are returned.

## Provider precedence

AUTO is deterministic:

1. configured external provider;
2. otherwise configured user-input backend;
3. otherwise fail closed with NO_COGNITIVE_BACKEND_AVAILABLE.

This is a runtime availability decision, not an epistemic quality decision. A provider response is not inherently more truthful than a user-mediated response; both remain cognitive execution output until independently verified.
