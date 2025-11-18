"""Import diagrams from OpenAPI specifications."""

from pathlib import Path
from typing import Dict, Optional, Union

from ..core import DiagramIR, Edge, EdgeType, Node, NodeType


def from_openapi(spec: Union[str, Dict], title: Optional[str] = None) -> DiagramIR:
    """Import diagram from OpenAPI specification.

    Creates a diagram showing API endpoints and their relationships.

    Args:
        spec: Path to OpenAPI file or dict specification
        title: Optional diagram title

    Returns:
        DiagramIR representing API structure

    Example:
        >>> diagram = from_openapi('openapi.yaml')
        >>> diagram = from_openapi({'openapi': '3.0.0', ...})

    Note:
        Requires pyyaml for YAML files: pip install pyyaml
    """
    import json

    # Load spec if it's a file path
    if isinstance(spec, str):
        spec_path = Path(spec)
        if spec_path.suffix in [".yaml", ".yml"]:
            try:
                import yaml

                spec_dict = yaml.safe_load(spec_path.read_text())
            except ImportError:
                raise ImportError(
                    "PyYAML required for YAML files. Install with: pip install pyyaml"
                )
        else:  # JSON
            spec_dict = json.loads(spec_path.read_text())
    else:
        spec_dict = spec

    # Create diagram
    diagram_title = title or spec_dict.get("info", {}).get("title", "API")
    diagram = DiagramIR(metadata={"title": diagram_title, "type": "api"})

    # Add API info node
    api_version = spec_dict.get("info", {}).get("version", "1.0")
    diagram.add_node(
        Node(
            id="api_root",
            label=f"{diagram_title} v{api_version}",
            node_type=NodeType.START,
        )
    )

    # Group endpoints by tags
    paths = spec_dict.get("paths", {})
    tag_groups = {}

    for path, path_item in paths.items():
        for method in ["get", "post", "put", "delete", "patch"]:
            if method in path_item:
                operation = path_item[method]
                operation_id = operation.get("operationId", f"{method}_{path}")

                # Get tags
                tags = operation.get("tags", ["default"])
                tag = tags[0] if tags else "default"

                if tag not in tag_groups:
                    tag_groups[tag] = []

                tag_groups[tag].append(
                    {"id": operation_id, "method": method.upper(), "path": path}
                )

    # Create nodes for tags
    for tag_name, operations in tag_groups.items():
        tag_id = f"tag_{tag_name}"
        diagram.add_node(
            Node(id=tag_id, label=tag_name.title(), node_type=NodeType.DECISION)
        )
        diagram.add_edge(Edge(source="api_root", target=tag_id))

        # Create nodes for operations
        for op in operations:
            node_id = op["id"]
            label = f"{op['method']} {op['path']}"
            diagram.add_node(Node(id=node_id, label=label, node_type=NodeType.PROCESS))
            diagram.add_edge(Edge(source=tag_id, target=node_id))

    return diagram


def from_openapi_to_sequence(spec: Union[str, Dict], flow: str = "default") -> DiagramIR:
    """Create sequence diagram from OpenAPI spec showing request flow.

    Args:
        spec: Path to OpenAPI file or dict
        flow: Flow to diagram (e.g., 'auth', 'crud')

    Returns:
        DiagramIR as sequence diagram

    Example:
        >>> diagram = from_openapi_to_sequence('api.yaml', flow='auth')
    """
    # This would create a sequence diagram showing client -> API -> services flow
    # Implementation would parse the OpenAPI spec and create participant interactions
    # For now, return a basic implementation
    diagram = DiagramIR(metadata={"type": "sequence"})

    # Add basic participants
    diagram.add_node(Node(id="client", label="Client"))
    diagram.add_node(Node(id="api", label="API"))
    diagram.add_node(Node(id="database", label="Database"))

    # Add sample flow
    diagram.add_edge(Edge(source="client", target="api", label="Request"))
    diagram.add_edge(Edge(source="api", target="database", label="Query"))
    diagram.add_edge(
        Edge(source="database", target="api", label="Result", edge_type=EdgeType.CONDITIONAL)
    )
    diagram.add_edge(
        Edge(source="api", target="client", label="Response", edge_type=EdgeType.CONDITIONAL)
    )

    return diagram
