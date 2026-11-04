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

Development: correct ≥ 67, topic ≥ 20, collision ≥ 8, unnecessary-media ≤ 0.000, missed-media ≤ 0.286. Held-out: correct ≥ 32, topic ≥ 12, collision ≥ 3, unnecessary-media ≤ 0.048, missed-media ≤ 0.294 (updated after section 7.6). Both: explicit and plain 100%, wrong-media 0.

### 7.5 Trade-offs and limits

- Development numbers are optimistic: rules were adjusted on that set (one adjustment: "plot" was removed from the verb list after "the plot of the movie" fired). Treat the held-out numbers as the realistic estimate.
- The held-out set has the same author as the rules and the development set, so it shares the author's phrasing habits.
- Neither set contains terse, verbless requests; the leading-noun and Korean 부탁/필요/원해 cues were added after probing such cases and are pinned by unit tests. Known cost: a task that *opens* with a format word used as a topic ("Image compression in JPEG: how does it work?") is selected.
- Requests that phrase the format without a request cue or a leading noun (e.g. "Explain photosynthesis with diagrams", plural without an article) are now missed.
### 7.6 Review follow-up (Codex on #12)

An external automated review found two cue false positives outside both sets:

- A request verb governing a different clause: "I **need to** understand video codecs", "We **need to** discuss image compression". Fix: a request verb counts only if no `to`, wh-word, `that`, or `if` lies between it and the keyword (also covers "Show **how** video codecs work").
- `in/with a …` modifying another noun: "rules in a **video game**", "in a **video codec**". Fix: the preposition form counts only when the format word heads its phrase (followed by the end, punctuation, or `of/about/that/to/for/with/…`).

After the fix: development unchanged (67/77, unnecessary-media 0.000); held-out **32/38 (0.842)**, unnecessary-media **0.048 (1/21)**, missed-media unchanged.

**Contamination note:** the clause-boundary rule also fixes held-out case HT08 ("Show **that** the image of …"), which was already known to fail when this rule was written. The rule was motivated by the reviewer's examples, not by HT08, but the held-out gain from 31 to 32 is not independent evidence. The remaining held-out false positive is HC01 ("ended in a draw;" — the noun "draw" heads its phrase and is followed by punctuation).

## 8. Follow-up: paraphrase recognition

### 8.1 Change

Paraphrase vocabulary was added to each format. Every new word goes through the same request-cue gating as section 7, except phrases that already describe an output form (self-cued).

| Format | Cue-gated words | Self-cued phrases |
|---|---|---|
| DIAGRAM | visualize/visualise/visualization, chart, graph, mind map, timeline, 시각화, 차트, 그래프, 도표, 도해, 마인드맵, 타임라인 | boxes and arrows |
| IMAGE | photo, photograph, clip art, 사진 | — |
| VIDEO | clip, screencast, 녹화, 클립 | — |
| INTERACTIVE | — | let me tweak/adjust/play with/change/vary, 바꿔가며, 바꿔볼 수 있게, 조절하면서, 조절하며, 조절할 수 있게 |
| SIMULATION | what-if, scenario analysis, 시나리오별 | model what happens |
| ANIMATION | in motion, 움직이게 | 움직이는 모습으로 |

`visualize`, `visualise`, `chart`, and `graph` also count as imperative verb keywords ("Chart the revenue …", "Graph y = x²").

### 8.2 Second held-out set

`tests/evaluation/format_routing_eval_holdout_v0.2.json` (40 cases: 20 paraphrased requests, 12 topic mentions of the new vocabulary such as "graph theory", "photo editing", "chart of accounts", 4 plain, 4 explicit) was written and committed **before** this change, with no task overlapping the other sets. Baseline on `main` @ `fa9dd95`.

### 8.3 Results

| Set | Metric | Before | After |
|---|---|---|---|
| Development (77) | Correct | 67 | 77 |
| | Paraphrase group | 0/10 | 10/10 |
| | Missed-media rate | 0.286 | 0.000 |
| Held-out v0.1 (38) | Correct | 32 | 37 |
| | Paraphrase group | 0/5 | 5/5 |
| **Held-out v0.2 (40)** | Correct | 20 (0.500) | **37 (0.925)** |
| | Paraphrase group | 0/20 | **18/20** |
| | Topic group | 12/12 | 11/12 |
| | Unnecessary-media rate | 0.000 | **0.062 (1/16)** |
| | Missed-media rate | 0.833 | **0.083** |

Explicit and plain groups stay at 100% and wrong-media stays 0 on all three sets.

**Which numbers to trust:** the vocabulary was built from the development-set paraphrase errors, so the development result is tuned; the v0.1 held-out paraphrases reuse the same words (visualize, photo, 시각화, 사진), so that gain is not independent either. Held-out v0.2 is the estimate to use: paraphrase recall rises from 0 to 0.9 at the cost of one new false positive in 16 TEXT tasks.

Remaining v0.2 errors (reported, not tuned):
- QT03 "Give me tips for **photo** editing" → IMAGE: "give" governs "tips", but the cue window does not check what the verb's object is.
- QR07 "Render a 3D **view** of the molecule" → TEXT: "view" is not in the vocabulary.
- QR10 "Give me **controls** to change gravity" → TEXT: "controls" was deliberately not added (too common as a topic).

### 8.4 Limits

- Held-out v0.2 was written by the same author, after the general direction of the vocabulary (chart/graph/photo/clip) had been chosen. Its topic group deliberately uses that vocabulary to measure false positives, but it still shares the author's phrasing.
- Self-cued phrases ("let me change", "조절하면서") select a format with no further check; a sentence like "Let me change the subject" would be selected as INTERACTIVE.
- Vocabulary is closed: new paraphrases ("render a 3D view", "controls to …") need explicit additions measured against a new held-out set.

### 8.5 Review follow-up (Codex on #13)

The Codex review of #13 completed after merge and reported three false positives outside all evaluation sets; all three reproduced on `main` @ `db02b3c` and were fixed:

- Sentence-initial `graph`/`chart` used as a subject noun ("Graph theory **is** …", "Chart **of** accounts …") was treated as an imperative → DIAGRAM. A verb keyword no longer counts as an imperative when followed by `of` or by a copula/auxiliary (is, are, was, were, has, have, can, will) within three tokens.
- `움직이게` as a causative ("힘이 물체를 움직이게 **하는 이유**") was self-cued → ANIMATION. It is no longer self-cued and now needs the Korean request-verb cue ("움직이게 **보여줘**").
- "clip art" matched VIDEO via `clip`. "clip art" is now an IMAGE keyword, and `clip` is skipped when followed by "art".

All three evaluation sets are unchanged (dev 77/77, held-out v0.1 37/38, held-out v0.2 37/40); the examples are pinned by unit tests.

---

[Korean source](format_routing_keyword_eval_v0.1.md)
