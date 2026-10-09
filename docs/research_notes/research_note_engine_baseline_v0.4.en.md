# Research Note Engine v0.4 — Baseline Consolidation

Status: **BASELINE v0.4 — CONSOLIDATED**

## 1. Baseline Scope

This document consolidates T2–T13 and the current Notion/GitHub implementation state. It is the semantic baseline for the project. Historical versions remain in history and do not override this baseline.

## 2. Canonical Layer Model

### Core knowledge objects
1. Research Object
2. Claim
3. Evidence
4. Transformation Event
5. Verification
6. Relation

Conversation is the provenance origin.

### Representation
- Research Note

### Classification
- Research Purpose
- Question Operator
- Research Design
- Method
- Evidence/Source
- Knowledge Domain
- R&D Orientation
- Knowledge Product
- Document Type
- Review Type
- Synthesis Operation

### Lifecycle / provenance
- Version / Revision Event
- Branch
- Provenance

### Promotion
- D9 Candidate / D9 Promotion Gate

## 3. Core Invariants

- Conversation ≠ Knowledge Object.
- Claim ≠ Evidence.
- Source ≠ Evidence.
- Evidence ≠ Verification.
- Transformation Event ≠ Claim / Evidence / Verification.
- Research Purpose ≠ Method.
- Research Purpose ≠ Document Type.
- D9 Promotion ≠ Claim Verification.
- Persistence ≠ Verification.
- AI authorship disclosure is provenance metadata, not a knowledge object or epistemic state.

## 4. Generation and Persistence

The one-stop adapter executes generation, duplicate/consistency assessment, metadata mapping, persistence when capable, and post-write verification. It must preserve distinctions among NEW, REVISION, EXTENSION, NO_CHANGE, and BLOCKED.

A successful write is not verification. Missing objects must not be fabricated to fill templates.

## 5. AI Disclosure

Every AI-generated or AI-structured Research Note must disclose AI participation at artifact level and preserve human-review/editing provenance. Editing by a human does not erase AI-generation provenance.

## 6. Validation State

T51–T56 establish consistency of the tested disclosure and output semantics for the tested scope. Live writable Notion persistence, post-write verification, and empirical repeated/large-scale generation validation remain capability-bound or open.

---

[Korean source](research_note_engine_baseline_v0.4.md)
