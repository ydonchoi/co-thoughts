"""Regression gate for the Phase 4 keyword evaluation.

Floors are the measured values after request-cue gating and paraphrase
recognition, and self-cue context checks (see
docs/testing/format_routing_keyword_eval_v0.1.md, sections 7-9). They guard
against regressions; raise them when the planner improves. The held-out sets
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
HOLDOUT2_CASES = load_cases(HERE / "format_routing_eval_holdout_v0.2.json")
HOLDOUT3_CASES = load_cases(HERE / "format_routing_eval_holdout_v0.3.json")
DEV = evaluate(DEV_CASES)
HOLDOUT = evaluate(HOLDOUT_CASES)
HOLDOUT2 = evaluate(HOLDOUT2_CASES)
HOLDOUT3 = evaluate(HOLDOUT3_CASES)
GROUPS = {"explicit", "plain", "topic", "collision", "paraphrase"}


@pytest.mark.parametrize("cases, sizes", [
    (DEV_CASES, {"explicit": 25, "plain": 14, "topic": 20, "collision": 8, "paraphrase": 10}),
    (HOLDOUT_CASES, {"explicit": 12, "plain": 5, "topic": 12, "collision": 4, "paraphrase": 5}),
    (HOLDOUT2_CASES, {"explicit": 4, "plain": 4, "topic": 12, "paraphrase": 20}),
    (HOLDOUT3_CASES, {"paraphrase": 8, "collision": 12}),
])
def test_datasets_are_well_formed(cases, sizes):
    ids = [c["id"] for c in cases]
    assert len(ids) == len(set(ids))
    for case in cases:
        assert case["expected"] in FORMATS
        assert case["lang"] in {"en", "ko"}
        assert case["group"] in GROUPS
    assert Counter(c["group"] for c in cases) == sizes


def test_datasets_do_not_overlap():
    sets = [DEV_CASES, HOLDOUT_CASES, HOLDOUT2_CASES, HOLDOUT3_CASES]
    for i, left in enumerate(sets):
        for right in sets[i + 1:]:
            assert not {c["id"] for c in left} & {c["id"] for c in right}
            assert not {c["task"] for c in left} & {c["task"] for c in right}


@pytest.mark.parametrize("result", [DEV, HOLDOUT, HOLDOUT2], ids=["dev", "holdout", "holdout2"])
def test_explicit_requests_and_plain_text_are_fully_correct(result):
    assert result["by_group"]["explicit"]["accuracy"] == 1.0
    assert result["by_group"]["plain"]["accuracy"] == 1.0
    assert result["wrong_media_rate"] == 0.0


def test_dev_floors_do_not_regress():
    assert DEV["overall"]["correct"] >= 77
    assert DEV["by_group"]["collision"]["correct"] >= 8
    assert DEV["by_group"]["topic"]["correct"] >= 20
    assert DEV["by_group"]["paraphrase"]["correct"] >= 10
    assert DEV["unnecessary_media_rate"] <= 0.0
    assert DEV["missed_media_rate"] <= 0.0


def test_holdout_floors_do_not_regress():
    assert HOLDOUT["overall"]["correct"] >= 37
    assert HOLDOUT["by_group"]["topic"]["correct"] >= 12
    assert HOLDOUT["by_group"]["collision"]["correct"] >= 3
    assert HOLDOUT["by_group"]["paraphrase"]["correct"] >= 5
    assert HOLDOUT["unnecessary_media_rate"] <= 0.048
    assert HOLDOUT["missed_media_rate"] <= 0.0


def test_holdout3_self_cue_floors_do_not_regress():
    assert HOLDOUT3["overall"]["correct"] >= 20
    assert HOLDOUT3["by_group"]["collision"]["correct"] >= 12
    assert HOLDOUT3["by_group"]["paraphrase"]["correct"] >= 8
    assert HOLDOUT3["wrong_media_rate"] == 0.0


def test_holdout2_floors_do_not_regress():
    assert HOLDOUT2["overall"]["correct"] >= 37
    assert HOLDOUT2["by_group"]["paraphrase"]["correct"] >= 18
    assert HOLDOUT2["by_group"]["topic"]["correct"] >= 11
    assert HOLDOUT2["unnecessary_media_rate"] <= 0.062
    assert HOLDOUT2["missed_media_rate"] <= 0.083
