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
    labels = [el.text for el in root if el.get("class") == "node-label"]
    assert labels == ["Request received", "Review", "Done"]
    assert [el.text for el in root if el.get("class") == "edge-label"] == ["approve", "reject"]


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
    assert edges[1].get("marker-end") == "url(#arrow)"


def test_labels_are_escaped_not_injected():
    output, root = _svg('graph TD\nA["<script>alert(1)</script> & co"]')
    assert "<script>" not in output["artifact"]
    labels = [el.text for el in root if el.get("class") == "node-label"]
    assert labels == ["<script>alert(1)</script> & co"]


def test_korean_labels_render():
    _, root = _svg("flowchart TD\nA[요청 접수] -->|승인| B(완료)")
    assert [el.text for el in root if el.get("class") == "node-label"] == ["요청 접수", "완료"]


# --- Accessibility: <title>/<desc> ---

def test_svg_has_title_desc_and_img_role_with_generated_summary():
    output, root = _svg(APPROVAL)
    assert root.get("role") == "img"
    assert root.get("aria-labelledby") == "diagram-title diagram-desc"
    assert root.find(f"{SVG}title").text == "Flowchart"
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
