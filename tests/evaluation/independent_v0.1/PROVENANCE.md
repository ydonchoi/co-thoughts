# Provenance

- Author: Codex
- Date: 2026-11-04 (Asia/Seoul)
- Model: GPT-6 (Codex agent)
- Files opened during this task:
  - `docs/testing/format_routing_independent_eval_guidelines_v0.1.en.md`
- Section-2 files opened: No. No files listed in section 2 were opened.
- Source of the guideline (corrected 2026-11-04): Codex reported reading the English guideline from `ydonchoi/co-thoughts` on GitHub (`main` branch) because its local checkout did not contain it. The same file is tracked in this repository at this PR's base commit `f56761e`; the original wording "absent from the local workspace" refers to Codex's own checkout, not to the repository. Which exact revision Codex read was not recorded. No other repository files were opened, per Codex's report.

## Corrections after annotation

- 2026-11-04, by Claude (the routing-rule author and planned annotator B), at the project owner's request, in response to Codex review findings on PR #23:
  - **I079** was tagged `lang: "ko"` but its task text was English: "Run best-case and worst-case cost scenarios, then calculate the average cost." It was replaced with a Korean request of the same meaning: "최선의 경우랑 최악의 경우 비용 시나리오를 돌려 보고, 그다음 평균 비용을 계산해줘." `lang`, `group`, and the 40 en / 40 ko balance are unchanged.
  - The I079 label in `labels_annotator_a.json` was **not changed and not viewed**; the translation is intended to preserve the requested output.
  - Independence note: this one task's wording was written by the rule author. Analyses may exclude I079 or report results with and without it.
  - The guideline-source line above was clarified; no other content was changed.
