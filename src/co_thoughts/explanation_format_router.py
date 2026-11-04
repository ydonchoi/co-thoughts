"""Deterministic, capability-aware explanation-format planning.

This module plans presentation only. It does not generate media, render output,
or verify claims and never changes epistemic or verification status.

Plan fields:
- ``fallback``: the format to use if rendering ``primary`` fails; ``None`` when
  ``primary`` is already TEXT.
- ``excluded_formats``: the candidate format that was considered but not
  selected (FALLBACK), otherwise empty.
- ``secondary``: reserved; v0.1 plans a single primary format and returns ``[]``.
- ``conflicts``: conflicts between the user's explicit ``requested_format`` and
  the user's ``output_intent.accessibility`` requirements or the project
  adapter's ``output_schema``; empty when there is none. The planner reports a
  conflict and overrides neither constraint (``selection_status`` ``CONFLICT``,
  TEXT plan).
- ``accessibility_requirements``: obligations the host must meet when
  rendering ``primary`` (``TEXT_ALTERNATIVE``, ``CAPTIONS``); empty otherwise.
"""
from __future__ import annotations

import re
from collections.abc import Mapping
from typing import Any

from request_validation import validate_routing_request

FORMATS = frozenset({
    "TEXT", "DIAGRAM", "IMAGE", "INTERACTIVE", "ANIMATION", "VIDEO", "SIMULATION",
})
_CAPABILITY_KEYS = {
    "TEXT": "text",
    "DIAGRAM": "diagram",
    "IMAGE": "image",
    "INTERACTIVE": "interactive",
    "ANIMATION": "animation",
    "VIDEO": "video",
    "SIMULATION": "simulation",
}

# Checked in order: DIAGRAM precedes IMAGE so specific wording ("draw a
# flowchart") wins over the generic "draw".
_FORMAT_KEYWORDS: dict[str, tuple[str, ...]] = {
    "SIMULATION": (
        "simulation", "simulate", "simulating", "시뮬레이션", "모의실험", "가정별 결과",
        # paraphrases
        "what-if", "scenario analysis", "model what happens", "시나리오별",
    ),
    "INTERACTIVE": (
        "interactive", "interactivity", "slider", "manipulate variables",
        "대화형", "인터랙티브", "변수 조작", "직접 조작", "상호작용",
        # paraphrases
        "let me tweak", "let me adjust", "let me play with", "let me change",
        "let me vary", "바꿔가며", "바꿔 가며", "바꿔볼 수 있게", "조절하면서",
        "조절하며", "조절할 수 있게",
    ),
    "ANIMATION": (
        "animation", "animated", "animate", "animating", "애니메이션", "움직이는 설명",
        "동작을 움직임으로",
        # paraphrases
        "in motion", "움직이게", "움직이는 모습으로",
    ),
    "VIDEO": (
        "video", "movie", "영상", "동영상", "설명 영상",
        # paraphrases
        "clip", "screencast", "녹화", "클립",
    ),
    "DIAGRAM": (
        "diagram", "flowchart", "process flow", "architecture diagram",
        "structure diagram", "도식", "다이어그램", "흐름도", "구조도",
        "관계도", "순서도", "절차도", "개념도",
        # paraphrases
        "visualize", "visualise", "visualization", "visualisation", "chart",
        "graph", "mind map", "timeline", "boxes and arrows",
        "시각화", "차트", "그래프", "도표", "도해", "마인드맵", "타임라인",
    ),
    "IMAGE": (
        "image", "illustration", "draw", "drawing", "picture", "이미지", "그림",
        "일러스트", "삽화", "외관을 그려",
        # paraphrases
        "photo", "photograph", "clip art", "사진",
    ),
}

# Phrases whose substrings collide with format keywords but do not request a
# format (e.g. "big picture", "그림자" = shadow, "영상의학" = radiology).
_KEYWORD_EXCLUSIONS: tuple[str, ...] = (
    "big picture", "bigger picture", "draw conclusions", "draw a conclusion",
    "draw on", "draw upon", "그림자", "영상의학",
)


def _keyword_pattern(keyword: str) -> re.Pattern[str]:
    escaped = re.escape(keyword.casefold())
    if keyword.isascii():
        # ASCII keywords must match whole words ("draw" must not match "drawbacks"),
        # allowing simple plural/past suffixes ("images", "simulated").
        return re.compile(rf"(?<![a-z0-9]){escaped}(?:s|es|d|ed)?(?![a-z0-9])")
    # Korean keywords are matched as substrings so particles (e.g. "도식을") still match.
    return re.compile(escaped)


# Keyword matches to skip when followed by these words, because the compound
# names a different format ("clip art" is an image, not a video clip).
_KEYWORD_NOT_FOLLOWED_BY: dict[str, tuple[str, ...]] = {
    "clip": ("art",),
}

_FORMAT_PATTERNS: tuple[tuple[str, tuple[tuple[str, re.Pattern[str]], ...]], ...] = tuple(
    (format_name, tuple((k, _keyword_pattern(k)) for k in keywords))
    for format_name, keywords in _FORMAT_KEYWORDS.items()
)

# --- Request cues -----------------------------------------------------------
# A format keyword only selects a format when the wording asks for that output,
# not when the format word is merely the topic ("explain JPEG image
# compression", "기업 이미지 관리 전략"). See
# docs/testing/format_routing_keyword_eval_v0.1.md for the measured motivation.

# English request verbs that may appear up to _CUE_WINDOW tokens before a
# format noun ("show me a picture", "make a short video").
_EN_REQUEST_VERBS = frozenset({
    "show", "draw", "make", "create", "give", "generate", "render", "build",
    "produce", "run", "sketch", "illustrate", "add", "display", "design",
    "record", "prepare", "provide", "include", "use", "want", "need",
    "present",
})
_CUE_WINDOW = 4
# A request verb only governs the keyword when no clause boundary sits between
# them: "I need to understand video codecs" / "Show how video codecs work" /
# "Show that the image of ..." do not request a video or an image.
_EN_CLAUSE_BREAKERS = frozenset({
    "to", "how", "why", "what", "when", "where", "which", "who", "whether",
    "that", "if",
})
# "as a diagram", "in a video", "with an animation", ...
_EN_PREPOSITION_CUE = re.compile(r"(?<![a-z0-9])(?:as|in|with|into|using|via)\s+(?:a|an)\s+(?:\S+\s+){0,2}$")
# The preposition form only marks an output form when the format word heads
# its phrase ("in a video", "as a diagram, please", "with an animation of ...")
# rather than modifying another noun ("in a video game", "in a video codec").
_EN_PHRASE_HEAD_FOLLOWER = re.compile(
    r"^(?:\s*(?:$|[.,;:!?)])|\s+(?:of|about|on|that|which|showing|explaining|"
    r"illustrating|to|for|with|please|so|and)(?![a-z0-9]))"
)
# Keywords that are themselves request verbs; they count when used as an
# imperative ("Draw ...", "Can you simulate ...").
_EN_VERB_KEYWORDS = frozenset({
    "draw", "simulate", "simulating", "animate", "animating",
    "visualize", "visualise", "chart", "graph",
})
# A sentence-initial verb keyword is a noun subject, not a command, when it is
# followed by "of" or a copula/auxiliary soon after ("Graph theory is ...",
# "Chart of accounts ...").
# A wh-word right after the keyword opens an object clause ("Chart what is
# happening ...", "Chart who is buying"), so it is still a command.
_EN_SUBJECT_FOLLOWER = re.compile(
    r"^\s+(?!(?:what|who|whom|whose|which|how|where|when|why|whether)(?![a-z0-9]))"
    r"(?:of(?![a-z0-9])|(?:\S+\s+){0,2}(?:is|are|was|were|has|have|can|will)(?![a-z0-9]))"
)
_EN_POLITE_PREFIX = re.compile(r"^(?:(?:please|kindly|can|could|would|will|you)\s+)*$")
# A format noun that opens the task is a terse request ("Diagram of the TCP
# handshake", "A video about photosynthesis", "Image: a red apple").
_EN_LEADING_NOUN_PREFIX = re.compile(r"^\W*(?:(?:please|a|an|the|one|some)\s+)*$")

# Korean: keyword, optionally one short word, then a particle and a request
# verb ("구조도를 만들어줘", "인터랙티브 설명을 만들어줘"), or a form particle
# ("애니메이션으로", "흐름도로") which already marks the output form.
_KO_FORM_PARTICLE = re.compile(r"^(?:으로|로)")
_KO_OBJECT_REQUEST = re.compile(
    r"^(?:\s?\S{0,4})?(?:을|를|이|가)?\s?"
    # ㄴ-forms (그린, 만든, ...) only count when sequential ("그린 다음 ...");
    # otherwise _ko_is_attributive rejects them ("만든 이어폰").
    r"(?:보여|그려|그리|만들|돌려|해\s?줘|해줘|생성|띄워|부탁|필요|원해"
    r"|그린|만든|보여준|돌린|생성한|띄운)\S*"
)


_KO_SEQUENCE_NOUN = re.compile(r"^\s*(?:다음|뒤|후)")
# Only production verbs in ㄴ-form can start a "<make it> 다음 <then ...>"
# request, and only when the sentence still ends in a request.
_KO_SEQUENCE_PRODUCTION = ("그린", "만든", "보여준", "돌린", "생성한", "띄운")
_KO_REQUEST_ENDING = re.compile(r"줘|주세요|주시")


def _ko_is_attributive(word: str, following: str = "") -> bool:
    """True for an attributive (noun-modifying) Korean verb form.

    "그려주는 프로그램", "만들어주는 도구", "필요한 이유", "만든 이어폰" describe
    something rather than ask for it; "그려줘", "만들어주고", "보여주세요" ask.
    A production verb in ㄴ-form followed by 다음/뒤/후 and a later request
    ending is sequential, not attributive: "흐름도를 그린 다음 설명해줘" still
    asks for the diagram, while "흐름도를 그린 다음 단계는 뭐야?" and
    "구조도가 필요한 다음 단계는 무엇인가?" do not.
    """
    word = word.rstrip(".,;:!?)\"'")
    if not word:
        return False
    sequence = _KO_SEQUENCE_NOUN.match(following)
    if (
        sequence
        and word.startswith(_KO_SEQUENCE_PRODUCTION)
        and _KO_REQUEST_ENDING.search(following[sequence.end():])
    ):
        return False
    last = word[-1]
    if last == "는":
        return True
    code = ord(last) - 0xAC00
    return 0 <= code < 11172 and code % 28 == 4  # final consonant ㄴ


def _ko_request_word_at(text: str) -> bool:
    """True when ``text`` starts (after optional spaces) with a non-attributive word."""
    words = text.split(None, 1)
    return bool(words) and not _ko_is_attributive(words[0])
# Keywords that already describe a requested output form. Most still need a
# small context check, because the same phrases have everyday non-request
# uses ("Let me change the subject", "식단을 조절하면서 운동하는 방법").
_SELF_CUED = frozenset({
    "외관을 그려", "움직이는 설명", "동작을 움직임으로",
    "boxes and arrows", "model what happens",
    "let me tweak", "let me adjust", "let me play with", "let me change", "let me vary",
    "바꿔가며", "바꿔 가며", "바꿔볼 수 있게", "조절하면서", "조절하며", "조절할 수 있게",
    "움직이는 모습으로",
})
# "let me <manipulate>" is interactive only when the user also wants to watch
# the effect in the same sentence ("... and see how the curve changes").
_EN_LET_ME = frozenset({"let me tweak", "let me adjust", "let me play with", "let me change", "let me vary"})
_EN_OBSERVATION_CUE = re.compile(r"(?<![a-z0-9])(?:see|watch|observe|compare|what happens)(?![a-z0-9])")
_EN_SENTENCE_END = re.compile(r"[.!?;:\u2014]")
# Korean "<change/adjust> while ..." is interactive only with an observation or
# result cue, and not when the task asks for a method/reason/principle.
_KO_MANIPULATE = frozenset({"바꿔가며", "바꿔 가며", "바꿔볼 수 있게", "조절하면서", "조절하며", "조절할 수 있게"})
_KO_OBSERVATION_CUE = re.compile(r"결과|확인|볼 수|보여|변화|변하|바뀌|달라지")
_KO_EXPLANATION_NOUN = re.compile(r"방법|이유|원리")
_KO_INTERACTIVE_REQUEST_FORM = re.compile(r"(?:있게\s?해|보여|만들어)\S*")
_KO_MOTION_FORM_REQUEST = re.compile(r"^\s?(?:\S+\s){0,2}?(?:보여|그려|만들|설명해|나타내)\S*")
# Indirect request openers accepted before "model what happens"
# ("Would you be able to model ...", "Could you possibly model ...").
_EN_INDIRECT_REQUEST_PREFIX = re.compile(
    r"^(?:(?:please|kindly|can|could|would|will|you|possibly|be able to)\s+)*$"
)
_EN_FORM_PREPOSITION_BEFORE = re.compile(r"(?<![a-z0-9])(?:as|in|with|using|into)\s+$")

# Explicit precedence: the first true signal wins. Richer formats that subsume
# simpler ones come first (a simulation is also interactive; an animation of a
# process is also a diagram). Pinned by tests.
_CONTEXT_SIGNAL_PRECEDENCE: tuple[tuple[str, str], ...] = (
    ("simulation_required", "SIMULATION"),
    ("requires_interaction", "INTERACTIVE"),
    ("time_dependent_behavior", "ANIMATION"),
    ("visual_subject", "IMAGE"),
    ("process_or_structure", "DIAGRAM"),
    ("has_competing_hypotheses", "DIAGRAM"),
)


def _normalize_requested_format(value: Any) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str) or not value.strip():
        raise ValueError("REQUESTED_FORMAT_INVALID")
    normalized = value.strip().upper()
    if normalized not in FORMATS:
        raise ValueError("REQUESTED_FORMAT_UNSUPPORTED")
    return normalized


_ACCESSIBILITY_KEYS = ("screen_reader", "reduced_motion", "captions", "text_only")
_MOTION_FORMATS = frozenset({"ANIMATION", "VIDEO"})


def _normalize_accessibility(value: Any) -> dict[str, bool]:
    """Return the user's accessibility requirements (all ``False`` if absent).

    - ``text_only``: only TEXT may be planned.
    - ``reduced_motion``: ANIMATION and VIDEO may not be planned.
    - ``screen_reader``: a non-TEXT plan must carry a ``TEXT_ALTERNATIVE``
      requirement for the host.
    - ``captions``: a VIDEO plan must carry a ``CAPTIONS`` requirement.
    """
    if value is None:
        return {key: False for key in _ACCESSIBILITY_KEYS}
    if not isinstance(value, Mapping):
        raise ValueError("ACCESSIBILITY_INVALID")
    unknown = sorted(str(key) for key in value if key not in _ACCESSIBILITY_KEYS)
    if unknown:
        raise ValueError(f"ACCESSIBILITY_UNKNOWN:{unknown[0]}")
    normalized = {}
    for key in _ACCESSIBILITY_KEYS:
        flag = value.get(key, False)
        if not isinstance(flag, bool):
            raise ValueError(f"ACCESSIBILITY_INVALID:{key}")
        normalized[key] = flag
    return normalized


def _normalize_output_schema(value: Any) -> frozenset[str] | None:
    """Return the formats the project adapter's output schema allows.

    ``None`` means the adapter declared no schema (no constraint). A declared
    schema must list ``allowed_formats`` and must allow TEXT, because TEXT is
    the planner's only fallback.
    """
    if value is None:
        return None
    if not isinstance(value, Mapping):
        raise ValueError("OUTPUT_SCHEMA_INVALID")
    unknown = sorted(str(key) for key in value if key != "allowed_formats")
    if unknown:
        raise ValueError(f"OUTPUT_SCHEMA_UNKNOWN_FIELD:{unknown[0]}")
    allowed = value.get("allowed_formats")
    if not isinstance(allowed, (list, tuple)) or not allowed:
        raise ValueError("OUTPUT_SCHEMA_ALLOWED_FORMATS_INVALID")
    normalized = set()
    for item in allowed:
        if not isinstance(item, str) or not item.strip():
            raise ValueError("OUTPUT_SCHEMA_ALLOWED_FORMATS_INVALID")
        name = item.strip().upper()
        if name not in FORMATS:
            raise ValueError(f"OUTPUT_SCHEMA_FORMAT_UNSUPPORTED:{name}")
        normalized.add(name)
    if "TEXT" not in normalized:
        raise ValueError("OUTPUT_SCHEMA_TEXT_REQUIRED")
    return frozenset(normalized)


def _validate_context_signals(context: Mapping[str, Any]) -> None:
    for signal, _ in _CONTEXT_SIGNAL_PRECEDENCE:
        value = context.get(signal, False)
        if not isinstance(value, bool):
            raise ValueError(f"CONTEXT_SIGNAL_INVALID:{signal}")


def _exclusion_pattern(phrase: str) -> re.Pattern[str]:
    if not phrase.isascii():
        return re.compile(re.escape(phrase))
    # Inflection-aware on the first word: "draw upon" also excludes
    # "draws upon" / "drawing upon"; "big picture" also "bigger picture".
    first, _, rest = phrase.partition(" ")
    tail = rf"\s+{re.escape(rest)}" if rest else ""
    return re.compile(rf"(?<![a-z0-9]){re.escape(first)}[a-z]*{tail}(?![a-z0-9])")


_EXCLUSION_PATTERNS = tuple(_exclusion_pattern(p) for p in _KEYWORD_EXCLUSIONS)


def _normalize_task_text(task: str) -> str:
    normalized = task.casefold()
    for pattern in _EXCLUSION_PATTERNS:
        normalized = pattern.sub(" ", normalized)
    return normalized


def _self_cue_holds(keyword: str, text: str, start: int, end: int) -> bool:
    """Context check for self-cued phrases (see _SELF_CUED)."""
    before, after = text[:start], text[end:]
    if keyword in _EN_LET_ME:
        sentence_rest = _EN_SENTENCE_END.split(after, maxsplit=1)[0]
        return bool(_EN_OBSERVATION_CUE.search(sentence_rest))
    if keyword in _KO_MANIPULATE:
        rest = re.split(r"[.!?]", after, maxsplit=1)[0]
        explanation = _KO_EXPLANATION_NOUN.search(rest)
        if explanation is None:
            return bool(_KO_OBSERVATION_CUE.search(rest))
        # An explanation noun means "how/why to <manipulate>" unless the
        # interactive output was already requested before it
        # ("... 확인할 수 있게 해주고, 그 원리도 설명해줘").
        head = rest[:explanation.start()]
        return bool(_KO_OBSERVATION_CUE.search(head)) and any(
            not _ko_is_attributive(m.group(0), head[m.end():])
            for m in _KO_INTERACTIVE_REQUEST_FORM.finditer(head)
        )
    if keyword == "model what happens":
        sentence_start = re.split(r"[.!?;]\s*", before)[-1]
        if _EN_INDIRECT_REQUEST_PREFIX.match(sentence_start):
            return True
        tokens = re.findall(r"[a-z0-9]+", before)
        start_index = max(len(tokens) - _CUE_WINDOW, 0)
        for index in range(start_index, len(tokens)):
            if tokens[index] not in _EN_REQUEST_VERBS:
                continue
            between = tokens[index + 1:]
            # "I want you to model ..." / "I need to model ..." ask us;
            # "researchers need to model ..." describes someone else.
            previous = tokens[index - 1] if index > 0 else ""
            first_person = previous in {"i", "we"} and between == ["to"]
            if between == ["you", "to"] or first_person or not _EN_CLAUSE_BREAKERS & set(between):
                return True
        return False
    if keyword == "boxes and arrows":
        return bool(_EN_FORM_PREPOSITION_BEFORE.search(before))
    if keyword == "움직이는 모습으로":
        match = _KO_MOTION_FORM_REQUEST.match(after)
        return bool(match) and not _ko_is_attributive(match.group(0).split()[-1], after[match.end():])
    return True


def _is_requested(keyword: str, text: str, start: int, end: int) -> bool:
    """Return True when the keyword at text[start:end] is asked for as output."""
    if keyword in _SELF_CUED:
        return _self_cue_holds(keyword, text, start, end)
    if not keyword.isascii():
        after = text[end:]
        particle = _KO_FORM_PARTICLE.match(after)
        if particle:
            # "흐름도로 그려주는 프로그램" describes a tool, not a request.
            rest = after[particle.end():]
            verb = _KO_OBJECT_REQUEST.match(rest)
            return not (verb and _ko_is_attributive(verb.group(0).split()[-1], rest[verb.end():]))
        verb = _KO_OBJECT_REQUEST.match(after)
        return bool(verb) and not _ko_is_attributive(verb.group(0).split()[-1], after[verb.end():])

    before = text[:start]
    sentence_start = re.split(r"[.!?;]\s*", before)[-1]
    if keyword in _EN_VERB_KEYWORDS:
        if _EN_POLITE_PREFIX.match(sentence_start) and not _EN_SUBJECT_FOLLOWER.match(text[end:]):
            return True
    elif _EN_LEADING_NOUN_PREFIX.match(before):
        return True
    if _EN_PREPOSITION_CUE.search(before) and _EN_PHRASE_HEAD_FOLLOWER.match(text[end:]):
        return True
    window = re.findall(r"[a-z0-9]+", before)[-_CUE_WINDOW:]
    for index, token in enumerate(window):
        if token in _EN_REQUEST_VERBS and not _EN_CLAUSE_BREAKERS & set(window[index + 1:]):
            return True
    return False


def _infer_format(task: str, context: Mapping[str, Any]) -> tuple[str, str]:
    # Explicit, typed context signals take precedence over lexical hints.
    for signal, format_name in _CONTEXT_SIGNAL_PRECEDENCE:
        if context.get(signal, False):
            return format_name, f"context signal: {signal}"

    normalized = _normalize_task_text(task)
    for format_name, patterns in _FORMAT_PATTERNS:
        for keyword, pattern in patterns:
            blocked = _KEYWORD_NOT_FOLLOWED_BY.get(keyword.casefold(), ())
            for match in pattern.finditer(normalized):
                following = normalized[match.end():].split(None, 1)
                if blocked and following and following[0].strip(".,;:!?") in blocked:
                    continue
                if _is_requested(keyword.casefold(), normalized, match.start(), match.end()):
                    return format_name, f"task wording requests {format_name.lower()}"

    return "TEXT", "text is the least-complex sufficient default"


def route_explanation_format(request: Mapping[str, Any]) -> dict[str, Any]:
    """Return a provisional explanation-format plan without generating media.

    Only TEXT is assumed available when the host supplies no capability map.
    Non-text formats require an explicit capability declaration from the host.
    """
    task, context = validate_routing_request(request)
    _validate_context_signals(context)

    output_intent = request.get("output_intent")
    if output_intent is None:
        output_intent = {}
    if not isinstance(output_intent, Mapping):
        raise ValueError("OUTPUT_INTENT_INVALID")

    requested_format = _normalize_requested_format(
        output_intent.get("requested_format")
    )

    accessibility = _normalize_accessibility(output_intent.get("accessibility"))
    allowed_by_schema = _normalize_output_schema(request.get("output_schema"))

    capabilities = request.get("capabilities")
    if capabilities is None:
        normalized_capabilities = {"TEXT": True}
    else:
        if not isinstance(capabilities, Mapping):
            raise ValueError("CAPABILITIES_INVALID")
        unknown = sorted(
            str(key) for key in capabilities if key not in _CAPABILITY_KEYS.values()
        )
        if unknown:
            raise ValueError(f"CAPABILITY_UNKNOWN:{unknown[0]}")
        normalized_capabilities = {"TEXT": True}
        for format_name, key in _CAPABILITY_KEYS.items():
            if key in capabilities:
                value = capabilities[key]
                if not isinstance(value, bool):
                    raise ValueError(f"CAPABILITY_INVALID:{key}")
                normalized_capabilities[format_name] = value

    if normalized_capabilities.get("TEXT") is not True:
        raise ValueError("TEXT_CAPABILITY_REQUIRED")

    if requested_format is not None:
        candidate = requested_format
        rationale = [f"user explicitly requested {candidate}"]
    else:
        candidate, reason = _infer_format(task, context)
        rationale = [reason]

    available = sorted(
        name for name, enabled in normalized_capabilities.items() if enabled
    )
    unavailable = [candidate] if candidate not in available else []

    candidate_declared = (
        capabilities is not None and _CAPABILITY_KEYS[candidate] in capabilities
    )

    # Blockers are evaluated in the §7 priority order: the user's
    # accessibility requirements first, then the project output schema.
    blockers: list[dict[str, Any]] = []
    if accessibility["text_only"] and candidate != "TEXT":
        blockers.append({
            "type": "REQUESTED_FORMAT_CONFLICTS_WITH_ACCESSIBILITY",
            "requirement": "text_only",
            "reason": f"{candidate} is excluded by the text_only accessibility requirement",
        })
    if accessibility["reduced_motion"] and candidate in _MOTION_FORMATS:
        blockers.append({
            "type": "REQUESTED_FORMAT_CONFLICTS_WITH_ACCESSIBILITY",
            "requirement": "reduced_motion",
            "reason": f"{candidate} is excluded by the reduced_motion accessibility requirement",
        })
    if allowed_by_schema is not None and candidate not in allowed_by_schema:
        blockers.append({
            "type": "REQUESTED_FORMAT_NOT_IN_OUTPUT_SCHEMA",
            "allowed_formats": sorted(allowed_by_schema),
            "reason": f"{candidate} is not allowed by the project output schema",
        })

    conflicts: list[dict[str, Any]] = []
    if blockers:
        # An explicit user request that contradicts an accessibility
        # requirement or the project output schema is reported, not silently
        # applied or silently dropped; neither constraint is overridden.
        primary = "TEXT"
        fallback = None
        if requested_format is not None:
            selection_status = "CONFLICT"
            for blocker in blockers:
                entry = {"type": blocker["type"], "requested_format": candidate}
                if "requirement" in blocker:
                    entry["requirement"] = blocker["requirement"]
                if "allowed_formats" in blocker:
                    entry["allowed_formats"] = blocker["allowed_formats"]
                conflicts.append(entry)
                if blocker["type"] == "REQUESTED_FORMAT_NOT_IN_OUTPUT_SCHEMA":
                    rationale.append(
                        f"{blocker['reason']}; the schema is not overridden; using TEXT"
                    )
                else:
                    rationale.append(
                        f"{blocker['reason']}; the requirement is not overridden; using TEXT"
                    )
        else:
            selection_status = "FALLBACK"
            for blocker in blockers:
                rationale.append(f"{blocker['reason']}; using TEXT")
    elif candidate in available:
        primary = candidate
        selection_status = "SELECTED"
        fallback = "TEXT" if candidate != "TEXT" else None
        if candidate != "TEXT":
            rationale.append("host capability explicitly declares this format available")
    else:
        primary = "TEXT"
        selection_status = "FALLBACK"
        # primary is already TEXT; there is nothing further to fall back to.
        fallback = None
        if candidate_declared:
            rationale.append(
                f"{candidate} is declared unavailable by the host; using TEXT"
            )
        else:
            rationale.append(
                f"{candidate} capability was not declared by the host; using TEXT"
            )

    accessibility_requirements: list[str] = []
    if primary != "TEXT" and accessibility["screen_reader"]:
        accessibility_requirements.append("TEXT_ALTERNATIVE")
    if primary == "VIDEO" and accessibility["captions"]:
        accessibility_requirements.append("CAPTIONS")

    uncertainties = []
    if capabilities is None:
        uncertainties.append(
            "Only TEXT is assumed available because the host supplied no capability map"
        )
    if blockers:
        for blocker in blockers:
            if selection_status == "CONFLICT":
                if blocker["type"] == "REQUESTED_FORMAT_NOT_IN_OUTPUT_SCHEMA":
                    uncertainties.append(
                        f"The user requested {candidate}, which the project output schema "
                        "does not allow; the user or project owner must resolve the conflict"
                    )
                else:
                    uncertainties.append(
                        f"The user requested {candidate}, which conflicts with the user's "
                        f"{blocker['requirement']} accessibility requirement; "
                        "the user must resolve the conflict"
                    )
            elif blocker["type"] == "REQUESTED_FORMAT_NOT_IN_OUTPUT_SCHEMA":
                uncertainties.append(
                    f"The project output schema does not allow {candidate}"
                )
            else:
                uncertainties.append(
                    f"The {blocker['requirement']} accessibility requirement excludes {candidate}"
                )
    elif selection_status == "FALLBACK":
        if candidate_declared:
            uncertainties.append(
                f"The host explicitly declared {candidate} unavailable"
            )
        else:
            uncertainties.append(
                f"The host did not declare {candidate} capability"
            )

    return {
        "format_plan": {
            "primary": primary,
            # Reserved: v0.1 plans a single primary format and never fills this.
            "secondary": [],
            "rationale": rationale,
            "excluded_formats": [] if selection_status == "SELECTED" else [candidate],
            "assumptions": ["Format planning does not generate or render media"],
            "uncertainties": uncertainties,
            "fallback": fallback,
            "selection_status": selection_status,
            "conflicts": conflicts,
            "accessibility_requirements": accessibility_requirements,
        },
        "capability_status": {
            "requested": [candidate],
            "available": available,
            "unavailable": unavailable,
        },
        "execution_status": "NOT_RUN",
        "render_status": "NOT_RUN",
        "functional_test_status": "NOT_RUN",
        "verification_status": "UNVERIFIED",
        "is_evidence": False,
    }


def plan_explanation_format_safely(request: Mapping[str, Any]) -> dict[str, Any]:
    """Like ``route_explanation_format`` but never raises on invalid format input.

    Used by ``cognitive_router.route()`` so that malformed format-planning input
    (capabilities, output_intent, output_schema, context signals) cannot break cognitive or
    verification routing. The failure is reported as ``INVALID_INPUT`` with a
    TEXT plan instead.
    """
    try:
        return route_explanation_format(request)
    except (TypeError, ValueError) as exc:
        return {
            "format_plan": {
                "primary": "TEXT",
                "secondary": [],
                "rationale": ["format planning input was invalid; using TEXT"],
                "excluded_formats": [],
                "assumptions": ["Format planning does not generate or render media"],
                "uncertainties": [
                    "Requested format and host capabilities could not be evaluated"
                ],
                "fallback": None,
                "selection_status": "INVALID_INPUT",
                "conflicts": [],
                "accessibility_requirements": [],
            },
            "capability_status": {
                "requested": [],
                "available": ["TEXT"],
                "unavailable": [],
            },
            "error": str(exc),
            "execution_status": "NOT_RUN",
            "render_status": "NOT_RUN",
            "functional_test_status": "NOT_RUN",
            "verification_status": "UNVERIFIED",
            "is_evidence": False,
        }
