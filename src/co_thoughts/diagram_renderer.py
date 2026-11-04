"""Dependency-free DIAGRAM renderer: a Mermaid flowchart subset to SVG.

This is the first real renderer for ``format_host`` (design doc §13.3 item 5).
It parses and validates a small, explicit subset of Mermaid flowchart syntax
and lays it out deterministically as SVG. Anything outside the subset raises
``DiagramSyntaxError`` so the host records ``RENDER_FAILED`` and delivers the
TEXT version instead of a guessed drawing.

Supported subset:

- Header: ``graph`` or ``flowchart`` followed by ``TD``, ``TB`` or ``LR``.
- Nodes: ``id``, ``id[label]``, ``id(label)`` (rounded), ``id{label}``
  (decision). Ids are letters, digits and ``_`` with single inner hyphens (``a-b``); labels may be quoted.
- Edges: ``-->`` (arrow) and ``---`` (line), optionally labelled with
  ``-->|label|`` or ``-- label -->``; chains such as ``A --> B --> C``.
- ``%%`` comment lines and ``;`` statement separators.

The SVG carries ``<title>`` and ``<desc>`` (``role="img"``). Rendering never
verifies the diagram's content; the host keeps ``verification_status``
``UNVERIFIED`` regardless of what this renderer returns.
"""
from __future__ import annotations

import hashlib
import re
import unicodedata
from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import Any
from xml.sax.saxutils import escape

MAX_NODES = 200
MAX_EDGES = 400
MAX_LABEL_CHARS = 200
MAX_SOURCE_CHARS = 20_000
MAX_TITLE_CHARS = 200
MAX_DESCRIPTION_CHARS = 2_000

# The header may be followed by statements on the same line after ``;``
# (compact form ``graph TD; A --> B``).
_HEADER = re.compile(r"^(?:graph|flowchart)\s+(TD|TB|LR)\s*(?:;(.*))?$", re.IGNORECASE)
_ID = r"[A-Za-z_][A-Za-z0-9_]*(?:-[A-Za-z0-9_]+)*"
_NODE = re.compile(
    rf"\s*({_ID})\s*(?:\[([^\[\]]*)\]|\(([^()]*)\)|\{{([^{{}}]*)\}})?"
)
# ``-- label -->`` must be tried before the bare ``-->``/``---`` operators.
_EDGE_TEXT = re.compile(r"\s*--\s+([^-|][^|]*?)\s+(-->|---)")
_EDGE = re.compile(r"\s*(-->|---)(?:\s*\|([^|]*)\|)?")
# Characters XML 1.0 forbids; escaping cannot make them valid SVG.
_XML_INVALID = re.compile("[\x00-\x08\x0b\x0c\x0e-\x1f\ud800-\udfff\ufffe\uffff]")


def _split_statements(line: str) -> list[str]:
    """Split on ``;`` only outside quotes, brackets and ``|edge labels|``."""
    parts: list[str] = []
    buffer: list[str] = []
    in_quote = in_pipe = False
    depth = 0
    for char in line:
        if char == '"':
            in_quote = not in_quote
        elif not in_quote:
            if char in "[({":
                depth += 1
            elif char in "])}":
                depth = max(0, depth - 1)
            elif char == "|" and depth == 0:
                in_pipe = not in_pipe
            elif char == ";" and depth == 0 and not in_pipe:
                parts.append("".join(buffer))
                buffer = []
                continue
        buffer.append(char)
    parts.append("".join(buffer))
    return parts


class DiagramSyntaxError(ValueError):
    """Source is outside the supported Mermaid flowchart subset."""


@dataclass
class Flowchart:
    direction: str
    nodes: dict[str, dict[str, str]] = field(default_factory=dict)
    edges: list[dict[str, Any]] = field(default_factory=list)


def _clean_label(raw: str | None, line_no: int) -> str | None:
    if raw is None:
        return None
    label = raw.strip()
    if len(label) >= 2 and label[0] == label[-1] == '"':
        label = label[1:-1].strip()
    if not label:
        raise DiagramSyntaxError(f"DIAGRAM_EMPTY_LABEL:line {line_no}")
    if len(label) > MAX_LABEL_CHARS:
        raise DiagramSyntaxError(f"DIAGRAM_LABEL_TOO_LONG:line {line_no}")
    return label


def _add_node(chart: Flowchart, match: re.Match[str], line_no: int) -> str:
    node_id = match.group(1)
    rect, rounded, decision = match.group(2), match.group(3), match.group(4)
    if rect is not None:
        shape, raw = "rect", rect
    elif rounded is not None:
        shape, raw = "round", rounded
    elif decision is not None:
        shape, raw = "decision", decision
    else:
        shape, raw = None, None
    label = _clean_label(raw, line_no)

    existing = chart.nodes.get(node_id)
    if existing is None:
        if len(chart.nodes) >= MAX_NODES:
            raise DiagramSyntaxError("DIAGRAM_TOO_MANY_NODES")
        chart.nodes[node_id] = {
            "label": label if label is not None else node_id,
            "shape": shape or "rect",
            "explicit": "1" if label is not None else "",
        }
    elif label is not None:
        if existing["explicit"] and (
            existing["label"] != label or existing["shape"] != shape
        ):
            raise DiagramSyntaxError(f"DIAGRAM_NODE_REDEFINED:{node_id}")
        existing.update(label=label, shape=shape, explicit="1")
    return node_id


def parse_flowchart(source: str) -> Flowchart:
    """Parse ``source`` or raise ``DiagramSyntaxError`` with a stable code."""
    if not isinstance(source, str) or not source.strip():
        raise DiagramSyntaxError("DIAGRAM_SOURCE_REQUIRED")
    if len(source) > MAX_SOURCE_CHARS:
        raise DiagramSyntaxError("DIAGRAM_SOURCE_TOO_LONG")
    if _XML_INVALID.search(source):
        raise DiagramSyntaxError("DIAGRAM_INVALID_CHARACTER")

    lines = [
        (number, line.strip())
        for number, line in enumerate(source.splitlines(), start=1)
        if line.strip() and not line.strip().startswith("%%")
    ]
    if not lines:
        raise DiagramSyntaxError("DIAGRAM_SOURCE_REQUIRED")
    header = _HEADER.match(lines[0][1])
    if header is None:
        raise DiagramSyntaxError(f"DIAGRAM_HEADER_UNSUPPORTED:line {lines[0][0]}")
    direction = "TD" if header.group(1).upper() in ("TD", "TB") else "LR"
    chart = Flowchart(direction=direction)

    statements = list(lines[1:])
    if header.group(2) and header.group(2).strip():
        statements.insert(0, (lines[0][0], header.group(2)))
    for line_no, line in statements:
        for statement in _split_statements(line):
            if statement.strip():
                _parse_statement(chart, statement, line_no)

    if not chart.nodes:
        raise DiagramSyntaxError("DIAGRAM_EMPTY")
    return chart


def _parse_statement(chart: Flowchart, statement: str, line_no: int) -> None:
    match = _NODE.match(statement)
    if match is None:
        raise DiagramSyntaxError(f"DIAGRAM_SYNTAX_UNSUPPORTED:line {line_no}")
    current = _add_node(chart, match, line_no)
    pos = match.end()
    while pos < len(statement) and statement[pos:].strip():
        text_edge = _EDGE_TEXT.match(statement, pos)
        if text_edge is not None:
            op, edge_label = text_edge.group(2), text_edge.group(1)
            op_end, pos = text_edge.end(2), text_edge.end()
        else:
            edge = _EDGE.match(statement, pos)
            if edge is None:
                raise DiagramSyntaxError(f"DIAGRAM_SYNTAX_UNSUPPORTED:line {line_no}")
            op, edge_label = edge.group(1), edge.group(2)
            op_end, pos = edge.end(1), edge.end()
        # Mermaid reserves ``---o``/``---x`` (and ``-->o``/``-->x``) for
        # circle and cross edges; never read the marker as a node id.
        if statement[op_end:op_end + 1] in ("o", "x"):
            raise DiagramSyntaxError(f"DIAGRAM_EDGE_UNSUPPORTED:line {line_no}")
        target = _NODE.match(statement, pos)
        if target is None:
            raise DiagramSyntaxError(f"DIAGRAM_SYNTAX_UNSUPPORTED:line {line_no}")
        target_id = _add_node(chart, target, line_no)
        if len(chart.edges) >= MAX_EDGES:
            raise DiagramSyntaxError("DIAGRAM_TOO_MANY_EDGES")
        chart.edges.append({
            "source": current,
            "target": target_id,
            "arrow": op == "-->",
            "label": _clean_label(edge_label, line_no) if edge_label is not None else None,
        })
        current = target_id
        pos = target.end()


def _ranks(chart: Flowchart) -> dict[str, int]:
    """Deterministic layering: breadth-first depth from source nodes.

    Roots are nodes without incoming edges in declaration order; nodes only
    reachable through a cycle start a new search in declaration order.
    """
    successors: dict[str, list[str]] = {node: [] for node in chart.nodes}
    has_incoming: set[str] = set()
    for edge in chart.edges:
        successors[edge["source"]].append(edge["target"])
        has_incoming.add(edge["target"])
    rank: dict[str, int] = {}
    roots = [node for node in chart.nodes if node not in has_incoming]
    for start in roots + list(chart.nodes):
        if start in rank:
            continue
        rank[start] = 0
        queue = [start]
        while queue:
            node = queue.pop(0)
            for nxt in successors[node]:
                if nxt not in rank:
                    rank[nxt] = rank[node] + 1
                    queue.append(nxt)
    return rank


def describe(chart: Flowchart) -> str:
    """Plain-text summary used for ``<desc>`` when none is supplied."""
    direction = "top-down" if chart.direction == "TD" else "left-to-right"
    parts = []
    for edge in chart.edges:
        connector = "→" if edge["arrow"] else "—"
        text = (
            f"{chart.nodes[edge['source']]['label']} {connector} "
            f"{chart.nodes[edge['target']]['label']}"
        )
        if edge["label"]:
            text += f" ({edge['label']})"
        parts.append(text)
    linked = {e["source"] for e in chart.edges} | {e["target"] for e in chart.edges}
    parts.extend(
        chart.nodes[node]["label"] for node in chart.nodes if node not in linked
    )
    text = (
        f"Flowchart ({direction}) with {len(chart.nodes)} nodes and "
        f"{len(chart.edges)} connections: " + "; ".join(parts) + "."
    )
    # Bound the generated summary like a caller-supplied description, so the
    # <desc> (and the artifact) cannot grow far beyond the source limit.
    if len(text) > MAX_DESCRIPTION_CHARS:
        text = text[: MAX_DESCRIPTION_CHARS - 13].rstrip() + " (truncated)"
    return text


_LINE_PX = 170          # wrap labels at this rendered width
_LINE_HEIGHT = 15
_LANE_GAP = 14
_PARALLEL_GAP = 14
_MAX_TRACKS = 8          # distinct track offsets inside one gap band


# All text uses an explicit monospace stack, so widths are fixed per glyph
# class instead of guessed: ~0.60em for normal glyphs in common monospace
# fonts (DejaVu Sans Mono, Menlo, Courier New; Consolas is 0.55em) and 1em
# for East Asian wide glyphs. The bounds below round up for 12px text and
# are also used for the smaller 11px edge labels, so they are conservative.
FONT_FAMILY = "ui-monospace, 'DejaVu Sans Mono', Menlo, Consolas, 'Courier New', monospace"
_NARROW_PX = 7.5    # 0.625em at 12px
_WIDE_PX = 12.0     # 1em at 12px


def _char_px(char: str) -> float:
    return _WIDE_PX if unicodedata.east_asian_width(char) in ("W", "F") else _NARROW_PX


def _text_px(text: str) -> float:
    return sum(_char_px(char) for char in text)


def wrap_label(label: str, max_px: int = _LINE_PX) -> list[str]:
    """Wrap at spaces when possible, hard-breaking words wider than a line."""
    lines: list[str] = []
    current = ""
    for word in label.split():
        candidate = f"{current} {word}" if current else word
        if _text_px(candidate) <= max_px:
            current = candidate
            continue
        if current:
            lines.append(current)
        current = ""
        for char in word:
            if _text_px(current + char) > max_px and current:
                lines.append(current)
                current = ""
            current += char
    if current:
        lines.append(current)
    return lines or [label]


_EDGE_LINE_PX = 120     # wrap edge labels narrower than node labels


def _text_lines(
    x: float, y_center: float, lines: list[str], css_class: str, size: int,
    anchor: str = "middle",
) -> str:
    first_y = y_center - (len(lines) - 1) * _LINE_HEIGHT / 2 + 4
    spans = "".join(
        f'<tspan x="{x:g}" y="{first_y + i * _LINE_HEIGHT:g}">{escape(line)}</tspan>'
        for i, line in enumerate(lines)
    )
    return (
        f'<text class="{css_class}" font-size="{size}" '
        f'text-anchor="{anchor}">{spans}</text>'
    )


def _block(lines: list[str]) -> tuple[float, int]:
    """Rendered (width, height) of a wrapped text block."""
    return max(_text_px(line) for line in lines), len(lines) * _LINE_HEIGHT


def render_svg(
    chart: Flowchart, *, title: str, description: str, id_prefix: str = "diagram"
) -> str:
    """Lay out ``chart`` so every node and edge label stays inside its shape
    and every element stays inside the SVG viewBox."""
    rank = _ranks(chart)
    layers: dict[int, list[str]] = {}
    for node in chart.nodes:
        layers.setdefault(rank[node], []).append(node)
    horizontal = chart.direction == "LR"

    # --- Node cells: every shape's text area must hold its wrapped label.
    # A diamond's largest inscribed rectangle is half its width and height,
    # so decision nodes need twice the text block (plus padding).
    wrapped = {node_id: wrap_label(node["label"]) for node_id, node in chart.nodes.items()}
    box_w, box_h = 80, 40
    for node_id, node in chart.nodes.items():
        text_w, text_h = _block(wrapped[node_id])
        if node["shape"] == "decision":
            need_w, need_h = 2 * text_w + 24, 2 * text_h + 20
        else:
            need_w, need_h = text_w + 24, text_h + 20
        box_w, box_h = max(box_w, need_w), max(box_h, need_h)

    # --- Edge labels: wrap, then size the gaps that hold them.
    edge_lines = {
        id(edge): wrap_label(edge["label"], _EDGE_LINE_PX)
        for edge in chart.edges if edge["label"]
    }
    label_w = max((_block(l)[0] for l in edge_lines.values()), default=0)
    label_h = max((_block(l)[1] for l in edge_lines.values()), default=0)
    routed = [
        edge for edge in chart.edges
        if rank[edge["target"]] != rank[edge["source"]] + 1
    ]
    straight_pairs: dict[tuple[str, str], int] = {}
    for edge in chart.edges:
        if edge not in routed:
            key = (edge["source"], edge["target"])
            straight_pairs[key] = straight_pairs.get(key, 0) + 1
    max_parallel = max(straight_pairs.values(), default=1)
    # Labels of straight edges sit in the gap between layers, stacked along
    # the main axis when edges are parallel.
    slot_main = (label_w + 8) if horizontal else (label_h + 4)
    gap_main = max(60, max_parallel * slot_main + 16) if edge_lines else 60
    # Labels of edges in neighbouring rows (LR) or columns (TD) share the
    # gap between two layers; space rows/columns so they cannot collide.
    gap_cross = 30
    if edge_lines:
        gap_cross = max(30, (label_h + 8) if horizontal else (label_w + 8))
    margin = 20
    # Lane labels sit beside their lane, so lanes are spaced to fit them.
    routed_labelled = any(id(edge) in edge_lines for edge in routed)
    lane_gap = _LANE_GAP
    if routed_labelled:
        lane_gap = max(_LANE_GAP, (label_h + 6) if horizontal else (label_w + 10))

    # Routed edges leave and enter nodes through short tracks in the gaps
    # between layers (never alongside a layer, where peers sit), so reserve
    # a track band on both sides of every gap and before the first layer.
    track_band = (6 + min(len(routed), _MAX_TRACKS) * 4) if routed else 0
    gap_main += 2 * track_band
    main_start = margin + track_band
    # In LR, straight-edge labels sit above their line; reserve room above
    # the first row so they never leave the viewBox.
    cross_start = margin + (label_h + 8 if horizontal and edge_lines else 0)
    pos: dict[str, tuple[float, float]] = {}
    for layer, members in layers.items():
        for index, node in enumerate(members):
            main = main_start + layer * ((box_w if horizontal else box_h) + gap_main)
            cross = cross_start + index * ((box_h if horizontal else box_w) + gap_cross)
            pos[node] = (main, cross) if horizontal else (cross, main)
    content_right = max(x for x, _ in pos.values()) + box_w
    content_bottom = max(y for _, y in pos.values()) + box_h
    lanes = {id(edge): index for index, edge in enumerate(routed)}

    extent = [content_right, content_bottom]

    def grow(x: float, y: float) -> None:
        extent[0], extent[1] = max(extent[0], x), max(extent[1], y)

    def label_svg(edge_id: int, x: float, y: float, anchor: str) -> str:
        lines = edge_lines[edge_id]
        width, height = _block(lines)
        left = {"start": x, "middle": x - width / 2, "end": x - width}[anchor]
        grow(left + width, y + height / 2)
        return _text_lines(x, y, lines, "edge-label", 11, anchor)

    title_id, desc_id, arrow_id = (
        f"{id_prefix}-title", f"{id_prefix}-desc", f"{id_prefix}-arrow"
    )
    body: list[str] = []
    parallel_seen: dict[tuple[str, str], int] = {}
    for edge in chart.edges:
        (sx, sy), (tx, ty) = pos[edge["source"]], pos[edge["target"]]
        marker = f' marker-end="url(#{arrow_id})"' if edge["arrow"] else ""
        if id(edge) in lanes:
            index = lanes[id(edge)]
            offset = 10 + index * lane_gap
            track = 6 + (index % _MAX_TRACKS) * 4
            if horizontal:
                # right side -> gap column -> lane below -> gap column -> left side
                lane = content_bottom + offset
                exit_y, entry_y = sy + box_h * 0.85, ty + box_h * 0.85
                out_x, in_x = sx + box_w + track, tx - track
                points = [(sx + box_w, exit_y), (out_x, exit_y), (out_x, lane),
                          (in_x, lane), (in_x, entry_y), (tx, entry_y)]
                label_at, anchor = ((out_x + in_x) / 2, lane + 3 + label_h / 2), "middle"
            else:
                # bottom -> gap row -> lane on the right -> gap row -> top
                lane = content_right + offset
                exit_x, entry_x = sx + box_w * 0.85, tx + box_w * 0.85
                out_y, in_y = sy + box_h + track, ty - track
                points = [(exit_x, sy + box_h), (exit_x, out_y), (lane, out_y),
                          (lane, in_y), (entry_x, in_y), (entry_x, ty)]
                label_at, anchor = (lane + 4, (out_y + in_y) / 2), "start"
            for px, py in points:
                grow(px, py)
            d = " ".join(
                f"{'M' if i == 0 else 'L'} {px:g} {py:g}" for i, (px, py) in enumerate(points)
            )
            body.append(
                f'<path class="edge" data-route="lane" d="{d}" fill="none" '
                f'stroke="#333"{marker}/>'
            )
        else:
            key = (edge["source"], edge["target"])
            nth = parallel_seen.get(key, 0)
            parallel_seen[key] = nth + 1
            count = straight_pairs[key]
            # Parallel lines: 0, +14, -14, +28, ... across the cross axis.
            spread = ((nth + 1) // 2) * _PARALLEL_GAP * (1 if nth % 2 else -1)
            x1, y1 = sx + box_w / 2, sy + box_h / 2
            x2, y2 = tx + box_w / 2, ty + box_h / 2
            if horizontal:
                x1, x2 = x1 + box_w / 2, x2 - box_w / 2
                y1, y2 = y1 + spread, y2 + spread
                mid = (x1 + x2) / 2 + (nth - (count - 1) / 2) * slot_main
                label_at, anchor = (mid, min(y1, y2) - 4 - label_h / 2), "middle"
            else:
                y1, y2 = y1 + box_h / 2, y2 - box_h / 2
                x1, x2 = x1 + spread, x2 + spread
                mid = (y1 + y2) / 2 + (nth - (count - 1) / 2) * slot_main
                label_at, anchor = (max(x1, x2) + 4, mid), "start"
            body.append(
                f'<line class="edge" x1="{x1:g}" y1="{y1:g}" x2="{x2:g}" '
                f'y2="{y2:g}" stroke="#333"{marker}/>'
            )
        if id(edge) in edge_lines:
            body.append(label_svg(id(edge), label_at[0], label_at[1], anchor))
    for node_id, node in chart.nodes.items():
        x, y = pos[node_id]
        if node["shape"] == "decision":
            cx, cy = x + box_w / 2, y + box_h / 2
            shape = (
                f'<polygon class="node" points="{cx:g},{y:g} {x + box_w:g},{cy:g} '
                f'{cx:g},{y + box_h:g} {x:g},{cy:g}" fill="#fff" stroke="#333"/>'
            )
        else:
            radius = ' rx="12"' if node["shape"] == "round" else ""
            shape = (
                f'<rect class="node" x="{x:g}" y="{y:g}" width="{box_w}" '
                f'height="{box_h}"{radius} fill="#fff" stroke="#333"/>'
            )
        body.append(shape)
        body.append(_text_lines(x + box_w / 2, y + box_h / 2, wrapped[node_id], "node-label", 12))

    width, height = extent[0] + margin, extent[1] + margin
    head = [
        f'<svg xmlns="http://www.w3.org/2000/svg" role="img" '
        f'font-family="{FONT_FAMILY}" '
        f'aria-labelledby="{title_id} {desc_id}" width="{width:g}" '
        f'height="{height:g}" viewBox="0 0 {width:g} {height:g}">',
        f'<title id="{title_id}">{escape(title)}</title>',
        f'<desc id="{desc_id}">{escape(description)}</desc>',
        f'<defs><marker id="{arrow_id}" viewBox="0 0 10 10" refX="10" refY="5" '
        'markerWidth="8" markerHeight="8" orient="auto-start-reverse">'
        '<path d="M 0 0 L 10 5 L 0 10 z" fill="#333"/></marker></defs>',
    ]
    return "\n".join(head + body + ["</svg>"])


class MermaidFlowchartRenderer:
    """``format_host`` renderer for DIAGRAM.

    The payload is the Mermaid source string, or a mapping with ``source`` and
    optional ``title`` / ``description`` strings. Element ids are derived from
    the content plus a per-renderer counter, so several SVGs returned by one
    renderer can be inlined in the same document without duplicate ids, while
    the same input to a fresh renderer gives identical output.
    """

    def __init__(self) -> None:
        self._count = 0

    def render(self, payload: Any) -> dict[str, Any]:
        if isinstance(payload, Mapping):
            source = payload.get("source")
            title = payload.get("title")
            description = payload.get("description")
        else:
            source, title, description = payload, None, None
        for name, value, limit in (
            ("title", title, MAX_TITLE_CHARS),
            ("description", description, MAX_DESCRIPTION_CHARS),
        ):
            if value is not None and (
                not isinstance(value, str) or not value.strip() or _XML_INVALID.search(value)
            ):
                raise DiagramSyntaxError(f"DIAGRAM_{name.upper()}_INVALID")
            if value is not None and len(value) > limit:
                raise DiagramSyntaxError(f"DIAGRAM_{name.upper()}_TOO_LONG")
        chart = parse_flowchart(source)
        summary = describe(chart)
        title_text = (title or "Flowchart").strip()
        desc_text = (description or summary).strip()
        self._count += 1
        digest = hashlib.sha256(
            "\x1f".join((source, title_text, desc_text)).encode("utf-8")
        ).hexdigest()[:10]
        svg = render_svg(
            chart,
            title=title_text,
            description=desc_text,
            id_prefix=f"diagram-{digest}-{self._count}",
        )
        return {
            "artifact": svg,
            "mime_type": "image/svg+xml",
            "node_count": len(chart.nodes),
            "edge_count": len(chart.edges),
            "summary": summary,
        }
