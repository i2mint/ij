"""Import diagrams from draw.io files."""

import base64
import re
import xml.etree.ElementTree as ET
import zlib
from pathlib import Path
from typing import Optional
from urllib.parse import unquote

from ..core import DiagramIR, Edge, Node, NodeType


def from_drawio(file_path: str, page: int = 0) -> DiagramIR:
    """Import diagram from draw.io file.

    Args:
        file_path: Path to draw.io (.drawio or .xml) file
        page: Page number to import (0-indexed)

    Returns:
        DiagramIR representation

    Example:
        >>> diagram = from_drawio('flowchart.drawio')

    Note:
        draw.io files use compressed XML. This provides basic support
        for flowchart elements.
    """
    content = Path(file_path).read_text()

    # Parse XML
    root = ET.fromstring(content)

    # Find diagram element
    diagram_elem = root.find(".//diagram")
    if diagram_elem is None:
        raise ValueError("No diagram found in file")

    # Decode diagram data
    diagram_data = diagram_elem.text
    if diagram_data:
        # draw.io uses URL encoding + base64 + zlib compression
        decoded = base64.b64decode(unquote(diagram_data))
        try:
            decompressed = zlib.decompress(decoded, -zlib.MAX_WBITS)
            xml_content = decompressed.decode("utf-8")
        except:
            xml_content = decoded.decode("utf-8")

        diagram_xml = ET.fromstring(xml_content)
    else:
        # Uncompressed format
        diagram_xml = diagram_elem

    # Parse diagram
    diagram = DiagramIR(metadata={"title": "Imported from draw.io"})

    # Find all cells (nodes and edges in draw.io)
    cells = diagram_xml.findall(".//mxCell")

    node_map = {}  # draw.io ID -> our node ID
    node_id_counter = 0

    # First pass: create nodes
    for cell in cells:
        cell_id = cell.get("id")
        cell_value = cell.get("value", "")
        cell_style = cell.get("style", "")

        # Skip root and layer cells
        if cell.get("parent") in ["0", "1"] and not cell_value:
            continue

        # Check if it's a vertex (node) or edge
        if cell.get("edge") != "1" and cell.get("vertex") == "1":
            # It's a node
            node_id = f"n{node_id_counter}"
            node_id_counter += 1

            # Determine node type from style
            node_type = NodeType.PROCESS
            if "ellipse" in cell_style or "rounded" in cell_style:
                if "start" in cell_value.lower() or "begin" in cell_value.lower():
                    node_type = NodeType.START
                elif "end" in cell_value.lower() or "stop" in cell_value.lower():
                    node_type = NodeType.END
            elif "rhombus" in cell_style or "diamond" in cell_style:
                node_type = NodeType.DECISION

            diagram.add_node(Node(id=node_id, label=cell_value, node_type=node_type))
            node_map[cell_id] = node_id

    # Second pass: create edges
    for cell in cells:
        if cell.get("edge") == "1":
            source_id = cell.get("source")
            target_id = cell.get("target")
            edge_label = cell.get("value", "")

            if source_id in node_map and target_id in node_map:
                diagram.add_edge(
                    Edge(
                        source=node_map[source_id],
                        target=node_map[target_id],
                        label=edge_label if edge_label else None,
                    )
                )

    return diagram


def from_drawio_xml(xml_content: str) -> DiagramIR:
    """Import from raw draw.io XML content.

    Args:
        xml_content: draw.io XML string

    Returns:
        DiagramIR representation
    """
    import tempfile

    # Write to temp file and use main function
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".drawio", delete=False
    ) as f:
        f.write(xml_content)
        temp_path = f.name

    try:
        diagram = from_drawio(temp_path)
    finally:
        Path(temp_path).unlink()

    return diagram
