"""Tests for diagram parsers."""

import warnings

import pytest
from ij.parsers import MermaidParseWarning, MermaidParser
from ij.core import NodeType, EdgeType


def test_mermaid_parser_simple():
    """Test parsing simple Mermaid diagram."""
    mermaid_text = """
    flowchart TD
        n1([Start])
        n2[Process]
        n3([End])
        n1 --> n2
        n2 --> n3
    """

    parser = MermaidParser()
    diagram = parser.parse(mermaid_text)

    assert len(diagram.nodes) == 3
    assert len(diagram.edges) == 2
    assert diagram.validate()


def test_mermaid_parser_with_title():
    """Test parsing diagram with title."""
    mermaid_text = """
    ---
    title: My Process
    ---
    flowchart TD
        n1[Step 1]
    """

    parser = MermaidParser()
    diagram = parser.parse(mermaid_text)

    assert diagram.metadata["title"] == "My Process"


def test_mermaid_parser_node_shapes():
    """Test parsing different node shapes."""
    mermaid_text = """
    flowchart TD
        n1([Start])
        n2{Decision?}
        n3[(Database)]
        n4[[Subprocess]]
        n5[Process]
    """

    parser = MermaidParser()
    diagram = parser.parse(mermaid_text)

    nodes = {node.id: node for node in diagram.nodes}

    assert nodes["n1"].node_type == NodeType.START
    assert nodes["n2"].node_type == NodeType.DECISION
    assert nodes["n3"].node_type == NodeType.DATA
    assert nodes["n4"].node_type == NodeType.SUBPROCESS
    assert nodes["n5"].node_type == NodeType.PROCESS


def test_mermaid_parser_edges_with_labels():
    """Test parsing edges with labels."""
    mermaid_text = """
    flowchart TD
        n1[A]
        n2[B]
        n1 -->|Yes| n2
    """

    parser = MermaidParser()
    diagram = parser.parse(mermaid_text)

    assert len(diagram.edges) == 1
    edge = diagram.edges[0]
    assert edge.label == "Yes"
    assert edge.source == "n1"
    assert edge.target == "n2"


def test_mermaid_parser_edge_types():
    """Test parsing different edge types."""
    mermaid_text = """
    flowchart TD
        n1[A]
        n2[B]
        n3[C]
        n4[D]
        n1 --> n2
        n2 -.-> n3
        n3 <--> n4
    """

    parser = MermaidParser()
    diagram = parser.parse(mermaid_text)

    edges = diagram.edges
    assert edges[0].edge_type == EdgeType.DIRECT
    assert edges[1].edge_type == EdgeType.CONDITIONAL
    assert edges[2].edge_type == EdgeType.BIDIRECTIONAL


def test_mermaid_parser_direction():
    """Test parsing diagram direction."""
    mermaid_text = """
    flowchart LR
        n1[A] --> n2[B]
    """

    parser = MermaidParser()
    diagram = parser.parse(mermaid_text)

    assert diagram.metadata["direction"] == "LR"


def test_mermaid_parser_inline_node_definitions():
    """Test nodes defined inline on an edge line are kept, not dropped."""
    mermaid_text = """
    flowchart TD
        start([Start]) --> check_user{Is user authenticated?}
        check_user -->|Yes| show_dashboard[Show Dashboard]
    """

    parser = MermaidParser()
    diagram = parser.parse(mermaid_text)

    nodes = {node.id: node for node in diagram.nodes}
    assert set(nodes) == {"start", "check_user", "show_dashboard"}
    assert nodes["start"].node_type == NodeType.START
    assert nodes["check_user"].node_type == NodeType.DECISION
    assert nodes["check_user"].label == "Is user authenticated?"
    assert [(e.source, e.target, e.label) for e in diagram.edges] == [
        ("start", "check_user", None),
        ("check_user", "show_dashboard", "Yes"),
    ]
    assert diagram.validate()


def test_mermaid_parser_normalizes_llm_edge_label_drift():
    """Test the invalid `a --|Yes|--> b` edge-label spelling is normalized.

    Regression test for a real live-API failure: gpt-4o-mini emitted
    `check_user --|Yes|--> show_dashboard` (the valid Mermaid form is
    `check_user -->|Yes| show_dashboard`). The parser dropped the line without
    a word, and with it the `check_user{...}` decision node it referenced, so a
    diagram that should contain a DECISION node silently contained none.
    """
    mermaid_text = """
    flowchart TD
        start([Start]) --> check_user{Is user authenticated?}
        check_user --|Yes|--> show_dashboard([Show Dashboard])
        check_user --|No|--> show_login([Show Login])
    """

    parser = MermaidParser()
    with warnings.catch_warnings():
        # No line of this diagram may be dropped, silently or otherwise
        warnings.simplefilter("error")
        diagram = parser.parse(mermaid_text)

    assert parser.unparsed_lines == []

    decision_nodes = [n for n in diagram.nodes if n.node_type == NodeType.DECISION]
    assert [n.id for n in decision_nodes] == ["check_user"]
    assert [(e.source, e.target, e.label) for e in diagram.edges] == [
        ("start", "check_user", None),
        ("check_user", "show_dashboard", "Yes"),
        ("check_user", "show_login", "No"),
    ]
    assert diagram.validate()


def test_mermaid_parser_dash_delimited_edge_labels():
    """Test the `a -- label --> b` and `a -. label .-> b` Mermaid forms."""
    mermaid_text = """
    flowchart TD
        a[A] -- yes --> b[B]
        b -. maybe .-> c[C]
    """

    parser = MermaidParser()
    diagram = parser.parse(mermaid_text)

    assert [(e.source, e.target, e.label, e.edge_type) for e in diagram.edges] == [
        ("a", "b", "yes", EdgeType.DIRECT),
        ("b", "c", "maybe", EdgeType.CONDITIONAL),
    ]


def test_mermaid_parser_chained_edges():
    """Test a chained edge line yields one edge per link."""
    parser = MermaidParser()
    diagram = parser.parse("flowchart TD\n    a[A] --> b[B] --> c[C]")

    assert [(e.source, e.target) for e in diagram.edges] == [("a", "b"), ("b", "c")]
    assert diagram.validate()


def test_mermaid_parser_warns_on_unparseable_line():
    """Test an unreadable line is reported rather than silently dropped."""
    mermaid_text = """
    flowchart TD
        n1[Start]
        n1 ~~> n2 not mermaid at all
    """

    parser = MermaidParser()
    with pytest.warns(MermaidParseWarning, match="Could not parse Mermaid line"):
        diagram = parser.parse(mermaid_text)

    assert parser.unparsed_lines == ["n1 ~~> n2 not mermaid at all"]
    assert diagram.validate()


def test_mermaid_parser_strict_raises_on_unparseable_line():
    """Test strict=True turns an unreadable line into an error."""
    parser = MermaidParser(strict=True)

    with pytest.raises(ValueError, match="Could not parse Mermaid line"):
        parser.parse("flowchart TD\n    n1[Start]\n    n1 ~~> n2 nope")


def test_mermaid_parser_does_not_warn_on_valid_diagram():
    """Test valid Mermaid produces no spurious parse warnings."""
    mermaid_text = """
    ---
    title: Guarded
    ---
    graph TD
        %% a comment
        subgraph outer
        direction LR
        n1([Start]) --> n2{Ok?}
        n2 -->|Yes| n3[Done]
        end
        classDef hot fill:#f00
        style n1 fill:#0f0
    """

    parser = MermaidParser()
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        diagram = parser.parse(mermaid_text)

    assert parser.unparsed_lines == []
    # `graph` is Mermaid's legacy synonym for `flowchart`
    assert diagram.metadata["direction"] == "TD"
    assert diagram.metadata["title"] == "Guarded"
    assert diagram.validate()


def test_mermaid_parser_roundtrip():
    """Test roundtrip conversion: IR -> Mermaid -> IR."""
    from ij import DiagramIR, Node, Edge, NodeType
    from ij.renderers import MermaidRenderer

    # Create original diagram
    original = DiagramIR()
    original.add_node(Node(id="n1", label="Start", node_type=NodeType.START))
    original.add_node(Node(id="n2", label="Process", node_type=NodeType.PROCESS))
    original.add_node(Node(id="n3", label="End", node_type=NodeType.END))
    original.add_edge(Edge(source="n1", target="n2"))
    original.add_edge(Edge(source="n2", target="n3"))

    # Convert to Mermaid
    renderer = MermaidRenderer()
    mermaid_text = renderer.render(original)

    # Parse back
    parser = MermaidParser()
    parsed = parser.parse(mermaid_text)

    # Verify
    assert len(parsed.nodes) == len(original.nodes)
    assert len(parsed.edges) == len(original.edges)
    assert parsed.validate()
