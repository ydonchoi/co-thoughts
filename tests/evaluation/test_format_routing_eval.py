"""Regression gate for the Phase 4 keyword evaluation.

Floors are the v0.1 measured values (see
docs/testing/format_routing_keyword_eval_v0.1.md). They guard against
regressions; raise them when the planner improves.
"""
from collections import Counter

from explanation_format_router import FORMATS

from format_routing_eval import evaluate, load_cases

CASES = load_cases()
RESULT = evaluate(CASES)


def test_dataset_is_well_formed():
    ids = [c["id"] for c in CASES]
    assert len(ids) == len(set(ids))
    for case in CASES:
        assert case["expected"] in FORMATS
        assert case["lang"] in {"en", "ko"}
        assert case["group"] in {"explicit", "plain", "topic", "collision", "paraphrase"}
    assert Counter(c["group"] for c in CASES) == {
        "explicit": 25, "plain": 14, "topic": 20, "collision": 8, "paraphrase": 10,
    }


def test_explicit_requests_and_plain_text_are_fully_correct():
    assert RESULT["by_group"]["explicit"]["accuracy"] == 1.0
    assert RESULT["by_group"]["plain"]["accuracy"] == 1.0
    assert RESULT["wrong_media_rate"] == 0.0


def test_measured_floors_do_not_regress():
    assert RESULT["overall"]["correct"] >= 48
    assert RESULT["by_group"]["collision"]["correct"] >= 7
    assert RESULT["by_group"]["topic"]["correct"] >= 2
    assert RESULT["unnecessary_media_rate"] <= 0.452
    assert RESULT["missed_media_rate"] <= 0.286
