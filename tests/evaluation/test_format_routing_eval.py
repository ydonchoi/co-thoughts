"""Regression gate for the Phase 4 keyword evaluation.

Floors are the measured values after request-cue gating (see
docs/testing/format_routing_keyword_eval_v0.1.md, section 7). They guard
against regressions; raise them when the planner improves. The held-out set
must not be used to tune rules.
"""
from collections import Counter
from pathlib import Path

import pytest

from explanation_format_router import FORMATS

from format_routing_eval import evaluate, load_cases

HERE = Path(__file__).parent
DEV_CASES = load_cases(HERE / "format_routing_eval_v0.1.json")
HOLDOUT_CASES = load_cases(HERE / "format_routing_eval_holdout_v0.1.json")
DEV = evaluate(DEV_CASES)
HOLDOUT = evaluate(HOLDOUT_CASES)
GROUPS = {"explicit", "plain", "topic", "collision", "paraphrase"}


@pytest.mark.parametrize("cases, sizes", [
    (DEV_CASES, {"explicit": 25, "plain": 14, "topic": 20, "collision": 8, "paraphrase": 10}),
    (HOLDOUT_CASES, {"explicit": 12, "plain": 5, "topic": 12, "collision": 4, "paraphrase": 5}),
])
def test_datasets_are_well_formed(cases, sizes):
    ids = [c["id"] for c in cases]
    assert len(ids) == len(set(ids))
    for case in cases:
        assert case["expected"] in FORMATS
        assert case["lang"] in {"en", "ko"}
        assert case["group"] in GROUPS
    assert Counter(c["group"] for c in cases) == sizes


def test_dev_and_holdout_ids_do_not_overlap():
    assert not {c["id"] for c in DEV_CASES} & {c["id"] for c in HOLDOUT_CASES}
    assert not {c["task"] for c in DEV_CASES} & {c["task"] for c in HOLDOUT_CASES}


@pytest.mark.parametrize("result", [DEV, HOLDOUT], ids=["dev", "holdout"])
def test_explicit_requests_and_plain_text_are_fully_correct(result):
    assert result["by_group"]["explicit"]["accuracy"] == 1.0
    assert result["by_group"]["plain"]["accuracy"] == 1.0
    assert result["wrong_media_rate"] == 0.0


def test_dev_floors_do_not_regress():
    assert DEV["overall"]["correct"] >= 67
    assert DEV["by_group"]["collision"]["correct"] >= 8
    assert DEV["by_group"]["topic"]["correct"] >= 20
    assert DEV["unnecessary_media_rate"] <= 0.0
    assert DEV["missed_media_rate"] <= 0.286


def test_holdout_floors_do_not_regress():
    assert HOLDOUT["overall"]["correct"] >= 31
    assert HOLDOUT["by_group"]["topic"]["correct"] >= 11
    assert HOLDOUT["by_group"]["collision"]["correct"] >= 3
    assert HOLDOUT["unnecessary_media_rate"] <= 0.095
    assert HOLDOUT["missed_media_rate"] <= 0.294
