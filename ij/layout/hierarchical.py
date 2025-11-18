"""Hierarchical (layered) graph layout algorithm."""

from collections import defaultdict, deque
from typing import Dict, List, Set, Tuple

from ..core import DiagramIR


class HierarchicalLayout:
    """Hierarchical layout using Sugiyama algorithm."""

    def __init__(
        self,
        direction: str = "TB",
        layer_spacing: float = 100,
        node_spacing: float = 150,
    ):
        """Initialize hierarchical layout.

        Args:
            direction: Layout direction ('TB', 'BT', 'LR', 'RL')
            layer_spacing: Spacing between layers
            node_spacing: Spacing between nodes in same layer
        """
        self.direction = direction
        self.layer_spacing = layer_spacing
        self.node_spacing = node_spacing

    def compute(self, diagram: DiagramIR) -> Dict[str, Tuple[float, float]]:
        """Compute node positions using hierarchical layout.

        Args:
            diagram: DiagramIR to layout

        Returns:
            Dictionary mapping node IDs to (x, y) positions
        """
        if not diagram.nodes:
            return {}

        # Build graph structure
        adj = defaultdict(list)
        in_degree = defaultdict(int)
        all_nodes = {node.id for node in diagram.nodes}

        for edge in diagram.edges:
            adj[edge.source].append(edge.target)
            in_degree[edge.target] += 1

        # Assign nodes to layers using topological sort
        layers = self._assign_layers(all_nodes, adj, in_degree)

        # Position nodes within layers
        positions = self._position_nodes(layers)

        return positions

    def _assign_layers(
        self, nodes: Set[str], adj: Dict, in_degree: Dict
    ) -> List[List[str]]:
        """Assign nodes to layers using topological ordering."""
        layers = []
        remaining = nodes.copy()
        processed = set()

        while remaining:
            # Find nodes with no incoming edges from unprocessed nodes
            current_layer = []
            for node in remaining:
                incoming_count = sum(
                    1
                    for pred in nodes
                    if node in adj.get(pred, []) and pred not in processed
                )
                if incoming_count == 0:
                    current_layer.append(node)

            if not current_layer:
                # Cycle detected or disconnected - add remaining nodes
                current_layer = list(remaining)

            layers.append(current_layer)
            processed.update(current_layer)
            remaining -= set(current_layer)

        return layers

    def _position_nodes(
        self, layers: List[List[str]]
    ) -> Dict[str, Tuple[float, float]]:
        """Position nodes based on layer assignment."""
        positions = {}

        for layer_idx, layer in enumerate(layers):
            layer_size = len(layer)

            for node_idx, node_id in enumerate(layer):
                if self.direction in ["TB", "BT"]:
                    # Top-to-bottom or bottom-to-top
                    x = (node_idx - layer_size / 2) * self.node_spacing + 300
                    y = layer_idx * self.layer_spacing + 50

                    if self.direction == "BT":
                        y = (len(layers) - layer_idx - 1) * self.layer_spacing + 50

                    positions[node_id] = (x, y)

                else:  # LR or RL
                    # Left-to-right or right-to-left
                    x = layer_idx * self.layer_spacing + 50
                    y = (node_idx - layer_size / 2) * self.node_spacing + 300

                    if self.direction == "RL":
                        x = (len(layers) - layer_idx - 1) * self.layer_spacing + 50

                    positions[node_id] = (x, y)

        return positions
