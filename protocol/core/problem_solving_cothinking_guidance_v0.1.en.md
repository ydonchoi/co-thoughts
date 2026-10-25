# Problem-Solving Co-Thinking Workflow Guidance v0.1 (provisional project term)

> Status: ACTIVE GUIDANCE CANDIDATE / DESIGN-LEVEL
> Target: co-thoughts v2.0 architecture
> Verification partner: SARA independent verification layer

This guidance connects existing co-thoughts operations for complex problem-solving tasks. It does not replace EXPLORE, EXAMINE, COUNTER, COMPETE, VERIFY, SYNTHESIZE, or REVISE, and does not absorb SARA's verification authority. This document alone does not prove runtime implementation or continuous execution of SARA.

## 1. Purpose and rationale

The dialogue review identified five candidate improvements: (1) connect structural problem framing and competing causal hypotheses to solution selection; (2) when a provisional solution is requested, avoid deferring a concrete proposal solely because prior review is needed; (3) evaluate feasibility across legal authority, funding, operating conditions, side effects, acceptability, and measurement; (4) compare user and AI hypotheses to find missing variables and complementary strengths; and (5) keep factual classification and verification involved as relevant claims and solutions are generated or revised. These are design candidates, not defects proven across multiple independent cases.

## 2. Core invariants

- Human Agency: final value choices, approval, and responsibility remain with the human.
- Anti-Sycophancy: assess user and AI hypotheses by the same evidence, premise, and counterexample standards.
- Epistemic Separation: distinguish FACT, VALUE/JUDGMENT, INTERPRETATION, INFERENCE, HYPOTHESIS, and SIMULATION. VALUE/JUDGMENT is a separate analysis tag, not a change to the v2.0 Epistemic Type schema.
- Independent Verification: agreement, self-assessment, code execution, and document persistence do not substitute for SARA verification.
- Always-on Verification, Progressive Disclosure: review relevant claims throughout the task; expose critical warnings in the summary and provide deeper audit when needed.
- Provisional Actionability: when asked for a provisional solution, give a concrete defensible proposal with uncertainty and verification needs stated.
- Feasibility Is Not Truth: factual validity, logical validity, value justification, feasibility, and final decision are distinct.
- Revision over Consistency: update or downgrade claims when new evidence, counterexamples, or constraints emerge.
- No Mandatory Full Pipeline: select only the operations needed for the task.

## 3. Problem-solving workflow

~~~text
TASK DIAGNOSIS → PROBLEM FRAMING → COMPETING CAUSAL HYPOTHESES
→ STAKEHOLDER / FRAME ANALYSIS → FACT / VALUE / INFERENCE SEPARATION
→ PROVISIONAL SOLUTION HYPOTHESIS → FEASIBILITY / CONSEQUENCE EVALUATION
→ SARA INDEPENDENT VERIFICATION (repeated at relevant stages)
→ SYNTHESIS / REVISION → HUMAN–AI HYPOTHESIS DELTA
→ REVISE / CHECKPOINT / CONTINUE / STOP
~~~

This is a state-based conceptual path, not a fixed linear pipeline. SARA's review is not confined to the final step; it recurs for relevant claims, premises, sources, solutions, and revisions.

### 3.1 Problem framing

Preserve the user's original problem statement. Separate symptoms, core problem, possible causes, affected parties, and target state. State relevant boundaries: subject, place, time, jurisdiction, affected groups, and decision authority. Consider alternative framings when they could change the solution. Distinguish observed facts from model interpretation.

### 3.2 Competing causal hypotheses

Generate competing explanations rather than prematurely selecting one cause. For each, record explanatory scope, premises, counterexamples, and observations that could distinguish it. Do not state unestablished causality as fact. Stop adding hypotheses when they add no material explanatory or decision value.

### 3.3 Stakeholder and frame analysis

Compare goals, concerns, benefits, burdens, risks, rights, authority, duties, constraints, incentives, and acceptance conditions. Perspective symmetry does not imply symmetry of rights, responsibility, harm, or evidence.

### 3.4 Fact, value, and inference separation

Classify key statements as FACT, VALUE/JUDGMENT, INTERPRETATION, INFERENCE, HYPOTHESIS, or SIMULATION. This does not change the formal v2.0 epistemic schema; VALUE/JUDGMENT remains a separate analysis tag. Split mixed statements into important subclaims and record evidence or justification criteria, status, and uncertainty.

### 3.5 Provisional solution hypothesis

When a solution or recommendation is requested: (1) provide the most concrete proposal defensible with current information; (2) explain its goal, mechanism, conditions, and expected effects; (3) state unverified premises, risks, failure paths, and alternatives; (4) do not present unverified law, figures, or causality as fact; and (5) distinguish proposing a provisional solution from authorizing implementation. Suggested form: “Given current information, the provisional solution is A. B and C remain unverified, and D must be checked before implementation.”

### 3.6 Feasibility and consequences

Assess each solution for: effect and measurement; legal/institutional authority; initial and recurring costs and lawful, sustainable funding; operational requirements; side effects and displacement; acceptability and distribution of burdens; baseline, outcome indicators, review timing, and revision path. Hard constraints such as legality cannot be offset by a weighted sum of other benefits. If a necessary condition is unconfirmed, mark the proposal conditional, requiring review, or blocked.

### 3.7 Human–AI hypothesis delta

Preserve both hypotheses and their scope. Identify common ground, material differences, incompatible assumptions, different decision criteria, and variables or risks appearing in only one. Evaluate by evidence and reasoning, not authorship. Identify what both sides missed, combine complementary strengths where justified, and record candidate reusable rules without automatically making every conversation a permanent rule. Differences between hypotheses are not themselves evidence; new factual claims remain subject to SARA review.

## 4. SARA independent and continuing verification

### 4.1 Independence boundary

Co-thoughts handles framing, hypothesis generation, solution construction, and synthesis. SARA independently assesses Claims, Premises, Evidence, Sources, and Inferences. Newly created or revised factual, causal, legal/policy, numerical, attribution, and predicted-effect claims should be routed for review as needed. Agreement, prior summaries, code execution, and successful saving must not raise verification status. If SARA or required source access was not actually invoked, report NOT RUN, UNVERIFIED, or BLOCKED as appropriate. “Continuing involvement” is a protocol requirement; automatic background execution requires runtime integration and execution-log evidence.

### 4.2 Review triggers

Review externally checkable facts; current law, rules, authority, costs, statistics, dates, and figures; causality and predicted effects; important source attributions or source conflicts; facts that determine legality or feasibility; material counterevidence; and attempts to promote a provisional hypothesis to a stronger conclusion. Pure value preferences are not fact claims, but factual premises embedded in value judgments should be checked.

### 4.3 Verification loop

~~~text
CLAIM / PREMISE / SOURCE / SOLUTION HYPOTHESIS
→ CLASSIFY → ALIGN EVIDENCE → SARA ASSESSMENT
→ DETECT ISSUE / CONFLICT / UNCERTAINTY
→ REVISE OR QUALIFY → RE-VERIFY MATERIAL CHANGES
→ RECORD STATE / PROVENANCE → CONTINUE / STOP / HUMAN DECISION
~~~

Do not verify only at the end. Re-review material claims in problem framing, causal hypotheses, solution feasibility, and revisions. Do not automatically reuse verification if scope, time, subject, or causal strength changes.

### 4.4 State and output separation

Follow the existing verification-output policy; do not duplicate a separate SARA section by default. Surface critical unverified facts, source conflicts, misattribution, unconfirmed authority, and claims stronger than their evidence. Keep execution state, verification state, and solution state separate. Solution labels such as PROVISIONAL, CONDITIONAL, BLOCKED, or READY FOR HUMAN DECISION are work labels, not SARA verification states or new runtime enums.

### 4.5 Provenance

Where possible, record claim/premise reference, type and scope, source/evidence references and their relation, verifier/version/execution state/result, uncertainty and unresolved conflicts, changes after verification, and need for re-verification. Logs and checkpoints are workflow history, not evidence. Never claim logs exist if they were not captured.

## 5. Stage mapping

| Stage | Existing concept | Enhancement | Verification boundary |
|---|---|---|---|
| Problem framing | Task Diagnosis, EXPLORE | Preserve original; specify scope and alternatives | Separate fact from interpretation |
| Competing causes | COMPETE, COUNTER, EXAMINE | Record premises, scope, counterexamples | Review causal claims as hypothesis/inference |
| Stakeholders | WIDTH, RELATE, ALTERNATIVE | Compare rights, burdens, incentives, acceptance | Do not equate symmetric perspectives with equal rights/evidence |
| Fact/value/inference | Epistemic State, Premise Ledger | Separate VALUE/JUDGMENT tag | Verify facts; disclose value justification |
| Provisional solution | SYNTHESIZE, HYPOTHESIS, ALTERNATIVE | Concrete option plus uncertainty when requested | Do not assert unverified facts |
| Feasibility | EXAMINE, VERIFY, Project Adapter | Assess authority, funding, operation, harms, metrics | SARA reviews critical premises |
| User–AI comparison | REVISION, AGREEMENT, CHECKPOINT | Record differences and omissions | Agreement is not evidence |
| Revision | SARA Dual Gate, REVISE, Provenance | Re-review relevant stages and material changes | Separate verification, execution, solution states |

## 6. Routing and stopping

FAST tasks should not be forced through the full workflow. MIXED and DEEP select needed stages. If a provisional solution is explicitly requested, SYNTHESIZE should produce a defensible proposal rather than merely repeat analysis. Do not skip SARA review when legal, financial, safety, or rights constraints determine the outcome; if unavailable, state uncertainty or BLOCKED. The deterministic keyword router alone does not prove semantic compliance; host behavior requires separate tests.

Stop or move to human decision when a concrete provisional answer and its unknowns are clear; critical claims were reviewed or inability is recorded; a hard condition is unmet; further operations add little information; or value/evidence conflicts require human judgment. Do not wait for all uncertainty to disappear, and do not confuse a provisional proposal with approval or proven effectiveness.

## 7. Test candidates and status

Test candidates (not passing results): concrete provisional response; fact/inference separation; SARA independence; re-verification after material change; hard-constraint gate; side-effect/displacement analysis; hypothesis-delta quality; human agency; state consistency; and avoidance of unnecessary complexity. Use fixed cases with explicit expected outcomes where possible. Do not report accuracy/recall without defined labels and denominators. Synthetic test success alone does not prove real-world reasoning quality or continuous production SARA involvement.

Status remains ACTIVE GUIDANCE CANDIDATE / DESIGN-LEVEL. Do not change the canonical v2.0 architecture or SARA state schema here. Runtime operations, enums, schemas, and automation require separate compatibility design and tests. Consider formal promotion only after repeated cases, regression tests, SARA independence, and provenance boundaries are validated.

## Related documents

- `protocol/core/human-ai_co-thoughts_protocol_v2.0.md`
- `protocol/verification/sara_verification_output_policy_v1.0.md`
- `docs/contracts/execution_contract_v01.md`
- `docs/architecture/cognitive_runtime_safety_v01.md`
- SARA repository: `SARA_v2.4/co_thoughts_integration_contract.md`

**Confession Report:** This is design guidance based on existing operations and SARA policy. Some rules are proposals derived from one dialogue, not established academic concepts or verified general laws. Claim continuous SARA involvement only when independent execution and runtime/host integration evidence exists. Documentation alone does not prove code implementation, CI success, or performance improvement.

---

[Korean source](problem_solving_cothinking_guidance_v0.1.md)
