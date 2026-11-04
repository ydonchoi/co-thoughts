# Explanation Format Routing — Keyword Evaluation v0.1 (Phase 4)

> Status: MEASURED (in-project, author-labeled) / NOT INDEPENDENTLY VALIDATED
> Scope: candidate-format selection by `explanation_format_router` keyword matching (no host capabilities, no context signals).
> Reproduce: `PYTHONPATH=src/co_thoughts python tests/evaluation/format_routing_eval.py`
> Data: `tests/evaluation/format_routing_eval_v0.1.json` · Gate: `tests/evaluation/test_format_routing_eval.py`
> Measured at: `main` @ `1a2c2d5`

## 1. Method

- 77 tasks (45 English, 32 Korean), each labeled with the format a reader would reasonably say the task *asks for*.
- Five groups: `explicit` (format requested with a listed keyword), `plain` (no format vocabulary), `topic` (a format word is the subject, not the requested output), `collision` (known substring/phrase collisions), `paraphrase` (format requested without a listed keyword).
- Metric target: `capability_status.requested`, i.e. the candidate before capability fallback.

## 2. Results

| Group | n | Correct | Accuracy |
|---|---|---|---|
| explicit | 25 | 25 | 1.000 |
| plain | 14 | 14 | 1.000 |
| collision | 8 | 7 | 0.875 |
| topic | 20 | 2 | 0.100 |
| paraphrase | 10 | 0 | 0.000 |
| **Overall** | **77** | **48** | **0.623** |

| Rate | Value | Definition |
|---|---|---|
| Unnecessary-media rate | 0.452 (19/42) | TEXT-expected tasks given a non-TEXT candidate |
| Missed-media rate | 0.286 (10/35) | Media-expected tasks given TEXT |
| Wrong-media rate | 0.000 (0/35) | Media-expected tasks given a different media format |

Per-format precision is lowest for IMAGE (0.417) and VIDEO (0.429), driven by topic mentions such as "image compression", "brand image", "video codecs", "the movie".

## 3. Findings

1. **Explicit requests and plain text are handled correctly** (39/39). When a listed keyword is used as a request, the right format is chosen, and no format is invented for plain tasks.
2. **Topic mentions are the dominant error (18/20 wrong).** Keyword matching cannot tell "explain JPEG image compression" (TEXT) from "show an image" (IMAGE). This is a structural limit of lexical matching, not a missing keyword.
3. **Paraphrased requests are never detected (0/10).** "visualize", "photo", "clip", "tweak the parameters", "시각화", "사진" are not keywords.
4. **One exclusion-list defect:** "draws upon" is not excluded because exclusions are literal phrases ("draw upon") and do not cover inflections (C05).
5. **Fallback limits the harm.** A wrong non-TEXT candidate only becomes the primary format when the host explicitly declares that capability; otherwise it falls back to TEXT. With capable hosts, the 45% unnecessary-media rate would surface directly.

## 4. Recommendations (not implemented in this change)

- Require a request cue near the keyword (e.g. "show/draw/make/create … as/in a <format>", "~로 보여줘/그려줘/만들어줘") before selecting a non-TEXT format, to cut topic false positives.
- Make exclusions inflection-aware (apply the same suffix handling as keywords).
- Add a small paraphrase lexicon only where the cue is unambiguous ("visualize", "시각화" → DIAGRAM; "photo", "사진" → IMAGE), measured against this set.
- Prefer host-provided `output_intent.requested_format` or context signals over lexical inference wherever the host can supply them.

## 5. Limitations

- Labels are author judgments; no external annotators or inter-rater agreement.
- The same author wrote the current keyword/exclusion rules and this dataset, so the `collision` group in particular is biased toward cases the rules already handle.
- 77 cases are too few for stable per-format estimates; per-format numbers have wide uncertainty.
- Only candidate selection is measured; rendering, accessibility, and user benefit are not evaluated.

## 6. Regression gate

`tests/evaluation/test_format_routing_eval.py` enforces the floors listed in section 7.4 on both the development and held-out sets. Raise the floors when the planner improves.

## 7. Follow-up: request-cue gating

### 7.1 Change

The planner now selects a non-TEXT format from a keyword only when the wording asks for that output:

- English: a request verb (show, make, create, give, generate, render, build, produce, run, sketch, illustrate, add, display, design, record, prepare, provide, include, use, want, need, present) within 4 tokens before the keyword; or "as/in/with/into/using/via a(n) …"; or the keyword opens the task ("Diagram of …", "A video about …"); verb keywords (draw, simulate, animate) count when used as an imperative ("Draw …", "Can you simulate …").
- Korean: the keyword followed by a form particle (`로`/`으로`), or optionally one short word and an object particle and a request verb (보여, 그려, 만들, 돌려, 해줘, 생성, 띄워, 부탁, 필요, 원해).
- Exclusions are inflection-aware on the first word ("draws upon", "drawing on", "bigger picture").
- No paraphrase lexicon was added; missed-media is unchanged by design (this change targets false positives).

### 7.2 Held-out set

`tests/evaluation/format_routing_eval_holdout_v0.1.json` (38 new cases, same groups) was written and committed **before** the planner change and was not used to tune rules. Its baseline was measured on `main` @ `44b3676`.

### 7.3 Results

| Set | Metric | Before | After |
|---|---|---|---|
| Development (77) | Correct | 48 (0.623) | **67 (0.870)** |
| | Topic group | 2/20 | **20/20** |
| | Collision group | 7/8 | **8/8** |
| | Unnecessary-media rate | 0.452 | **0.000** |
| | Missed-media rate | 0.286 | 0.286 |
| Held-out (38) | Correct | 20 (0.526) | **31 (0.816)** |
| | Topic group | 1/12 | **11/12** |
| | Collision group | 2/4 | **3/4** |
| | Unnecessary-media rate | 0.619 (13/21) | **0.095 (2/21)** |
| | Missed-media rate | 0.294 (5/17) | 0.294 (5/17) |

Explicit and plain groups stay at 100% and wrong-media stays at 0 on both sets.

Remaining held-out false positives (reported, not tuned):
- HT08 "**Show that** the image of a compact set …": the mathematical idiom "show that" is read as a request verb.
- HC01 "The match ended **in a draw**": the "in a …" form cue fires on the noun "draw".

### 7.4 Gate floors

Development: correct ≥ 67, topic ≥ 20, collision ≥ 8, unnecessary-media ≤ 0.000, missed-media ≤ 0.286. Held-out: correct ≥ 31, topic ≥ 11, collision ≥ 3, unnecessary-media ≤ 0.095, missed-media ≤ 0.294. Both: explicit and plain 100%, wrong-media 0.

### 7.5 Trade-offs and limits

- Development numbers are optimistic: rules were adjusted on that set (one adjustment: "plot" was removed from the verb list after "the plot of the movie" fired). Treat the held-out numbers as the realistic estimate.
- The held-out set has the same author as the rules and the development set, so it shares the author's phrasing habits.
- Neither set contains terse, verbless requests; the leading-noun and Korean 부탁/필요/원해 cues were added after probing such cases and are pinned by unit tests. Known cost: a task that *opens* with a format word used as a topic ("Image compression in JPEG: how does it work?") is selected.
- Requests that phrase the format without a request cue or a leading noun (e.g. "Explain photosynthesis with diagrams", plural without an article) are now missed.

---

[Korean source](format_routing_keyword_eval_v0.1.md)
