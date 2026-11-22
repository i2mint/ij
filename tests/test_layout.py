"""Tests for the layout algorithms: hierarchical layering, grid/circular, force-directed invariants."""

import math
import random

import pytest

from ij.core import DiagramIR, Edge, Node
from ij.layout.force_directed import ForceDirectedLayout
from ij.layout.hierarchical import HierarchicalLayout
from ij.layout.layout_engine import LayoutEngine


def _diagram(nodes, edges=()):
    d = DiagramIR()
    for n in nodes:
        d.add_node(Node(id=n, label=n))
    for s, t in edges:
        d.add_edge(Edge(source=s, target=t))
    return d


CHAIN = _diagram("abc", [("a", "b"), ("b", "c")])
DIAMOND = _diagram("abcd", [("a", "b"), ("a", "c"), ("b", "d"), ("c", "d")])


def test_hierarchical_layers_follow_edges_top_to_bottom():
    pos = HierarchicalLayout().compute(CHAIN)
    assert pos["a"][1] < pos["b"][1] < pos["c"][1]
    pos = HierarchicalLayout(layer_spacing=10).compute(CHAIN)
    assert pos["b"][1] - pos["a"][1] == 10


def test_hierarchical_diamond_has_three_layers_with_siblings_side_by_side():
    pos = HierarchicalLayout().compute(DIAMOND)
    assert pos["a"][1] < pos["b"][1] == pos["c"][1] < pos["d"][1]
    assert pos["b"][0] != pos["c"][0]


@pytest.mark.parametrize(
    "direction, axis, increasing",
    [("TB", 1, True), ("BT", 1, False), ("LR", 0, True), ("RL", 0, False)],
)
def test_hierarchical_directions(direction, axis, increasing):
    pos = HierarchicalLayout(direction=direction).compute(CHAIN)
    a, c = pos["a"][axis], pos["c"][axis]
    assert (a < c) is increasing


def test_hierarchical_cycle_and_empty():
    cyc = _diagram("ab", [("a", "b"), ("b", "a")])
    assert set(HierarchicalLayout().compute(cyc)) == {"a", "b"}  # no infinite loop
    assert HierarchicalLayout().compute(DiagramIR()) == {}


def test_engine_grid_layout():
    d = _diagram("abcde")
    pos = LayoutEngine("grid").apply(d)
    assert pos["a"] == (50, 50) and pos["b"] == (200, 50)
    assert pos["d"][1] == 150  # third column fits three, so the 4th node wraps to row 2
    assert len(set(pos.values())) == 5


def test_engine_circular_layout_is_equidistant_from_center():
    d = _diagram("abcd")
    pos = LayoutEngine("circular").apply(d)
    radius = max(200, 4 * 30)
    for x, y in pos.values():
        assert math.hypot(x - radius, y - radius) == pytest.approx(radius)


def test_engine_dispatch_and_unknown():
    assert set(LayoutEngine().apply(CHAIN)) == set("abc")  # hierarchical by default
    with pytest.raises(ValueError, match="Unknown algorithm"):
        LayoutEngine("nope").apply(CHAIN)
    pos = LayoutEngine("hierarchical", direction="LR").apply(CHAIN)
    assert pos["a"][0] < pos["c"][0]


def test_force_directed_places_every_node_and_pulls_neighbours_closer():
    random.seed(3)
    d = _diagram("abcdef", [("a", "b"), ("b", "c"), ("d", "e")])
    pos = ForceDirectedLayout(iterations=60).compute(d)
    assert set(pos) == set("abcdef")
    assert all(math.isfinite(x) and math.isfinite(y) for x, y in pos.values())
    dist = lambda u, v: math.dist(pos[u], pos[v])
    assert dist("a", "b") < dist("a", "f")  # connected beat unconnected, on this seed


def test_force_directed_is_seed_deterministic_and_handles_tiny_graphs():
    random.seed(1)
    p1 = ForceDirectedLayout(iterations=10).compute(CHAIN)
    random.seed(1)
    p2 = ForceDirectedLayout(iterations=10).compute(CHAIN)
    assert p1 == p2
    assert ForceDirectedLayout().compute(DiagramIR()) == {}
    assert len(ForceDirectedLayout(iterations=5).compute(_diagram("a"))) == 1
