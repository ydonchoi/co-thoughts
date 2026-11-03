# Adaptive Explanation Format Protocol v0.1

> Status: ACTIVE GUIDANCE / DESIGN-LEVEL  
> Applies to: co-thoughts v2.0 and project adapters using it  
> Purpose: Select suitable representation formats to improve accuracy, comprehension, and reproducibility.

## 1. Purpose and Scope

This protocol does not limit explanations to text. Depending on the task, it permits structured text, diagrams, images, interactive web pages, animations, explainer videos, and simulations, used separately or in combination.

It does not require every response to become a visual or video artifact. Format selection must consider the user's goal, conceptual complexity, temporal behavior, data type, accuracy requirements, production cost, and accessibility.

## 2. Governing Principles

1. **Purpose first:** Prioritize contribution to understanding, judgment, or action over novelty of format.
2. **Preserve accuracy:** Do not remove material conditions, exceptions, uncertainty, or counterexamples for visual simplicity.
3. **Traceability:** Visuals based on data, facts, or citations must preserve traceability to source material, reference time, transformations, and interpretation.
4. **Epistemic separation:** Visually distinguish FACT, INTERPRETATION, INFERENCE, HYPOTHESIS, and SIMULATION.
5. **Format fitness:** Prefer diagrams for static relationships, animation/video for temporal change, and interactive formats for user exploration of variables.
6. **Human agency:** Visualizations and simulations support judgment; they do not replace human authority or responsibility.
7. **Progressive disclosure:** Present the core explanation first; expose detailed evidence, procedures, and raw data when needed.
8. **Separate execution evidence:** Creating a web page, video, or simulation does not prove that it works, is integrated, or has been verified.

## 3. Format Selection

| Task characteristic | Preferred formats | Main purpose |
|---|---|---|
| Definitions, concepts, precise conditions | Structured text | Precise meaning |
| Components and static relationships | Block, architecture, or concept diagrams | Structural understanding |
| Sequences and decision branches | Flowcharts, sequence diagrams | Procedure and branching |
| Causality and competing hypotheses | Causal diagrams, claim-evidence maps | Compare relationships and arguments |
| Space, shape, and appearance | Images, maps, annotated illustrations | Visual context |
| Change or behavior over time | Animation, explainer video | Understand dynamic processes |
| User exploration of variables | Interactive web pages, dashboards | Explore conditional outcomes |
| Outcomes under assumptions | Explicit simulation | Observe conditional results |

Keep text when another format does not materially improve understanding or reliable supporting material is unavailable.

## 4. Technical Writing Rules

For complex technical, research, and operational explanations, refer to the clarity principles of aircraft maintenance manuals and ASD-STE100. This does not claim official ASD-STE100 compliance or certification.

- Put one main action or judgment in each sentence.
- Use short, direct sentences and consistent terminology.
- Define technical terms at first use.
- Separate facts, assumptions, inferences, and recommendations.
- Present procedures in order. State each step's inputs, actions, outputs, and acceptance criteria.
- Include conditions, exceptions, failure states, and recovery methods.
- Do not omit material technical details in the name of simplification.

Where useful, use this structure:

1. Purpose and scope
2. Components and terminology
3. Operating principles and data flow
4. Procedures
5. Decision criteria
6. Exceptions and failure conditions
7. Inspection and verification
8. Limitations and unknowns

## 5. Quality Rules for Visual, Interactive, and Video Outputs

### 5.1 Diagrams and Images

- Label nodes, arrows, legends, axes, units, and time ranges.
- A connector must represent a real relationship. Do not let visual placement imply causation.
- Distinguish concept diagrams, data-derived charts, and illustrative images.
- Clearly label example or synthetic data.
- Include a legend and text explanation for complex diagrams.

### 5.2 Interactive Web Pages

- Make each control's input, action, output, and initial state clear.
- State the assumptions and data on which an interaction depends.
- Provide a static summary that communicates the core content without interaction.
- Consider accessibility, keyboard use, small screens, and error states.
- Distinguish generated code, successful rendering, and verified interaction.

### 5.3 Animation and Explainer Videos

- Define the learning objective and key message first.
- Plan the scene sequence and narration.
- Do not let visual representations of time, scale, or causality imply more than the evidence supports.
- Provide captions or a transcript so the core information remains available without video.
- A generated video is an explanatory artifact, not evidence of an experiment, observation, or real system operation.

### 5.4 Simulation

- State input variables, initial conditions, assumptions, model, and output metrics.
- Do not present simulation results as observed facts or certain predictions.
- Show sensitivity, alternative conditions, and model limitations where feasible.
- Distinguish replication of an original study from simulation under hypothetical conditions.

## 6. Source and Data Preservation

For data-driven representations, record the following where available:

- Source data and source identifiers
- Collection or reference time
- Population, sample, spatial, and temporal scope
- Transformation, aggregation, and exclusion rules
- Metric definitions and units
- Visual encodings and interpretive cautions
- Indicators for unknown, missing, or estimated data

If a diagram, video, or web page presents a summary that differs from the source data, disclose the difference. Do not use visual authority to strengthen unsupported numbers or relationships.

## 7. Default Output Combinations

For complex tasks, consider these combinations:

- Technical explanation: core text + structure diagram + stepwise procedure
- Research review: claim-evidence map + verification-status table + detailed explanation
- System analysis: architecture diagram + data flow + failure and recovery procedures
- Dynamic concept: concise explanation + animation/video + transcript
- Data analysis: chart + metric definitions + source and method notes
- Conditional exploration: static baseline explanation + interactive tool + assumptions and limits

Do not generate every format at once. Select the format with the highest expected information gain first.

## 8. Non-Application and Limits

- Use concise text by default for simple fact checks, short translations, simple calculations, and casual conversation.
- Honor explicit requests for text-only output or a specific format.
- If the environment cannot produce a suitable diagram, video, or interactive artifact, state the limitation and offer a supported alternative.
- Do not present high-stakes conclusions through visuals alone. Include evidence, uncertainty, and the need for expert review where relevant.

## 9. Status and Verification

This document is a design guideline for explanation formats. Its existence does not prove that automatic runtime format selection, image/video generation, web-page execution, or explanation quality has been implemented or verified.

For each task, distinguish:

- **Selected:** Chosen representation format
- **Generated:** Artifact created
- **Rendered:** Rendering observed
- **Functionally tested:** Interaction or behavior tested
- **Source verified:** Source material checked
- **Unverified / Blocked:** Items not checked and reasons

## 10. Change Policy

This guidance does not replace co-thoughts v2.0 cognitive operations, SARA verification authority, or project-specific output schemas. Revise it based on issues demonstrated by actual use and tests.
