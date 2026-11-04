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
    return (
        f"Flowchart ({direction}) with {len(chart.nodes)} nodes and "
        f"{len(chart.edges)} connections: " + "; ".join(parts) + "."
    )


_LINE_PX = 170          # wrap labels at this rendered width
_LINE_HEIGHT = 15
_LANE_GAP = 14
_PARALLEL_GAP = 14


def _char_px(char: str) -> int:
    """Approximate glyph width at 12px: wide (CJK) glyphs take ~12px."""
    return 12 if unicodedata.east_asian_width(char) in ("W", "F") else 7


def _text_px(text: str) -> int:
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


def _text_lines(x: float, y_center: float, lines: list[str], css_class: str, size: int) -> str:
    first_y = y_center - (len(lines) - 1) * _LINE_HEIGHT / 2 + 4
    spans = "".join(
        f'<tspan x="{x:g}" y="{first_y + i * _LINE_HEIGHT:g}">{escape(line)}</tspan>'
        for i, line in enumerate(lines)
    )
    return f'<text class="{css_class}" font-size="{size}" text-anchor="middle">{spans}</text>'


def render_svg(
    chart: Flowchart, *, title: str, description: str, id_prefix: str = "diagram"
) -> str:
    rank = _ranks(chart)
    layers: dict[int, list[str]] = {}
    for node in chart.nodes:
        layers.setdefault(rank[node], []).append(node)

    wrapped = {node_id: wrap_label(node["label"]) for node_id, node in chart.nodes.items()}
    widest = max(_text_px(line) for lines in wrapped.values() for line in lines)
    tallest = max(len(lines) for lines in wrapped.values())
    box_w = max(80, widest + 24)
    box_h = max(40, tallest * _LINE_HEIGHT + 20)
    gap_main, gap_cross, margin = 60, 30, 20
    horizontal = chart.direction == "LR"

    pos: dict[str, tuple[float, float]] = {}
    for layer, members in layers.items():
        for index, node in enumerate(members):
            main = margin + layer * ((box_w if horizontal else box_h) + gap_main)
            cross = margin + index * ((box_h if horizontal else box_w) + gap_cross)
            pos[node] = (main, cross) if horizontal else (cross, main)
    content_right = max(x for x, _ in pos.values()) + box_w
    content_bottom = max(y for _, y in pos.values()) + box_h

    # Only edges between adjacent layers are drawn straight. Back edges,
    # same-layer edges, self-loops and layer-skipping edges would cross
    # other nodes or overlap forward edges, so they get their own lane
    # beside the diagram (right side for TD, below for LR).
    routed = [
        edge for edge in chart.edges
        if rank[edge["target"]] != rank[edge["source"]] + 1
    ]
    lanes = {id(edge): index for index, edge in enumerate(routed)}
    lane_space = (len(routed) * _LANE_GAP + 10) if routed else 0
    width = content_right + margin + (0 if horizontal else lane_space)
    height = content_bottom + margin + (lane_space if horizontal else 0)

    title_id, desc_id, arrow_id = (
        f"{id_prefix}-title", f"{id_prefix}-desc", f"{id_prefix}-arrow"
    )
    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" role="img" '
        f'aria-labelledby="{title_id} {desc_id}" width="{width:g}" '
        f'height="{height:g}" viewBox="0 0 {width:g} {height:g}">',
        f'<title id="{title_id}">{escape(title)}</title>',
        f'<desc id="{desc_id}">{escape(description)}</desc>',
        f'<defs><marker id="{arrow_id}" viewBox="0 0 10 10" refX="10" refY="5" '
        'markerWidth="8" markerHeight="8" orient="auto-start-reverse">'
        '<path d="M 0 0 L 10 5 L 0 10 z" fill="#333"/></marker></defs>',
    ]
    # Straight edges with the same endpoints are spread across the cross
    # axis (0, +14, -14, +28, ...) so parallel branches and their labels
    # stay distinguishable.
    parallel_seen: dict[tuple[str, str], int] = {}
    for edge in chart.edges:
        (sx, sy), (tx, ty) = pos[edge["source"]], pos[edge["target"]]
        nth = parallel_seen.get((edge["source"], edge["target"]), 0)
        parallel_seen[(edge["source"], edge["target"])] = nth + 1
        spread = ((nth + 1) // 2) * _PARALLEL_GAP * (1 if nth % 2 else -1)
        marker = f' marker-end="url(#{arrow_id})"' if edge["arrow"] else ""
        if id(edge) in lanes:
            offset = 10 + lanes[id(edge)] * _LANE_GAP
            if horizontal:
                lane = content_bottom + offset
                x1, y1 = sx + box_w * 0.35, sy + box_h
                x2, y2 = tx + box_w * 0.65, ty + box_h
                points = [(x1, y1), (x1, lane), (x2, lane), (x2, y2)]
                label_at = ((x1 + x2) / 2, lane - 4)
            else:
                lane = content_right + offset
                x1, y1 = sx + box_w, sy + box_h * 0.35
                x2, y2 = tx + box_w, ty + box_h * 0.65
                points = [(x1, y1), (lane, y1), (lane, y2), (x2, y2)]
                label_at = (lane + 4, (y1 + y2) / 2)
            d = " ".join(
                f"{'M' if i == 0 else 'L'} {px:g} {py:g}" for i, (px, py) in enumerate(points)
            )
            out.append(
                f'<path class="edge" data-route="lane" d="{d}" fill="none" '
                f'stroke="#333"{marker}/>'
            )
            anchor = "middle" if horizontal else "start"
        else:
            x1, y1 = sx + box_w / 2, sy + box_h / 2
            x2, y2 = tx + box_w / 2, ty + box_h / 2
            if horizontal:
                x1, x2 = x1 + box_w / 2, x2 - box_w / 2
                y1, y2 = y1 + spread, y2 + spread
            else:
                y1, y2 = y1 + box_h / 2, y2 - box_h / 2
                x1, x2 = x1 + spread, x2 + spread
            out.append(
                f'<line class="edge" x1="{x1:g}" y1="{y1:g}" x2="{x2:g}" '
                f'y2="{y2:g}" stroke="#333"{marker}/>'
            )
            if horizontal:
                label_at, anchor = ((x1 + x2) / 2, (y1 + y2) / 2 - 4), "middle"
            else:
                # Stagger vertically too, so labels of parallel edges never overprint.
                label_at, anchor = ((x1 + x2) / 2 + 4, (y1 + y2) / 2 + 4 + nth * 12), "start"
        if edge["label"]:
            out.append(
                f'<text class="edge-label" x="{label_at[0]:g}" y="{label_at[1]:g}" '
                f'font-size="11" text-anchor="{anchor}">{escape(edge["label"])}</text>'
            )
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
        out.append(shape)
        out.append(_text_lines(x + box_w / 2, y + box_h / 2, wrapped[node_id], "node-label", 12))
    out.append("</svg>")
    return "\n".join(out)


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
        for name, value in (("title", title), ("description", description)):
            if value is not None and (
                not isinstance(value, str) or not value.strip() or _XML_INVALID.search(value)
            ):
                raise DiagramSyntaxError(f"DIAGRAM_{name.upper()}_INVALID")
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
