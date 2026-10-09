# T47 — Revision / Extension / New-Note Decision Test v0.1

Status: **PASS — DECISION CONTRACT DEFINED AND CONTROLLED FIXTURES RESOLVED**

## 1. Purpose
T47 tests whether the Research Note one-stop pipeline distinguishes among NO_CHANGE, REVISION, EXTENSION, NEW, and BLOCKED when new conversational input arrives in the context of an existing Research Note.

The objective is to prevent unnecessary duplicate notes and destructive or epistemically unsafe overwriting of existing knowledge.

## 2. Governing Principle
Interpret new input first as a change to a Research Object and its knowledge state, not as a request to create a document.

Decision sequence:

**Existing-State Check → Research Object Identity → Question / Scope Comparison → Claim / Evidence / Transformation Impact → Lifecycle Consequence → Decision**

Document creation is downstream of semantic comparison.

## 3. Decision States

### NO_CHANGE
Use when the new input does not materially change the Research Object, question/scope, material Claims, Evidence mapping, epistemic state, Transformation trace, relations, or unresolved questions.

Examples: same conclusion restated; duplicate Evidence already represented; stylistic clarification; no material new information.

No new note or Revision Event is required.

### REVISION
Use when input materially changes the state of an existing Research Object.

Typical triggers:
- new Evidence changes Claim support;
- contradictory Evidence changes epistemic state;
- a Claim is reformulated due to new information;
- a Transformation becomes invalid or requires re-analysis;
- a Relation is materially qualified;
- Document Type or Research Purpose changes while the Research Object remains the same.

Revision is non-destructive. Previous state remains queryable and a Revision Event records the transition.

### EXTENSION
Use when the Research Object remains the same but the input adds a materially new analytical component without invalidating or materially changing the existing principal conclusions.

Examples: new boundary condition; additional mechanism branch; secondary analysis; comparison dimension; additional Evidence that strengthens context without changing Claim state.

An extension may add Claims, Evidence, or Transformations while preserving existing state.

If the material independently requires a question, evidence structure, conclusion, or lifecycle, EXTENSION is insufficient; split it into a new Research Object.

### NEW
Use when the input represents a distinct Research Object.

Typical triggers: independent primary question; materially different purpose; independent evidence structure or conclusion; independent lifecycle; new problem not representable as a bounded extension/revision of the existing object.

A related topic alone does not make an object NEW.

### BLOCKED
Use when the semantic decision cannot safely be made because required state is unavailable or mutation/persistence is prohibited.

Examples:
- existing note cannot be located while duplicate risk is material;
- relevant Claim/Evidence/Transformation state cannot be inspected;
- target is locked;
- required human decision remains unresolved;
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

Priority rule: **a BLOCKED safety condition overrides an otherwise inferred mutation decision.**

## 5. Identity Test
Assess Research Object identity independently of title similarity. Compare:
1. Primary question;
2. target phenomenon/concept/problem;
3. scope/boundary;
4. purpose;
5. material conclusion structure;
6. evidence structure;
7. lifecycle dependence.

A shared keyword, person, topic, source, or Document Type is not sufficient for identity.

## 6. Revision vs Extension
The critical distinction is whether the new input **changes the epistemic or structural state of existing material**.

**Revision example:** Existing C1 is SUPPORTED by E1; new E2 materially contradicts E1/C1. Preserve C1/E1, create Revision Event, re-evaluate C1, possibly create revised C2, and activate SARA.

**Extension example:** Existing C1 is SUPPORTED by E1; new E2 adds a boundary condition but does not alter C1 within its existing scope. Preserve C1, add E2 and/or C2 and relevant Transformations, without downgrading or replacing C1.

## 7. Extension vs New
An additive input becomes NEW when it develops an independently answerable Research Object.

Test: **Could the added material have its own question, evidence structure, conclusion, and lifecycle without depending on the original note?**

If yes, split it into a new Research Object unless there is a stronger reason to retain an explicit higher-order integration. This prevents indefinite “note accretion.”

## 8. Controlled Fixture Set
- **T47-01 — Duplicate / Restatement:** Same conclusion and Evidence repeated. Expected NO_CHANGE. PASS.
- **T47-02 — New Supporting Evidence:** E2 independently supports C1 without changing scope/state. Expected EXTENSION. PASS.
- **T47-03 — Contradictory Evidence:** E2 materially contradicts C1. Expected REVISION. PASS.
- **T47-04 — New Boundary Condition:** C1 applies within S; Evidence indicates it does not hold under B while original scoped conclusion remains valid. EXTENSION if B is an additive bounded component; REVISION if original scope must change. PASS with explicit state comparison.
- **T47-05 — New Independent Question:** Existing Q1 concerns mechanism X; new Q2 concerns X's long-term economic impact and needs a separate evidence structure. Expected NEW. PASS.
- **T47-06 — Related but Independent Topic:** Existing note concerns AI-assisted research writing; new request analyzes university assessment policy separately. Expected NEW. PASS.
- **T47-07 — New Mechanism Branch:** C1 explains Y through M1; new Evidence supports M2 under a distinct condition without invalidating M1. EXTENSION if still bounded within the same question; otherwise NEW. PASS with explicit boundary check.
- **T47-08 — Reclassification:** Same Research Object, but new Evidence makes D5 a better representation than D4. Expected REVISION. PASS. A Document Type change does not automatically mean NEW.
- **T47-09 — Missing Existing State:** Existing note cannot be reliably located while duplicate risk is material. Expected BLOCKED. PASS.
- **T47-10 — Locked Persistence Target:** Semantic decision is REVISION but target cannot be written. Semantic decision: REVISION candidate; persistence: BLOCKED; no mutation. PASS.
- **T47-11 — Same Topic, Independent Lifecycle:** New question uses R1 as background but introduces independent evidence, conclusion, and follow-up. Expected NEW. PASS.
- **T47-12 — Derived Claim Re-analysis:** E3 changes validity of a T1 inference that produced C1 from E1/E2. Expected REVISION; preserve T1/C1, create Revision Event and re-analysis as necessary, re-verify, do not overwrite. PASS.

## 9. Existing-Note Consistency Algorithm

### Step A — Locate candidate notes
Search by Research Object identity, not just title or keyword.

### Step B — Retrieve sufficient current state
At minimum: question, scope, purpose, Document Type, material Claims, relevant Evidence, epistemic states, material Transformations, revision state, and relations.

### Step C — Compare semantic state
Classify differences as NONE, ADDITIVE, STATE_CHANGING, INDEPENDENT, or UNKNOWN.

### Step D — Map to decision
- NONE → NO_CHANGE
- ADDITIVE → EXTENSION
- STATE_CHANGING → REVISION
- INDEPENDENT → NEW
- UNKNOWN/materially unresolved → BLOCKED

### Step E — Apply mutation safety
- NO_CHANGE → no mutation
- EXTENSION → additive mutation preserving prior state
- REVISION → non-destructive revision path
- NEW → create only after duplicate-risk check
- BLOCKED → no mutation

## 10. Ambiguous Cases
Some inputs legitimately support more than one decision: a new boundary condition may be EXTENSION or REVISION; a new mechanism may be EXTENSION or NEW; a reclassification may be REVISION or may reveal a different Research Object.

Identify the discriminating condition and escalate if it cannot be resolved safely. Do not silently choose the most convenient document operation.

## 11. Decision Precedence
When multiple conditions apply:
1. **BLOCKED safety condition**
2. **Independent Research Object → NEW**
3. **Material state change → REVISION**
4. **Bounded additive change → EXTENSION**
5. **No material change → NO_CHANGE**

This is a safety-oriented operational ordering, not an epistemic hierarchy.

## 12. Traceability Requirements
Each REVISION or EXTENSION should preserve the affected Research Object, affected Claims, added/changed Evidence and role, affected Transformations, Revision Event where applicable, SARA status, and provenance.

- NO_CHANGE should preserve the reason for non-mutation when needed for auditability.
- NEW should preserve relations to prior notes when materially related.
- BLOCKED should record the missing prerequisite or safety condition.

## 13. Safety Tests
- S1 Duplicate avoidance: no duplicate NEW when Research Object is materially the same. **PASS.**
- S2 Non-destructive revision: no historical state overwrite. **PASS.**
- S3 No Evidence inflation: a conversational assertion is not automatically Evidence. **PASS.**
- S4 No epistemic upgrade: additional input does not automatically make a Claim VERIFIED. **PASS.**
- S5 Persistence separation: saving/updating does not determine the semantic decision or verification state. **PASS.**
- S6 Locked target: no lock bypass. **PASS.**
- S7 Stale state: stale manifest cannot override fresh existing state. **PASS.**
- S8 Independent object protection: related subject matter cannot force an additive mutation when an independent lifecycle exists. **PASS.**

## 14. Result
**T47 = PASS**

The controlled fixtures establish a coherent decision contract for NO_CHANGE, REVISION, EXTENSION, NEW, and BLOCKED.

> **Revision changes existing state; Extension adds bounded material without changing existing principal state; New creates an independent Research Object; Blocked prevents unsafe mutation when required state or authority is unavailable.**

## 15. Validation Boundary
T47 is a controlled semantic decision test; it does not establish empirical accuracy across a large corpus of real conversations.

Remaining validation:
1. repeated real-conversation decision cases;
2. false-NEW / false-REVISION / false-EXTENSION rates;
3. human agreement on ambiguous cases;
4. interaction with Branch/Merge;
5. D9 integration;
6. live Notion persistence after writable capability is restored.

## 16. Architecture Decision
**RETAIN CURRENT CORE MODEL AND ONE-STOP CONTRACT.**

No new Research Object type, Document Type, or Notion database is justified. The decision is an orchestration state over existing objects and lifecycle semantics.

## 17. Next Test
**T48 — Branch / Merge / Revision Decision Interaction Test**

T48 should test whether NEW / REVISION / EXTENSION decisions remain coherent when multiple branches of an existing Research Object diverge and are later reconciled or retained as conflict.

## 18. Boundary
This is a project-level operational test and specification, not an established academic or industry standard. The human remains the final epistemic decision authority.

---

[Korean source](t47_revision_extension_new_decision_test_v0.1.md)
