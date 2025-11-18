"""Force-directed graph layout algorithm."""

import math
import random
from typing import Dict, Tuple

from ..core import DiagramIR


class ForceDirectedLayout:
    """Force-directed layout using Fruchterman-Reingold algorithm."""

    def __init__(
        self,
        iterations: int = 100,
        optimal_distance: float = 100,
        repulsion_strength: float = 5000,
        attraction_strength: float = 0.1,
        cooling_factor: float = 0.95,
    ):
        """Initialize force-directed layout.

        Args:
            iterations: Number of iterations
            optimal_distance: Optimal distance between connected nodes
            repulsion_strength: Node repulsion strength
            attraction_strength: Edge attraction strength
            cooling_factor: Temperature cooling factor per iteration
        """
        self.iterations = iterations
        self.k = optimal_distance
        self.c_repulsion = repulsion_strength
        self.c_spring = attraction_strength
        self.cooling = cooling_factor

    def compute(self, diagram: DiagramIR) -> Dict[str, Tuple[float, float]]:
        """Compute node positions using force-directed layout.

        Args:
            diagram: DiagramIR to layout

        Returns:
            Dictionary mapping node IDs to (x, y) positions
        """
        # Initialize random positions
        positions = {}
        for node in diagram.nodes:
            positions[node.id] = (
                random.uniform(0, 500),
                random.uniform(0, 500),
            )

        # Build adjacency for faster lookup
        adjacent = {node.id: set() for node in diagram.nodes}
        for edge in diagram.edges:
            adjacent[edge.source].add(edge.target)
            adjacent[edge.target].add(edge.source)

        # Initial temperature
        temperature = 100.0

        # Iterate
        for iteration in range(self.iterations):
            # Calculate forces
            forces = {node_id: (0.0, 0.0) for node_id in positions.keys()}

            # Repulsive forces (all pairs)
            node_ids = list(positions.keys())
            for i, node_a in enumerate(node_ids):
                for node_b in node_ids[i + 1 :]:
                    pos_a = positions[node_a]
                    pos_b = positions[node_b]

                    dx = pos_a[0] - pos_b[0]
                    dy = pos_a[1] - pos_b[1]
                    distance = math.sqrt(dx * dx + dy * dy) + 0.01  # Avoid division by zero

                    # Repulsion force
                    force = self.c_repulsion / (distance * distance)
                    fx = (dx / distance) * force
                    fy = (dy / distance) * force

                    forces[node_a] = (
                        forces[node_a][0] + fx,
                        forces[node_a][1] + fy,
                    )
                    forces[node_b] = (
                        forces[node_b][0] - fx,
                        forces[node_b][1] - fy,
                    )

            # Attractive forces (connected pairs)
            for edge in diagram.edges:
                pos_source = positions[edge.source]
                pos_target = positions[edge.target]

                dx = pos_target[0] - pos_source[0]
                dy = pos_target[1] - pos_source[1]
                distance = math.sqrt(dx * dx + dy * dy) + 0.01

                # Spring force
                force = self.c_spring * (distance - self.k)
                fx = (dx / distance) * force
                fy = (dy / distance) * force

                forces[edge.source] = (
                    forces[edge.source][0] + fx,
                    forces[edge.source][1] + fy,
                )
                forces[edge.target] = (
                    forces[edge.target][0] - fx,
                    forces[edge.target][1] - fy,
                )

            # Apply forces with temperature
            for node_id in positions.keys():
                fx, fy = forces[node_id]
                force_magnitude = math.sqrt(fx * fx + fy * fy)

                if force_magnitude > 0:
                    displacement = min(force_magnitude, temperature)
                    dx = (fx / force_magnitude) * displacement
                    dy = (fy / force_magnitude) * displacement

                    positions[node_id] = (
                        positions[node_id][0] + dx,
                        positions[node_id][1] + dy,
                    )

            # Cool down
            temperature *= self.cooling

        # Normalize positions to positive coordinates
        if positions:
            min_x = min(pos[0] for pos in positions.values())
            min_y = min(pos[1] for pos in positions.values())

            for node_id in positions:
                positions[node_id] = (
                    positions[node_id][0] - min_x + 50,
                    positions[node_id][1] - min_y + 50,
                )

        return positions
