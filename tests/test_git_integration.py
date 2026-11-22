"""Tests for DiagramDiff, DiagramChanges, merge strategies and DiagramHistory."""

import pytest

from ij.core import DiagramIR, Edge, Node, NodeType
from ij.git_integration import DiagramChanges, DiagramDiff, DiagramHistory


def D(nodes, edges=(), types=None):
    d = DiagramIR()
    for n, label in nodes:
        d.add_node(Node(id=n, label=label, node_type=(types or {}).get(n, NodeType.PROCESS)))
    for s, t, *lab in edges:
        d.add_edge(Edge(source=s, target=t, label=(lab[0] if lab else None)))
    return d


OLD = D([("a", "A"), ("b", "B")], [("a", "b")])
NEW = D([("a", "A2"), ("c", "C")], [("a", "c", "go")], types={"a": NodeType.DECISION})


def test_changes_counters():
    assert not DiagramChanges().has_changes and DiagramChanges().total_changes == 0
    c = DiagramDiff().compare(OLD, NEW)
    assert c.has_changes and c.total_changes == 5
    assert [n.id for n in c.added_nodes] == ["c"] and [n.id for n in c.removed_nodes] == ["b"]
    assert c.modified_nodes[0][0].label == "A" and c.modified_nodes[0][1].label == "A2"
    assert (c.added_edges[0].source, c.added_edges[0].target) == ("a", "c")
    assert (c.removed_edges[0].source, c.removed_edges[0].target) == ("a", "b")


def test_identical_diagrams_have_no_changes():
    differ = DiagramDiff()
    c = differ.compare(OLD, OLD)
    assert not c.has_changes
    assert differ.generate_diff_report(c) == "No changes detected."


def test_edge_label_change_is_remove_plus_add():
    a = D([("x", "X"), ("y", "Y")], [("x", "y", "old")])
    b = D([("x", "X"), ("y", "Y")], [("x", "y", "new")])
    c = DiagramDiff().compare(a, b)
    assert len(c.added_edges) == 1 and len(c.removed_edges) == 1


def test_report_lists_every_section():
    report = DiagramDiff().generate_diff_report(DiagramDiff().compare(OLD, NEW))
    for expected in [
        "Total changes: 5", "+ c: C [process]", "- b: B [process]", "~ a:",
        "label: A → A2", "type: process → decision", "+ a → c (go)", "- a → b",
    ]:
        assert expected in report


def test_compare_files_picks_parser_by_extension(tmp_path):
    f1, f2 = tmp_path / "one.mmd", tmp_path / "two.mmd"
    f1.write_text("graph TD\n    A[Start] --> B[End]\n")
    f2.write_text("graph TD\n    A[Start] --> B[End]\n    B --> C[More]\n")
    c = DiagramDiff().compare_files(str(f1), str(f2))
    assert [n.id for n in c.added_nodes] == ["C"]
    d2 = tmp_path / "x.d2"
    d2.write_text("a -> b\n")
    assert DiagramDiff()._parse_file(str(d2)) is not None
    unknown = tmp_path / "y.txt"  # falls back to mermaid
    unknown.write_text("graph TD\n    A --> B\n")
    assert len(DiagramDiff()._parse_file(str(unknown)).nodes) == 2


def test_merge_strategies():
    base = D([("a", "A")])
    b1 = D([("a", "A"), ("b", "B")], [("a", "b")])
    b2 = D([("a", "A-new"), ("c", "C")], [("a", "c")])
    differ = DiagramDiff()
    assert differ.merge(base, b1, b2, "ours") is b1
    assert differ.merge(base, b1, b2, "theirs") is b2
    union = differ.merge(base, b1, b2)
    assert {n.id for n in union.nodes} == {"a", "b", "c"}
    assert union.get_node("a").label == "A-new"  # branch2 wins conflicts
    assert len(union.edges) == 2
    inter = differ.merge(base, b1, b2, "intersection")
    assert {n.id for n in inter.nodes} == {"a"} and inter.edges == []
    with pytest.raises(ValueError, match="Unknown merge strategy"):
        differ.merge(base, b1, b2, "random")


def test_union_merge_dedupes_identical_edges():
    a = D([("a", "A"), ("b", "B")], [("a", "b")])
    merged = DiagramDiff().merge(a, a, a)
    assert len(merged.edges) == 1


def test_intersection_keeps_shared_edges():
    b1 = D([("a", "A"), ("b", "B")], [("a", "b")])
    b2 = D([("a", "A"), ("b", "B")], [("a", "b")])
    merged = DiagramDiff().merge(D([]), b1, b2, "intersection")
    assert len(merged.nodes) == 2 and len(merged.edges) == 1


def test_history_versions_compare_and_changelog():
    h = DiagramHistory()
    assert h.get_changelog() == "No version history to compare"
    h.add_version("v1", OLD)
    h.add_version("v2", NEW)
    h.add_version("v3", NEW)
    assert h.list_versions() == ["v1", "v2", "v3"]
    assert h.get_version("v2") is NEW and h.get_version("nope") is None
    assert h.compare_versions("v1", "v2").total_changes == 5
    with pytest.raises(ValueError, match="Version not found: zzz"):
        h.compare_versions("v1", "zzz")
    with pytest.raises(ValueError, match="Version not found: zzz"):
        h.compare_versions("zzz", "v1")
    log = h.get_changelog()
    assert "Changelog (3 versions)" in log and "v1 → v2" in log
    assert "Nodes: +1 -1 ~1" in log and "Edges: +1 -1" in log
    assert "v2 → v3" not in log  # unchanged step is omitted
