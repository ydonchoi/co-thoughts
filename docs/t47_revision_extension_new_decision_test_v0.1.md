# T47 — Revision / Extension / New-Note Decision Test v0.1

Status: **PASS — DECISION CONTRACT DEFINED AND CONTROLLED FIXTURES RESOLVED**

## 1. Purpose

T47 tests whether the Research Note one-stop pipeline can distinguish correctly among:

- NO_CHANGE
- REVISION
- EXTENSION
- NEW
- BLOCKED

when new conversational input is received in the context of an existing Research Note.

The objective is to prevent both:

1. unnecessary duplicate notes; and
2. destructive or epistemically unsafe overwriting of existing knowledge.

## 2. Governing Principle

A new input must first be interpreted as a change to a Research Object and its knowledge state, not as a request to create a document.

The decision sequence is:

**Existing-State Check**
→ **Research Object Identity**
→ **Question / Scope Comparison**
→ **Claim / Evidence / Transformation Impact**
→ **Lifecycle Consequence**
→ **Decision**

Document creation is therefore downstream of semantic comparison.

## 3. Decision States

### NO_CHANGE

Use when the new input does not materially change:

- Research Object;
- question or scope;
- material Claims;
- Evidence mapping;
- epistemic state;
- Transformation trace;
- relations;
- unresolved questions.

Examples:
- same conclusion restated;
- duplicate evidence already represented;
- stylistic clarification;
- no material new information.

No new note and no revision event are required.

### REVISION

Use when the input materially changes the state of an existing Research Object.

Typical triggers:

- new Evidence changes Claim support;
- contradictory Evidence changes epistemic state;
- Claim is reformulated because of new information;
- Transformation becomes invalid or requires re-analysis;
- Relation is materially qualified;
- Document Type or Research Purpose changes while the Research Object remains the same.

Revision is non-destructive.

The previous state remains queryable and a Revision Event records the transition.

### EXTENSION

Use when the Research Object remains the same but the input adds a materially new analytical component without invalidating or materially changing the existing principal conclusions.

Examples:

- new boundary condition;
- additional mechanism branch;
- new secondary analysis;
- new comparison dimension;
- additional Evidence that strengthens context without changing the Claim state.

An extension may create new Claims, Evidence, or Transformations while preserving existing state.

If the new material independently requires a question, evidence structure, conclusion, or lifecycle, EXTENSION is insufficient and the content should be split into a new Research Object.

### NEW

Use when the input represents a distinct Research Object.

Typical triggers:

- independent primary question;
- materially different purpose;
- independent evidence structure;
- independent conclusion;
- independent lifecycle;
- a new problem that cannot be represented as a bounded extension/revision of the existing object.

A related topic alone does not make an object NEW.

### BLOCKED

Use when the correct semantic decision cannot safely be made because required state is unavailable or mutation/persistence is prohibited.

Examples:

- existing note cannot be located while duplicate risk is material;
- relevant Claim/Evidence/Transformation state cannot be inspected;
- target is locked;
- required human decision is unresolved;
- repository/project state required for classification is unavailable.

BLOCKED means “do not mutate,” not “create a new note anyway.”

## 4. Decision Matrix

| Condition | Decision |
|---|---|
| No material semantic change | NO_CHANGE |
| Same Research Object + material state change | REVISION |
| Same Research Object + additive material component | EXTENSION |
| Independent Research Object | NEW |
| Safe decision/mutation impossible | BLOCKED |

Priority rule:

**BLOCKED safety condition overrides an otherwise inferred mutation decision.**

## 5. Identity Test

Research Object identity must be assessed independently of title similarity.

Compare:

1. Primary question;
2. target phenomenon/concept/problem;
3. scope/boundary;
4. purpose;
5. material conclusion structure;
6. evidence structure;
7. lifecycle dependence.

A shared keyword, person, topic, source, or document type is not sufficient for identity.

## 6. Revision vs Extension

The critical distinction is whether the new input **changes the epistemic or structural state of existing material**.

### Revision

Existing proposition:

> C1 is SUPPORTED by E1.

New input:

> E2 materially contradicts E1/C1.

Result:

- preserve C1/E1;
- create Revision Event;
- re-evaluate C1;
- possibly create revised C2;
- activate SARA.

### Extension

Existing proposition:

> C1 is SUPPORTED by E1.

New input:

> E2 adds a new boundary condition but does not alter C1 under its existing scope.

Result:

- preserve C1;
- add E2 and/or C2;
- add relevant Transformation;
- no downgrade or replacement of C1.

## 7. Extension vs New

An additive input becomes NEW when it develops an independently answerable Research Object.

Test:

> Could the added material have its own question, evidence structure, conclusion, and lifecycle without depending on the original note?

If yes, split into a new Research Object unless there is a stronger reason to retain an explicit higher-order integration.

This prevents indefinite “note accretion.”

## 8. Controlled Fixture Set

### T47-01 — Duplicate / Restatement

Existing:
C1 supported by E1.

New:
User restates the same conclusion and evidence.

Expected: **NO_CHANGE**

Reason:
No material semantic change.

Result: PASS.

### T47-02 — New Supporting Evidence

Existing:
C1 SUPPORTED by E1.

New:
E2 independently supports C1 without changing its scope or state.

Expected: **EXTENSION**

Result: PASS.

### T47-03 — Contradictory Evidence

Existing:
C1 SUPPORTED by E1.

New:
E2 materially contradicts C1.

Expected: **REVISION**

Result: PASS.

### T47-04 — New Boundary Condition

Existing:
C1 applies within scope S.

New:
Evidence shows C1 does not hold under condition B, while the original scoped conclusion remains valid.

Expected: **EXTENSION** if B is an additional bounded component; **REVISION** if the original claim scope must be changed.

Result: PASS with explicit state comparison.

### T47-05 — New Independent Question

Existing:
Question Q1 concerns mechanism X.

New:
Question Q2 concerns the long-term economic impact of X and requires a separate evidence structure.

Expected: **NEW**

Result: PASS.

### T47-06 — Related but Independent Topic

Existing:
Research Object concerns AI-assisted research writing.

New:
User asks for a separate historical analysis of university assessment policy.

Expected: **NEW**

Result: PASS.

### T47-07 — New Mechanism Branch

Existing:
C1 explains outcome Y through mechanism M1.

New:
Evidence supports an additional mechanism M2 operating under a distinct condition, without invalidating M1.

Expected: **EXTENSION** if M2 remains a bounded component of the same question; otherwise NEW.

Result: PASS with explicit boundary check.

### T47-08 — Reclassification

Existing:
Research Object remains unchanged, but new evidence shows D4 is no longer the most appropriate Document Type and D5 better represents the information structure.

Expected: **REVISION**

Result: PASS.

Document Type change is not automatically NEW.

### T47-09 — Missing Existing State

Existing note cannot be reliably located and duplicate risk is material.

Expected: **BLOCKED**

Result: PASS.

### T47-10 — Locked Persistence Target

Semantic comparison determines REVISION, but target cannot be written.

Expected:

- semantic decision: REVISION candidate;
- persistence: BLOCKED;
- no mutation.

Result: PASS.

### T47-11 — Same Topic, Independent Lifecycle

Existing:
Research Object R1.

New:
A question uses R1 as background but introduces independent evidence, conclusion, and follow-up.

Expected: **NEW**

Result: PASS.

### T47-12 — Derived Claim Re-analysis

Existing:
T1 generated C1 from E1/E2.

New:
E3 changes the validity of T1's inference.

Expected: **REVISION**

Required:
- preserve T1/C1 historically;
- create Revision Event;
- new Transformation/re-analysis as necessary;
- re-verification;
- no overwrite.

Result: PASS.

## 9. Existing-Note Consistency Algorithm

The one-stop adapter should apply the following order:

### Step A — Locate candidate existing notes

Search by Research Object identity, not merely title or keyword.

### Step B — Retrieve sufficient current state

At minimum:

- question;
- scope;
- purpose;
- document type;
- material Claims;
- relevant Evidence;
- epistemic states;
- material Transformations;
- revision state;
- relations.

### Step C — Compare semantic state

Classify differences as:

- NONE;
- ADDITIVE;
- STATE_CHANGING;
- INDEPENDENT;
- UNKNOWN.

### Step D — Map to decision

- NONE → NO_CHANGE
- ADDITIVE → EXTENSION
- STATE_CHANGING → REVISION
- INDEPENDENT → NEW
- UNKNOWN/materially unresolved → BLOCKED

### Step E — Apply mutation safety

Only after the semantic decision:

- NO_CHANGE → no mutation
- EXTENSION → additive mutation, preserving prior state
- REVISION → non-destructive revision path
- NEW → create new note only after duplicate-risk check
- BLOCKED → no mutation

## 10. Ambiguous Cases

Some inputs legitimately support more than one decision.

Examples:

- a new boundary condition may be EXTENSION or REVISION;
- a new mechanism may be EXTENSION or NEW;
- a reclassification may be REVISION or indicate an actually different Research Object.

In such cases the system must identify the discriminating condition and escalate if it cannot be resolved safely.

It must not silently choose the most convenient document operation.

## 11. Decision Precedence

When multiple conditions apply:

1. **BLOCKED safety condition**
2. **Independent Research Object → NEW**
3. **Material state change → REVISION**
4. **Bounded additive change → EXTENSION**
5. **No material change → NO_CHANGE**

The precedence is a safety-oriented operational ordering, not an epistemic hierarchy.

## 12. Traceability Requirements

Each REVISION or EXTENSION should preserve:

- affected Research Object;
- affected Claim(s);
- added/changed Evidence;
- Evidence role;
- affected Transformation(s);
- Revision Event where applicable;
- SARA status;
- provenance.

NO_CHANGE should preserve the reason for non-mutation when operational auditability requires it.

NEW should preserve relation to prior notes when they are materially related.

BLOCKED should record the missing prerequisite or safety condition.

## 13. Safety Tests

### S1 — Duplicate avoidance

No duplicate NEW creation when the existing Research Object is materially the same.

PASS.

### S2 — Non-destructive revision

No historical state overwrite.

PASS.

### S3 — No evidence inflation

New conversational assertion is not automatically Evidence.

PASS.

### S4 — No epistemic upgrade

Additional input does not automatically make a Claim VERIFIED.

PASS.

### S5 — Persistence separation

A successful save/update does not determine the semantic decision or verification state.

PASS.

### S6 — Locked target

No lock bypass.

PASS.

### S7 — Stale state

A stale manifest cannot override fresh existing state.

PASS.

### S8 — Independent object protection

Related subject matter cannot force an additive mutation when an independent lifecycle exists.

PASS.

## 14. Result

**T47 = PASS**

The controlled fixtures establish a coherent decision contract for:

- NO_CHANGE;
- REVISION;
- EXTENSION;
- NEW;
- BLOCKED.

The key boundary is:

> **Revision changes existing state; Extension adds bounded material without changing existing principal state; New creates an independent Research Object; Blocked prevents unsafe mutation when required state or authority is unavailable.**

## 15. Validation Boundary

T47 is a controlled semantic decision test.

It does not yet establish empirical accuracy across a large corpus of real conversations.

Remaining validation:

1. repeated real-conversation decision cases;
2. false-NEW / false-REVISION / false-EXTENSION rates;
3. human agreement on ambiguous cases;
4. interaction with Branch/Merge;
5. D9 integration;
6. live Notion persistence after writable capability is restored.

## 16. Architecture Decision

**RETAIN CURRENT CORE MODEL AND ONE-STOP CONTRACT.**

No new Research Object type, Document Type, or Notion database is justified.

The decision is an orchestration state over existing objects and lifecycle semantics.

## 17. Next Test

**T48 — Branch / Merge / Revision Decision Interaction Test**

T48 should test whether NEW / REVISION / EXTENSION decisions remain coherent when multiple branches of an existing Research Object diverge and are later reconciled or preserved as conflict.

## 18. Boundary

This is a project-level operational test and specification. It is not an established academic or industry standard.

Human remains final epistemic decision authority.
