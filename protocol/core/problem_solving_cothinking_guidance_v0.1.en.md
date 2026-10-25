# Problem-Solving Co-Thinking Workflow Guidance v0.1 (provisional project term)

> Status: ACTIVE GUIDANCE CANDIDATE / DESIGN-LEVEL
> Target: co-thoughts v2.0 architecture
> Verification partner: SARA independent verification layer
> Implementation status: `cognitive_router.route_verification_domains()` provides provisional keyword-based domain hints. Claim extraction, evidence search, SARA verification, and automatic execution of the full problem-solving workflow are outside its scope.

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

### 3.0 Verification-domain routing before and after hypothesis formation

**Before** developing a concrete provisional solution, identify likely fact-verification domains from the problem statement and current premises. **After** deriving and comparing provisional solutions, re-extract the domains from the actual proposed mechanisms and claims, then add any missed domains. This initial routing prioritizes verification; it must not become a permanent restriction that excludes necessary checks.

The reference router returns domain hints from problem text and optional `proposed_solution` and caller-supplied `claims`. Domain labels are candidates and do not resolve the full meaning of the context. Claims are not extracted automatically. Domain tags, source strategies, and temporal-sensitivity signals do not indicate completed verification; all verification states remain `UNVERIFIED`. The primary domain is an estimate based on keyword-match counts and should be checked against task context.

#### A. Minimum routing output

- **Primary domain:** the one domain most directly connected to the decisive claims.
- **Secondary domains:** additional domains that can materially change judgments about legality, effect, cost, operation, or acceptability.
- **Claim units:** facts, premises, causal claims, legal/policy claims, figures, and source attributions to check within each domain.
- **Criticality:** impact of error on the conclusion or implementation, e.g. decisive / important / supporting.
- **Temporal sensitivity:** whether current law, policy, prices, statistics, or technical conditions must be checked.
- **Verification criteria and source types:** what evidence can support or challenge each claim, and how it will be independently checked.
- **Unresolved domains / hold conditions:** areas lacking accessible evidence or requiring specialist judgment.

Classify important claims rather than assigning one domain to the whole answer. A claim may span multiple domains; allow multiple tags.

#### B. Top-level routing taxonomy (provisional operational taxonomy)

The following is a **working taxonomy inspired by academic classifications**, not a verbatim adoption of any institution's official classification. Subdivide only when useful; do not investigate the full taxonomy for every task.

1. **Natural sciences:** physics, chemistry, biology, earth and environmental sciences.
2. **Medicine, health and public health:** clinical questions, epidemiology, environmental health and health risks.
3. **Engineering, technology and information science:** design, systems, technical performance, software and information systems.
4. **Mathematics, statistics and data methodology:** measurement, sampling, estimation, statistical claims and reproducibility.
5. **Social sciences:** sociology, psychology, political science, anthropology, education and related fields.
6. **Economics, business, finance and organizational management:** costs and benefits, incentives, budgets, operations and governance.
7. **Law, legal systems and regulation:** authority, statutes and rules, duties, liability, sanctions, procedure and jurisdiction.
8. **Public administration, policy and policy evaluation:** public enforcement, policy instruments, administrative procedure, effects and evaluation.
9. **Humanities, history, language and culture:** texts, concepts, historical context and interpretive accuracy.
10. **Ethics, philosophy and normative judgment:** rights, justice, legitimacy, value conflicts and responsibility.
11. **Spatial, urban, housing and environmental planning:** spatial layout, access, housing management and spatial externalities.
12. **Interdisciplinary / other specialist domains:** combinations or specialist areas outside the categories above; state the subdomain and why it matters.

Do not assume this taxonomy is exhaustive or mutually exclusive. Do not bury high-stakes constraints such as law, ethics, safety, or privacy under a primary domain; add cross-cutting tags when needed.

#### C. Domain-specific verification strategy

A domain label alone is not verification. Identify **what kind of evidence could support or challenge the claim**.

- Law and regulation: establish jurisdiction and reference date; prioritize authoritative primary sources such as current legislation, official interpretations, and case law. Do not infer legal sanctioning authority merely from the existence of a private rule.
- Medicine, health and natural sciences: match evidence type to the claim; assess systematic reviews, original studies, public-authority sources, evidence strength and applicability.
- Statistics and data: inspect source data, definitions, sampling and measurement, methods, uncertainty, and reproducibility.
- Economics, finance and operations: inspect cost components, assumptions, funding sources, recurring costs, opportunity costs, and sensitivity conditions.
- Social science, policy and education: inspect research design, population and context, alternative explanations, causal-inference limits, and external validity.
- Humanities, history and language: inspect original text, edition, context, source lineage, and the distinction between factual statement and interpretation.
- Ethics and normative claims: factual verification alone cannot settle a value conclusion. State normative premises and evaluation criteria; separately verify empirical claims embedded in them.
- Spatial, urban and housing questions: separate spatial conditions, applicable rules, exposure or movement paths, field observations, and design assumptions.

Source authority varies by domain, and one source type cannot verify every claim. Record conflicts between sources rather than averaging them away.

#### D. Efficiency and verification depth

Prioritize review using these factors together:

- **Decision impact:** would a false claim change the solution or conclusion?
- **Error cost / risk:** does it affect legal rights, health, safety, finances, or serious harm?
- **Uncertainty:** is evidence missing or conflicting?
- **Temporal sensitivity:** does it require current confirmation?
- **Verifiability / marginal cost:** can reliable evidence be checked at reasonable cost?

Review high-risk, decisive claims first even when verification is costly. For low-risk supporting claims, reduce depth or explicitly retain an unverified status. Efficiency must not justify skipping decisive legal authority, safety premises, or facts that determine the conclusion. If scoring is used, define the scale, weights, and thresholds first; do not present an unvalidated score as an empirical measure.

#### E. Two-pass routing around provisional hypotheses

1. **Pre-hypothesis scan:** examine the problem statement and key premises; identify primary/secondary domains, decisive factual claims, and high-risk constraints. Use this to plan initial verification.
2. **Derive and compare hypotheses:** propose the most defensible concrete provisional solution with current information and compare alternatives. Do not confuse proposal with completed verification.
3. **Post-hypothesis scan:** decompose claims arising from each solution's mechanism, authority, costs, predicted effects, and side effects; reassess domain tags. Expand the verification scope if a new domain or high-risk claim appears.
4. **SARA routing and iterative review:** independently review decisive claims using domain-appropriate criteria and re-verify material changes.
5. **Exit decision:** determine whether decisive claims were reviewed or the reason for non-verification is recorded. Report solution status separately from factual verification status.

The two scans do not require investigating the same sources twice. The first creates the verification plan; the second finds claims and domains introduced or exposed by the proposed solution.

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

### 6.1 On-demand workflow clusters

The runtime does not chain the full workflow automatically. The caller selects one cluster through `CognitiveRuntime.run_workflow(name, request)`: `problem_diagnosis`, `solution_design`, `feasibility_review`, or `hypothesis_delta`. Each cluster sends its related stages and existing Cognitive Operation hints in one backend call. This is a cluster-level prompt invocation, not deterministic execution of each stage or SARA verification. Pre/post domain scans remain available separately through `route_verification_domains()`.

The natural-language entry point `CognitiveRuntime.run_natural_language(request)` detects explicit Korean and English cues in the task and routes to at most one workflow. `CognitiveRouter.route()` also returns `workflow_routing` with `MATCHED`, `NO_MATCH`, or `AMBIGUOUS` and candidate names. No match uses the existing single-run path. If cues select multiple clusters, execution stops with `WORKFLOW_AMBIGUOUS`; it does not silently combine clusters or make multiple calls.

### 6.2 External-tool planning and connection boundary

`CognitiveRuntime.plan_natural_language()` and `plan_workflow_tools()` inspect tool needs, connector availability, and whether execution has occurred. Current capabilities are `web_search`, `calculator`, `data_analysis`, and `spatial_lookup`: current/high-risk/source-checking tasks route to search; numerical or cost calculations to a calculator; datasets/statistics to data analysis; and map/route/location lookups to spatial tools. A planned tool is never executed automatically.

A host registers a concrete adapter with `ToolRegistry.register(capability, adapter)` and invokes it explicitly through `CognitiveRuntime.invoke_external_tool()`. Execution requires `SafetyPolicy.allow_tool_execution=True`; adapters with external side effects separately require `allow_external_side_effects=True`. The repository does not include live search, calculator, data, or spatial service adapters or credentials. Tool output remains unverified observation data and cannot promote `verification_status` or `is_evidence`.

By default, `CognitiveRuntime` connects to the sibling SARA v2.4 `CoThoughtsSARAAdapter` and checks epistemic-state and attribution constraints on generated claims. Set `CO_THOUGHTS_SARA_V24_ROOT` to change the checkout path. This is separate from SARA v2.5 judgment/source-verification providers, which require their own configuration. Unless actual source verification runs, the status remains `UNVERIFIED`.

## Related documents

- `protocol/core/human-ai_co-thoughts_protocol_v2.0.md`
- `protocol/verification/sara_verification_output_policy_v1.0.md`
- `docs/contracts/execution_contract_v01.md`
- `docs/architecture/cognitive_runtime_safety_v01.md`
- SARA repository: `SARA_v2.4/co_thoughts_integration_contract.md`

**Confession Report:** This is design guidance based on existing operations and SARA policy. Some rules are proposals derived from one dialogue, not established academic concepts or verified general laws. Claim continuous SARA involvement only when independent execution and runtime/host integration evidence exists. Documentation alone does not prove code implementation, CI success, or performance improvement.

---

[Korean source](problem_solving_cothinking_guidance_v0.1.md)
