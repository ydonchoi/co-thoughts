# Research Note Data Model v0.2 (가칭)

Status: HISTORICAL / RECONSTRUCTED / SUPERSEDED

> Reconstructed from recorded architecture decisions; not a byte-for-byte historical snapshot.

## Main Changes

v0.2 made classification and verification state explicit and added richer metadata around Research Objects, Research Notes, Claims, Evidence, and Relations.

## Research Object Metadata

RO ID, original expression, normalized question, object type, source session/segment, parent object, primary/secondary purpose, question operator, domain, candidate/final document type, epistemic status, evidence status, SARA status, object decision, related note, taxonomy provenance, generation provenance, revision history.

## Research Note Metadata

Note ID, title, document type, research purpose, primary/secondary questions, source session/objects, related notes, domain, design, method, review type, R&D orientation, knowledge product, epistemic state, evidence state, verification date, SARA status, uncertainty, boundary, counter-evidence, revision version, synthesis status.

## Claim / Evidence Separation

Claims and evidence were modeled separately so that a note could contain claims with different epistemic states and evidence mappings.

Evidence roles included SUPPORT, CONTRADICT, CONTEXT, ILLUSTRATE, and BACKGROUND.

## Relations

The relation layer was treated as an explicit knowledge object rather than implicit prose links.

## Provenance

Taxonomy Provenance, Evidence Provenance, and Generation Provenance were separated conceptually.

## Supersession

Superseded by v0.3 as provenance, traceability, and revision requirements became more explicit.
