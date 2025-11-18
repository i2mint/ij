"""Git integration for diagram version control and diffing.

Provides tools for comparing diagrams, merging changes, and tracking history.
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional, Tuple

from .core import DiagramIR, Edge, Node
from .parsers import D2Parser, MermaidParser


@dataclass
class DiagramChanges:
    """Changes between two diagrams."""

    added_nodes: List[Node] = field(default_factory=list)
    removed_nodes: List[Node] = field(default_factory=list)
    modified_nodes: List[Tuple[Node, Node]] = field(default_factory=list)
    added_edges: List[Edge] = field(default_factory=list)
    removed_edges: List[Edge] = field(default_factory=list)
    modified_edges: List[Tuple[Edge, Edge]] = field(default_factory=list)

    @property
    def has_changes(self) -> bool:
        """Check if there are any changes."""
        return bool(
            self.added_nodes
            or self.removed_nodes
            or self.modified_nodes
            or self.added_edges
            or self.removed_edges
            or self.modified_edges
        )

    @property
    def total_changes(self) -> int:
        """Count total number of changes."""
        return (
            len(self.added_nodes)
            + len(self.removed_nodes)
            + len(self.modified_nodes)
            + len(self.added_edges)
            + len(self.removed_edges)
            + len(self.modified_edges)
        )


class DiagramDiff:
    """Compare and diff diagrams."""

    def __init__(self):
        """Initialize differ."""
        pass

    def compare(self, diagram1: DiagramIR, diagram2: DiagramIR) -> DiagramChanges:
        """Compare two diagrams.

        Args:
            diagram1: Original diagram
            diagram2: Modified diagram

        Returns:
            DiagramChanges describing differences

        Example:
            >>> differ = DiagramDiff()
            >>> changes = differ.compare(old_diagram, new_diagram)
            >>> print(f"Added: {len(changes.added_nodes)} nodes")
        """
        changes = DiagramChanges()

        # Compare nodes
        nodes1 = {n.id: n for n in diagram1.nodes}
        nodes2 = {n.id: n for n in diagram2.nodes}

        # Find added/removed nodes
        for node_id in nodes2.keys() - nodes1.keys():
            changes.added_nodes.append(nodes2[node_id])

        for node_id in nodes1.keys() - nodes2.keys():
            changes.removed_nodes.append(nodes1[node_id])

        # Find modified nodes
        for node_id in nodes1.keys() & nodes2.keys():
            n1, n2 = nodes1[node_id], nodes2[node_id]
            if (
                n1.label != n2.label
                or n1.node_type != n2.node_type
                or n1.metadata != n2.metadata
            ):
                changes.modified_nodes.append((n1, n2))

        # Compare edges
        def edge_key(e: Edge) -> tuple:
            return (e.source, e.target, e.label or "", e.edge_type)

        edges1 = {edge_key(e): e for e in diagram1.edges}
        edges2 = {edge_key(e): e for e in diagram2.edges}

        # Find added/removed edges
        for key in edges2.keys() - edges1.keys():
            changes.added_edges.append(edges2[key])

        for key in edges1.keys() - edges2.keys():
            changes.removed_edges.append(edges1[key])

        return changes

    def compare_files(self, file1: str, file2: str) -> DiagramChanges:
        """Compare two diagram files.

        Args:
            file1: Path to first diagram
            file2: Path to second diagram

        Returns:
            DiagramChanges describing differences
        """
        diagram1 = self._parse_file(file1)
        diagram2 = self._parse_file(file2)
        return self.compare(diagram1, diagram2)

    def _parse_file(self, filename: str) -> DiagramIR:
        """Parse a diagram file."""
        ext = Path(filename).suffix.lower()

        text = Path(filename).read_text()

        if ext in [".mmd", ".mermaid"]:
            return MermaidParser().parse(text)
        elif ext == ".d2":
            return D2Parser().parse(text)
        else:
            # Try Mermaid as default
            try:
                return MermaidParser().parse(text)
            except:
                return D2Parser().parse(text)

    def generate_diff_report(self, changes: DiagramChanges) -> str:
        """Generate human-readable diff report.

        Args:
            changes: DiagramChanges to report

        Returns:
            Formatted diff report string
        """
        lines = []

        if not changes.has_changes:
            return "No changes detected."

        lines.append(f"Total changes: {changes.total_changes}\n")

        if changes.added_nodes:
            lines.append(f"Added nodes ({len(changes.added_nodes)}):")
            for node in changes.added_nodes:
                lines.append(f"  + {node.id}: {node.label} [{node.node_type.value}]")
            lines.append("")

        if changes.removed_nodes:
            lines.append(f"Removed nodes ({len(changes.removed_nodes)}):")
            for node in changes.removed_nodes:
                lines.append(f"  - {node.id}: {node.label} [{node.node_type.value}]")
            lines.append("")

        if changes.modified_nodes:
            lines.append(f"Modified nodes ({len(changes.modified_nodes)}):")
            for old_node, new_node in changes.modified_nodes:
                lines.append(f"  ~ {old_node.id}:")
                if old_node.label != new_node.label:
                    lines.append(f"      label: {old_node.label} → {new_node.label}")
                if old_node.node_type != new_node.node_type:
                    lines.append(
                        f"      type: {old_node.node_type.value} → {new_node.node_type.value}"
                    )
            lines.append("")

        if changes.added_edges:
            lines.append(f"Added edges ({len(changes.added_edges)}):")
            for edge in changes.added_edges:
                label = f" ({edge.label})" if edge.label else ""
                lines.append(f"  + {edge.source} → {edge.target}{label}")
            lines.append("")

        if changes.removed_edges:
            lines.append(f"Removed edges ({len(changes.removed_edges)}):")
            for edge in changes.removed_edges:
                label = f" ({edge.label})" if edge.label else ""
                lines.append(f"  - {edge.source} → {edge.target}{label}")
            lines.append("")

        return "\n".join(lines)

    def merge(
        self,
        base: DiagramIR,
        branch1: DiagramIR,
        branch2: DiagramIR,
        strategy: str = "union",
    ) -> DiagramIR:
        """Merge two diagram versions with a common base.

        Args:
            base: Common ancestor diagram
            branch1: First modified version
            branch2: Second modified version
            strategy: Merge strategy ('union', 'intersection', 'ours', 'theirs')

        Returns:
            Merged DiagramIR

        Example:
            >>> differ = DiagramDiff()
            >>> merged = differ.merge(base, branch1, branch2, strategy='union')
        """
        if strategy == "ours":
            return branch1
        elif strategy == "theirs":
            return branch2
        elif strategy == "union":
            return self._merge_union(base, branch1, branch2)
        elif strategy == "intersection":
            return self._merge_intersection(base, branch1, branch2)
        else:
            raise ValueError(f"Unknown merge strategy: {strategy}")

    def _merge_union(
        self, base: DiagramIR, branch1: DiagramIR, branch2: DiagramIR
    ) -> DiagramIR:
        """Merge using union strategy (include all changes)."""
        merged = DiagramIR(metadata=branch1.metadata.copy())

        # Collect all nodes (prefer branch2 for conflicts)
        nodes_dict = {}

        for node in base.nodes:
            nodes_dict[node.id] = node

        for node in branch1.nodes:
            nodes_dict[node.id] = node

        for node in branch2.nodes:
            nodes_dict[node.id] = node

        for node in nodes_dict.values():
            merged.add_node(node)

        # Collect all edges
        edge_set = set()

        def edge_sig(e: Edge) -> tuple:
            return (e.source, e.target, e.label or "", e.edge_type)

        for edge in base.edges + branch1.edges + branch2.edges:
            sig = edge_sig(edge)
            if sig not in edge_set:
                merged.add_edge(edge)
                edge_set.add(sig)

        return merged

    def _merge_intersection(
        self, base: DiagramIR, branch1: DiagramIR, branch2: DiagramIR
    ) -> DiagramIR:
        """Merge using intersection strategy (only common changes)."""
        merged = DiagramIR(metadata=base.metadata.copy())

        # Only include nodes present in both branches
        nodes1 = {n.id for n in branch1.nodes}
        nodes2 = {n.id for n in branch2.nodes}
        common_nodes = nodes1 & nodes2

        nodes_dict = {n.id: n for n in branch1.nodes}
        for node_id in common_nodes:
            merged.add_node(nodes_dict[node_id])

        # Only include edges present in both branches
        def edge_sig(e: Edge) -> tuple:
            return (e.source, e.target)

        edges1 = {edge_sig(e): e for e in branch1.edges}
        edges2 = {edge_sig(e): e for e in branch2.edges}

        for sig in edges1.keys() & edges2.keys():
            if sig[0] in common_nodes and sig[1] in common_nodes:
                merged.add_edge(edges1[sig])

        return merged


class DiagramHistory:
    """Track diagram history and changes over time."""

    def __init__(self):
        """Initialize history tracker."""
        self.versions: List[Tuple[str, DiagramIR]] = []

    def add_version(self, name: str, diagram: DiagramIR):
        """Add a version to history.

        Args:
            name: Version name/identifier
            diagram: DiagramIR snapshot
        """
        self.versions.append((name, diagram))

    def get_version(self, name: str) -> Optional[DiagramIR]:
        """Get a specific version.

        Args:
            name: Version name

        Returns:
            DiagramIR if found, None otherwise
        """
        for ver_name, diagram in self.versions:
            if ver_name == name:
                return diagram
        return None

    def list_versions(self) -> List[str]:
        """List all version names."""
        return [name for name, _ in self.versions]

    def compare_versions(self, name1: str, name2: str) -> DiagramChanges:
        """Compare two versions.

        Args:
            name1: First version name
            name2: Second version name

        Returns:
            DiagramChanges between versions
        """
        diagram1 = self.get_version(name1)
        diagram2 = self.get_version(name2)

        if diagram1 is None:
            raise ValueError(f"Version not found: {name1}")
        if diagram2 is None:
            raise ValueError(f"Version not found: {name2}")

        differ = DiagramDiff()
        return differ.compare(diagram1, diagram2)

    def get_changelog(self) -> str:
        """Generate changelog across all versions.

        Returns:
            Formatted changelog string
        """
        if len(self.versions) < 2:
            return "No version history to compare"

        lines = [f"Changelog ({len(self.versions)} versions):\n"]

        differ = DiagramDiff()

        for i in range(1, len(self.versions)):
            prev_name, prev_diagram = self.versions[i - 1]
            curr_name, curr_diagram = self.versions[i]

            changes = differ.compare(prev_diagram, curr_diagram)

            if changes.has_changes:
                lines.append(f"\n{prev_name} → {curr_name}:")
                lines.append(f"  Changes: {changes.total_changes}")
                lines.append(f"    Nodes: +{len(changes.added_nodes)} -{len(changes.removed_nodes)} ~{len(changes.modified_nodes)}")
                lines.append(f"    Edges: +{len(changes.added_edges)} -{len(changes.removed_edges)}")

        return "\n".join(lines)
