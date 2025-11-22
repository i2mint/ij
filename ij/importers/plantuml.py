"""Import diagrams from PlantUML format."""

import re
from typing import Optional

from ..core import DiagramIR, Edge, EdgeType, Node, NodeType


def from_plantuml(plantuml_code: str, title: Optional[str] = None) -> DiagramIR:
    """Parse PlantUML activity diagram to DiagramIR.

    Args:
        plantuml_code: PlantUML source code
        title: Optional diagram title

    Returns:
        DiagramIR representation

    Example:
        >>> code = '''
        ... @startuml
        ... start
        ... :Process;
        ... stop
        ... @enduml
        ... '''
        >>> diagram = from_plantuml(code)

    Note:
        Currently supports basic activity diagrams.
        Full PlantUML syntax support is complex and partial.
    """
    diagram = DiagramIR(metadata={"title": title or "Imported from PlantUML"})

    lines = [line.strip() for line in plantuml_code.split("\n")]

    node_counter = 0
    node_map = {}  # PlantUML label -> node ID

    for line in lines:
        # Skip comments and delimiters
        if (
            not line
            or line.startswith("'")
            or line.startswith("@")
            or line.startswith("title")
        ):
            continue

        # Parse start node
        if line == "start":
            node_id = "start"
            diagram.add_node(
                Node(id=node_id, label="Start", node_type=NodeType.START)
            )
            node_map["start"] = node_id

        # Parse stop/end node
        elif line in ["stop", "end"]:
            node_id = "end"
            diagram.add_node(Node(id=node_id, label="End", node_type=NodeType.END))
            node_map["end"] = node_id

        # Parse activity: :label;
        elif line.startswith(":") and line.endswith(";"):
            label = line[1:-1].strip()
            node_id = f"n{node_counter}"
            node_counter += 1
            diagram.add_node(Node(id=node_id, label=label, node_type=NodeType.PROCESS))
            node_map[label] = node_id

        # Parse decision: if (condition) then
        elif line.startswith("if") and "then" in line:
            match = re.match(r"if\s*\((.*?)\)\s+then", line)
            if match:
                condition = match.group(1)
                node_id = f"n{node_counter}"
                node_counter += 1
                diagram.add_node(
                    Node(id=node_id, label=condition, node_type=NodeType.DECISION)
                )
                node_map[condition] = node_id

    # Connect nodes sequentially (simplified)
    nodes = list(node_map.values())
    for i in range(len(nodes) - 1):
        diagram.add_edge(Edge(source=nodes[i], target=nodes[i + 1]))

    return diagram


def from_plantuml_file(file_path: str) -> DiagramIR:
    """Import PlantUML from file.

    Args:
        file_path: Path to PlantUML file

    Returns:
        DiagramIR representation
    """
    from pathlib import Path

    content = Path(file_path).read_text()
    return from_plantuml(content)
