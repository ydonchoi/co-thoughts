import xml.etree.ElementTree as ET

import pytest

from diagram_renderer import (
    MAX_LABEL_CHARS,
    MAX_NODES,
    DiagramSyntaxError,
    MermaidFlowchartRenderer,
    parse_flowchart,
)
from explanation_format_router import route_explanation_format
from format_host import FormatHost, RendererRegistry

SVG = "{http://www.w3.org/2000/svg}"

APPROVAL = """flowchart TD
  %% approval process
  A[Request received] --> B{Review}
  B -->|approve| C(Done)
  B -- reject --> A
"""


def _texts(root, css_class):
    """Text of each element; wrapped lines (``<tspan>``) are joined by spaces."""
    return [" ".join(span.text for span in el) if el.find(f"{SVG}tspan") is not None
            else el.text for el in root if el.get("class") == css_class]


def _svg(source, **extra):
    payload = {"source": source, **extra} if extra else source
    output = MermaidFlowchartRenderer().render(payload)
    return output, ET.fromstring(output["artifact"])


# --- Parsing ---

def test_parses_nodes_shapes_edges_and_labels():
    chart = parse_flowchart(APPROVAL)
    assert chart.direction == "TD"
    assert chart.nodes["A"]["label"] == "Request received"
    assert chart.nodes["B"]["shape"] == "decision"
    assert chart.nodes["C"]["shape"] == "round"
    assert [(e["source"], e["target"], e["arrow"], e["label"]) for e in chart.edges] == [
        ("A", "B", True, None),
        ("B", "C", True, "approve"),
        ("B", "A", True, "reject"),
    ]


def test_chains_lines_semicolons_hyphenated_ids_and_lr():
    chart = parse_flowchart('graph LR\n  a-1-->b --- c; d ; e[" quoted "]')
    assert chart.direction == "LR"
    assert list(chart.nodes) == ["a-1", "b", "c", "d", "e"]
    assert chart.nodes["e"]["label"] == "quoted"
    assert [e["arrow"] for e in chart.edges] == [True, False]


def test_tb_is_top_down_and_header_is_case_insensitive():
    assert parse_flowchart("FLOWCHART TB\nA").direction == "TD"


def test_bare_reference_keeps_earlier_label():
    chart = parse_flowchart("graph TD\nA[Start] --> B\nB --> A")
    assert chart.nodes["A"]["label"] == "Start"
    assert chart.nodes["B"]["label"] == "B"


def test_later_definition_labels_an_implicit_node():
    chart = parse_flowchart("graph TD\nA --> B\nB[Finish]")
    assert chart.nodes["B"]["label"] == "Finish"


@pytest.mark.parametrize("source, code", [
    ("", "DIAGRAM_SOURCE_REQUIRED"),
    (None, "DIAGRAM_SOURCE_REQUIRED"),
    ("%% only a comment", "DIAGRAM_SOURCE_REQUIRED"),
    ("sequenceDiagram\nA->>B: hi", "DIAGRAM_HEADER_UNSUPPORTED"),
    ("graph RL\nA --> B", "DIAGRAM_HEADER_UNSUPPORTED"),
    ("graph TD", "DIAGRAM_EMPTY"),
    ("graph TD\nA ==> B", "DIAGRAM_SYNTAX_UNSUPPORTED"),
    ("graph TD\nA --> B & C", "DIAGRAM_SYNTAX_UNSUPPORTED"),
    ("graph TD\nA -->", "DIAGRAM_SYNTAX_UNSUPPORTED"),
    ("graph TD\nsubgraph S\nA\nend", "DIAGRAM_SYNTAX_UNSUPPORTED"),
    ("graph TD\nA[]", "DIAGRAM_EMPTY_LABEL"),
    ("graph TD\nA -->|| B", "DIAGRAM_EMPTY_LABEL"),
    ("graph TD\nA[x] --> A[y]", "DIAGRAM_NODE_REDEFINED:A"),
    ("graph TD\nA[x] --> A(x)", "DIAGRAM_NODE_REDEFINED:A"),
    (f"graph TD\nA[{'x' * (MAX_LABEL_CHARS + 1)}]", "DIAGRAM_LABEL_TOO_LONG"),
    ("graph TD\n" + "\n".join(f"n{i}" for i in range(MAX_NODES + 1)), "DIAGRAM_TOO_MANY_NODES"),
    ("graph TD\n" + "A" * 20_001, "DIAGRAM_SOURCE_TOO_LONG"),
])
def test_unsupported_or_invalid_source_is_rejected(source, code):
    with pytest.raises(DiagramSyntaxError, match=code):
        parse_flowchart(source)


# --- Rendering and output validity ---

def test_render_output_is_well_formed_svg_with_one_shape_per_node():
    output, root = _svg(APPROVAL)
    assert output["mime_type"] == "image/svg+xml"
    assert (output["node_count"], output["edge_count"]) == (3, 3)
    assert root.tag == f"{SVG}svg"
    shapes = [el for el in root if el.get("class") == "node"]
    assert len(shapes) == 3
    assert len([el for el in root if el.get("class") == "edge"]) == 3
    assert _texts(root, "node-label") == ["Request received", "Review", "Done"]
    assert _texts(root, "edge-label") == ["approve", "reject"]


def test_render_is_deterministic():
    assert _svg(APPROVAL)[0]["artifact"] == _svg(APPROVAL)[0]["artifact"]


def test_lr_layout_places_successors_to_the_right():
    _, root = _svg("graph LR\nA --> B --> C")
    xs = [float(el.get("x")) for el in root if el.get("class") == "node"]
    assert xs == sorted(xs) and len(set(xs)) == 3


def test_td_layout_places_successors_below():
    _, root = _svg("graph TD\nA --> B --> C")
    ys = [float(el.get("y")) for el in root if el.get("class") == "node"]
    assert ys == sorted(ys) and len(set(ys)) == 3


def test_cycles_terminate():
    output, _ = _svg("graph TD\nA --> B --> C --> A")
    assert output["edge_count"] == 3


def test_line_edges_have_no_arrowhead():
    _, root = _svg("graph TD\nA --- B\nB --> C")
    edges = [el for el in root if el.get("class") == "edge"]
    assert edges[0].get("marker-end") is None
    marker_id = root.find(f"{SVG}defs/{SVG}marker").get("id")
    assert edges[1].get("marker-end") == f"url(#{marker_id})"


def test_labels_are_escaped_not_injected():
    output, root = _svg('graph TD\nA["<script>x</script> & co"]')
    assert "<script>" not in output["artifact"]
    assert _texts(root, "node-label") == ["<script>x</script> & co"]


def test_korean_labels_render():
    _, root = _svg("flowchart TD\nA[요청 접수] -->|승인| B(완료)")
    assert _texts(root, "node-label") == ["요청 접수", "완료"]


# --- Accessibility: <title>/<desc> ---

def test_svg_has_title_desc_and_img_role_with_generated_summary():
    output, root = _svg(APPROVAL)
    assert root.get("role") == "img"
    title, desc_el = root.find(f"{SVG}title"), root.find(f"{SVG}desc")
    assert root.get("aria-labelledby") == f"{title.get('id')} {desc_el.get('id')}"
    assert title.text == "Flowchart"
    desc = root.find(f"{SVG}desc").text
    assert desc == output["summary"]
    assert desc.startswith("Flowchart (top-down) with 3 nodes and 3 connections:")
    assert "Review → Done (approve)" in desc


def test_payload_title_and_description_are_used_and_escaped():
    _, root = _svg(APPROVAL, title="Approval <flow>", description="Steps & checks")
    assert root.find(f"{SVG}title").text == "Approval <flow>"
    assert root.find(f"{SVG}desc").text == "Steps & checks"


@pytest.mark.parametrize("extra", [{"title": " "}, {"description": 3}])
def test_invalid_title_or_description_is_rejected(extra):
    with pytest.raises(DiagramSyntaxError):
        MermaidFlowchartRenderer().render({"source": APPROVAL, **extra})


def test_isolated_nodes_are_listed_in_summary():
    output, _ = _svg("graph TD\nA --> B\nC[Alone]")
    assert output["summary"].endswith("A → B; Alone.")


# --- Registration with format_host (§13.3 item 5) ---

def _diagram_host():
    registry = RendererRegistry()
    registry.register("DIAGRAM", MermaidFlowchartRenderer())
    return FormatHost(registry)


def test_registered_renderer_is_declared_and_delivers_svg():
    host = _diagram_host()
    assert host.capabilities()["diagram"] is True
    plan = route_explanation_format(host.prepare_request({
        "task": "Draw a flowchart of the approval process",
        "output_intent": {"accessibility": {"screen_reader": True}},
    }))
    record = host.deliver(plan, {
        "text": "1. Request received. 2. Review. 3. Done or back to request.",
        "media": {"DIAGRAM": APPROVAL},
        "text_alternative": "Approval flow: request, review, then done or rejected back to request.",
    })
    assert record["delivered_format"] == "DIAGRAM"
    assert record["render_status"] == "SUCCEEDED"
    assert record["accessibility_status"] == {"TEXT_ALTERNATIVE": "MET"}
    assert record["renderer_metadata"]["mime_type"] == "image/svg+xml"
    ET.fromstring(record["artifact"])
    # Rendering never verifies the diagram's content.
    assert record["verification_status"] == "UNVERIFIED"
    assert record["is_evidence"] is False


def test_unsupported_source_falls_back_to_text_through_the_host():
    host = _diagram_host()
    plan = route_explanation_format(host.prepare_request({
        "task": "Draw a flowchart of the approval process",
    }))
    record = host.deliver(plan, {"text": "Steps...", "media": {"DIAGRAM": "sequenceDiagram\nA->>B: hi"}})
    assert record["render_status"] == "FAILED"
    assert record["fallback_reason"] == "RENDER_FAILED:DiagramSyntaxError"
    assert record["delivered_format"] == "TEXT"
    assert record["text"] == "Steps..."


def test_missing_text_alternative_blocks_svg_before_rendering():
    host = _diagram_host()
    plan = route_explanation_format(host.prepare_request({
        "task": "Draw a flowchart of the approval process",
        "output_intent": {"accessibility": {"screen_reader": True}},
    }))
    record = host.deliver(plan, {"text": "Steps...", "media": {"DIAGRAM": APPROVAL}})
    assert record["accessibility_status"] == {"TEXT_ALTERNATIVE": "NOT_MET"}
    assert record["render_status"] == "NOT_RUN"
    assert record["delivered_format"] == "TEXT"


# --- Review follow-ups (PR #28) ---

def test_long_labels_wrap_inside_their_box():
    from diagram_renderer import _text_px
    label = " ".join(["word"] * 40)                     # 199 characters
    _, root = _svg(f"graph TD\nA[{label}] --> B[{'x' * 120}]")
    box = next(el for el in root if el.get("class") == "node")
    box_w, box_h = float(box.get("width")), float(box.get("height"))
    for text in (el for el in root if el.get("class") == "node-label"):
        spans = list(text)
        assert len(spans) > 1                           # wrapped, not one long line
        assert all(_text_px(span.text) <= box_w - 20 for span in spans)
        assert len(spans) * 15 <= box_h
    assert " ".join(_texts(root, "node-label")[0].split()) == label


def test_wide_cjk_labels_are_measured_wider():
    from diagram_renderer import wrap_label
    assert len(wrap_label("가" * 30)) > len(wrap_label("a" * 30))


@pytest.mark.parametrize("source", [
    "graph TD\nA --> B --> C --> A",      # back edge
    "graph TD\nA --> B --> C\nA --> C",   # layer-skipping edge
    "graph TD\nA --> A",                  # self-loop
    "graph LR\nA --> B --> C --> A",
])
def test_non_adjacent_edges_are_routed_in_a_side_lane(source):
    _, root = _svg(source)
    nodes = [el for el in root if el.get("class") == "node"]
    right = max(float(n.get("x")) + float(n.get("width")) for n in nodes)
    bottom = max(float(n.get("y")) + float(n.get("height")) for n in nodes)
    lanes = [el for el in root if el.get("data-route") == "lane"]
    assert len(lanes) == 1
    coords = [float(v) for v in lanes[0].get("d").replace("M", "").replace("L", "").split()]
    if source.startswith("graph LR"):
        assert max(coords[1::2]) > bottom              # goes below every node
    else:
        assert max(coords[0::2]) > right               # goes right of every node
    straight = [el for el in root if el.get("class") == "edge" and el.tag == f"{SVG}line"]
    assert all(el.get("data-route") is None for el in straight)


def test_ids_are_unique_across_svgs_from_one_renderer():
    renderer = MermaidFlowchartRenderer()
    ids = []
    for _ in range(2):
        root = ET.fromstring(renderer.render(APPROVAL)["artifact"])
        ids += [el.get("id") for el in root.iter() if el.get("id")]
    assert len(ids) == len(set(ids)) == 6


def test_different_diagrams_get_different_ids_even_from_fresh_renderers():
    a = ET.fromstring(MermaidFlowchartRenderer().render("graph TD\nA --> B")["artifact"])
    b = ET.fromstring(MermaidFlowchartRenderer().render("graph TD\nC --> D")["artifact"])
    assert a.find(f"{SVG}title").get("id") != b.find(f"{SVG}title").get("id")


@pytest.mark.parametrize("source", [
    "graph TD\nA---oB", "graph TD\nA---xB", "graph TD\nA-->oB", "graph TD\nA-->xB",
    "graph TD\nA -- yes ---oB",
])
def test_circle_and_cross_edges_are_rejected(source):
    with pytest.raises(DiagramSyntaxError, match="DIAGRAM_EDGE_UNSUPPORTED"):
        parse_flowchart(source)


def test_ids_starting_with_o_or_x_still_work_after_a_space():
    chart = parse_flowchart("graph TD\nA --- open --> xray")
    assert list(chart.nodes) == ["A", "open", "xray"]


@pytest.mark.parametrize("payload", [
    'graph TD\nA["bad\x01char"]',
    {"source": "graph TD\nA", "title": "bad\x0btitle"},
    {"source": "graph TD\nA", "description": "bad\ufffe"},
])
def test_xml_invalid_characters_are_rejected(payload):
    with pytest.raises(DiagramSyntaxError, match="INVALID"):
        MermaidFlowchartRenderer().render(payload)


def test_semicolons_inside_labels_are_kept():
    chart = parse_flowchart('graph TD\nA["Check; retry"] -->|yes; once| B[x;y]; C')
    assert chart.nodes["A"]["label"] == "Check; retry"
    assert chart.nodes["B"]["label"] == "x;y"
    assert chart.edges[0]["label"] == "yes; once"
    assert list(chart.nodes) == ["A", "B", "C"]


# --- Review follow-ups, second round (PR #28) ---

@pytest.mark.parametrize("source, edges", [
    ("graph TD; A --> B", 1),
    ("graph TD;A-->B;B-->C", 2),
    ("flowchart LR ; A --- B", 1),
])
def test_statements_may_follow_the_header_on_the_same_line(source, edges):
    assert len(parse_flowchart(source).edges) == edges


def test_header_only_with_trailing_semicolon_is_still_empty():
    with pytest.raises(DiagramSyntaxError, match="DIAGRAM_EMPTY"):
        parse_flowchart("graph TD;")


@pytest.mark.parametrize("direction", ["TD", "LR"])
def test_parallel_edges_and_labels_are_separated(direction):
    _, root = _svg(f"graph {direction}\nA -->|yes| B\nA -->|no| B\nA --> B")
    lines = [el for el in root if el.get("class") == "edge"]
    coords = {tuple(el.get(k) for k in ("x1", "y1", "x2", "y2")) for el in lines}
    assert len(coords) == 3                              # three distinct lines
    labels = [(el[0].get("x"), el[0].get("y")) for el in root if el.get("class") == "edge-label"]
    assert len(labels) == len(set(labels)) == 2
    if direction == "TD":
        ys = sorted(float(y) for _, y in labels)
        assert ys[1] - ys[0] >= 11                       # stacked, no overprinting
    else:
        xs = sorted(float(x) for x, _ in labels)
        assert xs[1] - xs[0] >= 20                       # side by side, no overprinting


# --- Review follow-ups, third round (PR #28): text stays inside shapes and viewBox ---

def _text_boxes(root, css_class):
    """Approximate rendered boxes of each text element (per tspan)."""
    from diagram_renderer import _text_px
    boxes = []
    for el in root:
        if el.get("class") != css_class:
            continue
        anchor = el.get("text-anchor")
        for span in el:
            x, y, w = float(span.get("x")), float(span.get("y")), _text_px(span.text)
            left = {"start": x, "middle": x - w / 2, "end": x - w}[anchor]
            boxes.append((left, y - 11, left + w, y + 3))
    return boxes


def _assert_inside_viewbox(root):
    width, height = float(root.get("width")), float(root.get("height"))
    for cls in ("node-label", "edge-label"):
        for left, top, right, bottom in _text_boxes(root, cls):
            assert left >= 0 and top >= 0 and right <= width and bottom <= height


def test_decision_label_fits_inside_the_diamond():
    _, root = _svg("graph TD\nA{" + " ".join(["decide"] * 20) + "}")
    points = [tuple(map(float, p.split(","))) for p in
              next(el for el in root if el.get("class") == "node").get("points").split()]
    (cx, top), (right, cy) = points[0], points[1]
    half_w, half_h = right - cx, cy - top
    for left, t, r, b in _text_boxes(root, "node-label"):
        for x, y in ((left, t), (r, t), (left, b), (r, b)):
            # |dx|/half_w + |dy|/half_h <= 1  <=> point inside the diamond
            assert abs(x - cx) / half_w + abs(y - cy) / half_h <= 1.0


@pytest.mark.parametrize("source", [
    "graph TD\nA -->|" + " ".join(["label"] * 30) + "| B",
    "graph LR\nA -->|" + " ".join(["label"] * 30) + "| B",
    "graph TD\nA --> B --> C\nC -->|" + " ".join(["back"] * 40) + "| A",
    "graph LR\nA --> B --> C\nC -->|" + " ".join(["back"] * 40) + "| A",
    "graph TD\nA -->|" + "가" * 150 + "| B\nA -->|짧음| B",
])
def test_long_edge_labels_wrap_and_stay_inside_the_viewbox(source):
    _, root = _svg(source)
    edge_labels = [el for el in root if el.get("class") == "edge-label"]
    assert any(len(list(el)) > 1 for el in edge_labels)  # wrapped
    _assert_inside_viewbox(root)


def test_edge_labels_do_not_overlap_nodes():
    _, root = _svg("graph TD\nA[Start] -->|" + " ".join(["word"] * 25) + "| B[End]")
    nodes = [(float(n.get("x")), float(n.get("y")),
              float(n.get("x")) + float(n.get("width")), float(n.get("y")) + float(n.get("height")))
             for n in root if n.get("class") == "node"]
    for left, top, right, bottom in _text_boxes(root, "edge-label"):
        for nl, nt, nr, nb in nodes:
            assert right <= nl or left >= nr or bottom <= nt or top >= nb


@pytest.mark.parametrize("direction", ["TD", "LR"])
def test_labels_of_edges_in_neighbouring_rows_do_not_collide(direction):
    long = " ".join(["word"] * 12)
    _, root = _svg(f"graph {direction}\nA --> B -->|{long}| D\nA --> C -->|{long}| E")
    boxes = _text_boxes(root, "edge-label")
    by_element = []
    for el in (e for e in root if e.get("class") == "edge-label"):
        spans = _text_boxes(ET.fromstring(f'<svg xmlns="http://www.w3.org/2000/svg">{ET.tostring(el, encoding="unicode")}</svg>'), "edge-label")
        by_element.append((min(b[0] for b in spans), min(b[1] for b in spans),
                           max(b[2] for b in spans), max(b[3] for b in spans)))
    (l1, t1, r1, b1), (l2, t2, r2, b2) = by_element
    assert r1 <= l2 or r2 <= l1 or b1 <= t2 or b2 <= t1
    assert boxes
    _assert_inside_viewbox(root)
