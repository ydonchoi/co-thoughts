# Explanation Format Routing — Independent Evaluation Guidelines v0.1

> Status: PROTOCOL (dataset not yet created)
> Purpose: build an evaluation set for explanation-format selection that is **independent of the author of the routing rules**.
> Annotator: an annotator other than the rule author (planned: Codex), with a human-adjudicated sample.

## 1. Why this exists

All earlier evaluation sets (`tests/evaluation/format_routing_eval_*.json`) and their labels were written by the same author as the routing rules, so their scores are optimistic. This protocol defines a set written and labeled by someone else, frozen before it is ever run.

## 2. Independence rules (must be followed by the annotator)

The annotator **must not open or rely on** any of the following while writing tasks or labels:

- `src/co_thoughts/explanation_format_router.py` and any other routing code
- `tests/evaluation/` (existing datasets, evaluator, gates)
- `tests/unit/test_explanation_format_router.py`
- `docs/testing/format_routing_keyword_eval_v0.1*.md`
- Sections 7, 9, 12, and 13 of `docs/architecture/adaptive_explanation_router_integration_v0.1*.md`

The task is to describe how **people** would phrase requests, not to probe or avoid any particular implementation. Do not run the router. This rule can only be instructed, not enforced; the provenance file records that it was given.

## 3. What a label means

Each task is a single user message to an assistant. The label is the **one output format the user is asking the assistant to produce**, judged by a careful human reader:

| Label | Use when the user asks for… |
|---|---|
| TEXT | a written answer only (explanations, summaries, lists, tables, translations, code, calculations), or the request does not ask for any visual/media output |
| DIAGRAM | a structural visual: flowchart, architecture/relationship/concept diagram, chart, graph, timeline, mind map, boxes-and-arrows |
| IMAGE | a picture/illustration/photo of how something looks |
| ANIMATION | a moving visual showing change over time (no narration required) |
| VIDEO | a video/clip/recording, typically narrated or filmed |
| INTERACTIVE | something the user can manipulate (sliders, controls, change a value and see the effect) |
| SIMULATION | running a model/scenarios to compute outcomes under assumptions |

Decision rules:

1. **Requested output, not topic.** A media word used only as the subject ("explain how video codecs work", "history of animation", "what is graph theory") is **TEXT**.
2. **Explicit beats implicit.** If the user names a format, label that format even if another would suit the topic better.
3. **One label.** If several formats are requested, label the **primary** one the user most clearly wants as the deliverable; if truly tied, label the first one mentioned and mark `ambiguous: true`.
4. **Questions about tools or methods are TEXT.** "Which program draws flowcharts?", "How do I make a video?" ask for information, not the output.
5. **Do not label by usefulness.** Do not choose a visual just because it would help; label what is asked.
6. **Ambiguity is allowed but flagged.** If a careful reader could reasonably disagree, keep the case, choose the most likely label, and set `ambiguous: true` with a one-line `note`.

## 4. Composition

80 tasks: 40 English (`lang: "en"`), 40 Korean (`lang: "ko"`), each language with:

| Group | Per language | Description |
|---|---|---|
| `explicit` | 7 | format requested with ordinary wording ("make a flowchart …", "흐름도로 보여줘") |
| `paraphrase` | 7 | format requested without the usual format noun ("visualize …", "let me play with …", "사진", "직접 바꿔 보게") |
| `terse` | 5 | very short or verbless requests ("Diagram of X, please", "구조도 부탁") |
| `plain` | 7 | ordinary text tasks with no media vocabulary |
| `topic` | 8 | media words used only as the topic, including questions about tools/methods |
| `mixed` | 6 | multiple formats, conditions, follow-ups ("…after drawing it, explain…", "그린 다음 설명해줘"), or tasks combining a request with an explanation |

Across the set, cover all seven labels at least 3 times each. Use realistic, varied phrasing (polite/casual, typos are fine occasionally, domain variety: science, business, software, everyday life). Avoid near-duplicates.

## 5. Files to produce (two files, so a second annotator can label blind)

`tests/evaluation/independent_v0.1/tasks.json`:

```json
{
  "version": "independent-0.1",
  "cases": [
    {"id": "I001", "lang": "en", "group": "explicit", "task": "…"}
  ]
}
```

`tests/evaluation/independent_v0.1/labels_annotator_a.json`:

```json
{
  "version": "independent-0.1",
  "annotator": "codex",
  "labels": [
    {"id": "I001", "expected": "DIAGRAM", "ambiguous": false, "note": ""}
  ]
}
```

`tests/evaluation/independent_v0.1/PROVENANCE.md`: who/what wrote the files, the date, the model if known, and a statement of whether the files in section 2 were opened.

IDs `I001`–`I080`, unique; every `id` in `labels_annotator_a.json` must exist in `tasks.json` and vice versa. Do not modify any other file.

## 6. What happens next (not the annotator's job)

1. The files are committed and frozen before the router is run on them.
2. A second annotator (the rule author) labels `tasks.json` **without opening** `labels_annotator_a.json`, into `labels_annotator_b.json`.
3. Agreement (Cohen's kappa) is computed; disagreements plus a random sample of 20–30 cases are adjudicated by a human (project owner) into `labels_adjudicated.json`.
4. The router is evaluated against annotator A, annotator B, and the adjudicated sample, reported separately. Results are labeled "cross-model evaluation with a human-adjudicated sample", not as a human-validated benchmark.

---

[Korean source](format_routing_independent_eval_guidelines_v0.1.md)
