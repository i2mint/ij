"""Layout engine for positioning diagram nodes."""

from typing import Dict, Literal, Tuple

from ..core import DiagramIR


class LayoutEngine:
    """Apply layout algorithms to diagrams."""

    def __init__(
        self,
        algorithm: Literal[
            "force-directed", "hierarchical", "circular", "grid"
        ] = "hierarchical",
        **kwargs,
    ):
        """Initialize layout engine.

        Args:
            algorithm: Layout algorithm to use
            **kwargs: Algorithm-specific parameters
        """
        self.algorithm = algorithm
        self.params = kwargs

    def apply(self, diagram: DiagramIR) -> Dict[str, Tuple[float, float]]:
        """Apply layout algorithm to diagram.

        Args:
            diagram: DiagramIR to layout

        Returns:
            Dictionary mapping node IDs to (x, y) positions

        Example:
            >>> engine = LayoutEngine(algorithm='force-directed')
            >>> positions = engine.apply(diagram)
            >>> print(positions['node1'])  # (x, y)
            (150.0, 200.0)
        """
        if self.algorithm == "force-directed":
            from .force_directed import ForceDirectedLayout

            layout = ForceDirectedLayout(**self.params)
            return layout.compute(diagram)

        elif self.algorithm == "hierarchical":
            from .hierarchical import HierarchicalLayout

            layout = HierarchicalLayout(**self.params)
            return layout.compute(diagram)

        elif self.algorithm == "circular":
            return self._circular_layout(diagram)

        elif self.algorithm == "grid":
            return self._grid_layout(diagram)

        else:
            raise ValueError(f"Unknown algorithm: {self.algorithm}")

    def _circular_layout(self, diagram: DiagramIR) -> Dict[str, Tuple[float, float]]:
        """Arrange nodes in a circle."""
        import math

        positions = {}
        n = len(diagram.nodes)
        radius = max(200, n * 30)

        for i, node in enumerate(diagram.nodes):
            angle = 2 * math.pi * i / n
            x = radius * math.cos(angle) + radius
            y = radius * math.sin(angle) + radius
            positions[node.id] = (x, y)

        return positions

    def _grid_layout(self, diagram: DiagramIR) -> Dict[str, Tuple[float, float]]:
        """Arrange nodes in a grid."""
        import math

        positions = {}
        n = len(diagram.nodes)
        cols = math.ceil(math.sqrt(n))
        spacing_x = 150
        spacing_y = 100

        for i, node in enumerate(diagram.nodes):
            row = i // cols
            col = i % cols
            x = col * spacing_x + 50
            y = row * spacing_y + 50
            positions[node.id] = (x, y)

        return positions
