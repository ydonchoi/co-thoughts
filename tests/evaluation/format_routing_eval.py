"""Evaluate keyword-based explanation-format candidate selection (Phase 4).

Measures the planner's *candidate* format (``capability_status.requested``),
which is what keyword matching decides; host capabilities are deliberately not
involved. Run directly for a report:

    PYTHONPATH=src/co_thoughts python tests/evaluation/format_routing_eval.py
"""
from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from explanation_format_router import FORMATS, route_explanation_format

DATASET = Path(__file__).with_name("format_routing_eval_v0.1.json")


def load_cases(path: Path = DATASET) -> list[dict[str, Any]]:
    return json.loads(path.read_text(encoding="utf-8"))["cases"]


def predict(task: str) -> str:
    return route_explanation_format({"task": task})["capability_status"]["requested"][0]


def evaluate(cases: list[dict[str, Any]]) -> dict[str, Any]:
    rows = [{**case, "predicted": predict(case["task"])} for case in cases]
    for row in rows:
        row["correct"] = row["predicted"] == row["expected"]

    def rate(selected: list[dict[str, Any]]) -> dict[str, Any]:
        n = len(selected)
        hits = sum(r["correct"] for r in selected)
        return {"n": n, "correct": hits, "accuracy": round(hits / n, 3) if n else None}

    by_group = {g: rate([r for r in rows if r["group"] == g]) for g in sorted({r["group"] for r in rows})}
    by_lang = {l: rate([r for r in rows if r["lang"] == l]) for l in sorted({r["lang"] for r in rows})}

    text_expected = [r for r in rows if r["expected"] == "TEXT"]
    media_expected = [r for r in rows if r["expected"] != "TEXT"]
    unnecessary_media = [r for r in text_expected if r["predicted"] != "TEXT"]
    missed_media = [r for r in media_expected if r["predicted"] == "TEXT"]
    wrong_media = [r for r in media_expected if r["predicted"] not in ("TEXT", r["expected"])]

    per_format: dict[str, dict[str, Any]] = {}
    for fmt in sorted(FORMATS):
        tp = sum(r["predicted"] == fmt and r["expected"] == fmt for r in rows)
        fp = sum(r["predicted"] == fmt and r["expected"] != fmt for r in rows)
        fn = sum(r["predicted"] != fmt and r["expected"] == fmt for r in rows)
        per_format[fmt] = {
            "tp": tp, "fp": fp, "fn": fn,
            "precision": round(tp / (tp + fp), 3) if tp + fp else None,
            "recall": round(tp / (tp + fn), 3) if tp + fn else None,
        }

    confusion: dict[str, Counter] = defaultdict(Counter)
    for r in rows:
        confusion[r["expected"]][r["predicted"]] += 1

    return {
        "overall": rate(rows),
        "by_group": by_group,
        "by_lang": by_lang,
        "unnecessary_media_rate": round(len(unnecessary_media) / len(text_expected), 3),
        "missed_media_rate": round(len(missed_media) / len(media_expected), 3),
        "wrong_media_rate": round(len(wrong_media) / len(media_expected), 3),
        "per_format": per_format,
        "confusion": {k: dict(v) for k, v in sorted(confusion.items())},
        "errors": [
            {k: r[k] for k in ("id", "group", "lang", "task", "expected", "predicted")}
            for r in rows if not r["correct"]
        ],
    }


def main() -> None:
    print(json.dumps(evaluate(load_cases()), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
