# Research Note Data Model v0.1 (provisional project term)

Status: HISTORICAL / RECONSTRUCTED / SUPERSEDED

> Reconstructed from recorded project architecture decisions; not a byte-for-byte historical snapshot.

## Initial Logical Entities
1. Conversation Session
2. Research Object
3. Research Note
4. Claim
5. Evidence
6. Verification / SARA
7. Note Relation
8. Taxonomy

## Core Semantics

### Conversation Session
The origin/provenance of the source conversation. It is not itself a Research Note.

### Research Object
A separable question, claim, concept, phenomenon, hypothesis, model, evidence problem, contradiction, or research gap identified from a conversation.

### Research Note
A document representation of a Research Object using a document-type-specific structure.

### Claim
A proposition that can be evaluated independently for truth/epistemic status.

### Evidence
A unit that supports, contradicts, contextualizes, illustrates, or otherwise bears on a Claim. Source and Evidence are not identical.

### Verification / SARA
Verification records the review of Claims against Evidence and the resulting revision/re-verification state.

### Note Relation
Relations among Research Notes, including derivation, support, challenge, extension, refinement, contradiction, synthesis, contextualization, and evidence linkage.

### Taxonomy
Classification metadata for Research Purpose and related axes.

## Design Principle
The logical entity model was separated from the eventual number of Notion databases. One conversation was not forced into one Research Note.

## Supersession
Superseded as provenance and lifecycle requirements expanded.

---

[Korean source](research_note_data_model_v0.1.md)
