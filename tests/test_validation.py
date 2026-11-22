"""Tests for DiagramValidator rules and DiagramLinter."""

import pytest

from ij.core import DiagramIR, Edge, Node, NodeType
from ij.validation import DiagramLinter, DiagramValidator, Severity


def D(nodes, edges=(), types=None, meta=None):
    d = DiagramIR()
    for n in nodes:
        d.add_node(Node(id=n, label=n, node_type=(types or {}).get(n, NodeType.PROCESS)))
    for s, t in edges:
        d.add_edge(Edge(source=s, target=t))
    if meta:
        d.metadata.update(meta)
    return d


def check(diagram, rule):
    result = DiagramValidator().validate(diagram, [rule])
    return result.is_valid, [(i.severity, i.rule) for i in result.issues]


def test_orphaned_nodes_warn():
    valid, issues = check(D("abc", [("a", "b")]), "no-orphaned-nodes")
    assert valid and issues == [(Severity.WARNING, "no-orphaned-nodes")]
    assert check(D("ab", [("a", "b")]), "no-orphaned-nodes") == (True, [])


def test_cycles_are_errors():
    assert check(D("ab", [("a", "b"), ("b", "a")]), "no-cycles") == (
        False, [(Severity.ERROR, "no-cycles")],
    )
    assert check(D("ab", [("a", "b")]), "no-cycles") == (True, [])


def test_require_start_and_end():
    valid, issues = check(D("ab", [("a", "b")]), "require-start-end")
    assert not valid and len(issues) == 2
    typed = D("ab", [("a", "b")], types={"a": NodeType.START, "b": NodeType.END})
    assert check(typed, "require-start-end") == (True, [])


def test_unique_ids_and_labels():
    d = D("ab")
    d.nodes.append(Node(id="a", label="other"))
    assert check(d, "unique-node-ids") == (False, [(Severity.ERROR, "unique-node-ids")])
    d = D("ab")
    d.nodes[1].label = "a"
    assert check(d, "unique-labels") == (True, [(Severity.INFO, "unique-labels")])
    assert check(D("ab"), "unique-labels") == (True, [])


def test_valid_edges_self_loops_and_connectivity():
    assert check(D("ab", [("a", "ghost")]), "valid-edges") == (
        False, [(Severity.ERROR, "valid-edges")],
    )
    assert check(D("ab", [("a", "a")]), "no-self-loops") == (
        True, [(Severity.WARNING, "no-self-loops")],
    )
    assert check(D("abcd", [("a", "b"), ("c", "d")]), "connected-graph") == (
        True, [(Severity.WARNING, "connected-graph")],
    )
    assert check(D("abc", [("a", "b"), ("b", "c")]), "connected-graph") == (True, [])


def test_parameterised_limits():
    d = D("abc", [("a", "b"), ("b", "c")])
    result = DiagramValidator().validate(d, ["max-nodes-2", "max-edges-1"])
    assert not result.is_valid
    assert [i.rule for i in result.errors] == ["max-nodes-2", "max-edges-1"]
    ok = DiagramValidator().validate(d, ["max-nodes-10", "max-edges-10"])
    assert ok.is_valid and ok.issues == []
    # malformed or unknown rule names are ignored, not fatal
    ignored = DiagramValidator().validate(d, ["max-nodes-x", "max-edges-", "no-such-rule"])
    assert ignored.is_valid and ignored.issues == []


def test_all_rules_by_default_and_result_views():
    result = DiagramValidator().validate(D("ab"))
    assert set(i.rule for i in result.issues) >= {"require-start-end", "no-orphaned-nodes"}
    assert not result.is_valid
    assert all(i.severity == Severity.ERROR for i in result.errors)
    assert all(i.severity == Severity.WARNING for i in result.warnings)


def test_linter():
    long_label = D(["x"] + ["n%d" % i for i in range(7)])
    long_label.nodes[0].label = "x" * 60
    rules = [i.rule for i in DiagramLinter().lint(long_label)]
    assert rules == ["label-length", "naming-conventions", "metadata-title"]
    titled = D("ab", meta={"title": "Orders"})
    assert DiagramLinter().lint(titled) == []
    assert [i.rule for i in DiagramLinter().lint(D("ab", meta={"title": ""}))] == ["metadata-title"]
