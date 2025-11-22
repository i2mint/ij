"""Diagram validation and linting.

Provides rules and validators to ensure diagram quality and consistency.
"""

from dataclasses import dataclass
from enum import Enum
from typing import List, Optional

from .core import DiagramIR, NodeType
from .transforms import DiagramTransforms


class Severity(Enum):
    """Issue severity levels."""

    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


@dataclass
class ValidationIssue:
    """A validation issue found in a diagram."""

    severity: Severity
    message: str
    location: Optional[str] = None
    rule: Optional[str] = None


@dataclass
class ValidationResult:
    """Result of diagram validation."""

    is_valid: bool
    issues: List[ValidationIssue]

    @property
    def errors(self) -> List[ValidationIssue]:
        """Get only error-level issues."""
        return [i for i in self.issues if i.severity == Severity.ERROR]

    @property
    def warnings(self) -> List[ValidationIssue]:
        """Get only warning-level issues."""
        return [i for i in self.issues if i.severity == Severity.WARNING]


class DiagramValidator:
    """Validate diagrams against various rules."""

    def __init__(self):
        """Initialize validator."""
        self.rules = {
            "no-orphaned-nodes": self._check_no_orphaned_nodes,
            "no-cycles": self._check_no_cycles,
            "require-start-end": self._check_require_start_end,
            "max-complexity": self._check_max_complexity,
            "unique-node-ids": self._check_unique_node_ids,
            "unique-labels": self._check_unique_labels,
            "valid-edges": self._check_valid_edges,
            "no-self-loops": self._check_no_self_loops,
            "connected-graph": self._check_connected_graph,
        }

    def validate(
        self, diagram: DiagramIR, rules: Optional[List[str]] = None
    ) -> ValidationResult:
        """Validate diagram against rules.

        Args:
            diagram: DiagramIR to validate
            rules: List of rule names to check (None = all rules)

        Returns:
            ValidationResult with issues found

        Example:
            >>> validator = DiagramValidator()
            >>> result = validator.validate(diagram, rules=['no-cycles', 'no-orphaned-nodes'])
            >>> if not result.is_valid:
            ...     for issue in result.errors:
            ...         print(f"ERROR: {issue.message}")
        """
        issues = []

        # Determine which rules to run
        if rules is None:
            rules_to_run = self.rules.keys()
        else:
            rules_to_run = []
            for rule in rules:
                # Handle parameterized rules like "max-nodes-50"
                if rule.startswith("max-nodes-"):
                    try:
                        max_nodes = int(rule.split("-")[-1])
                        issues.extend(self._check_max_nodes(diagram, max_nodes))
                    except ValueError:
                        pass
                elif rule.startswith("max-edges-"):
                    try:
                        max_edges = int(rule.split("-")[-1])
                        issues.extend(self._check_max_edges(diagram, max_edges))
                    except ValueError:
                        pass
                elif rule in self.rules:
                    rules_to_run.append(rule)

        # Run validation rules
        for rule_name in rules_to_run:
            rule_func = self.rules[rule_name]
            rule_issues = rule_func(diagram)
            issues.extend(rule_issues)

        # Determine if valid (no errors)
        is_valid = not any(i.severity == Severity.ERROR for i in issues)

        return ValidationResult(is_valid=is_valid, issues=issues)

    def _check_no_orphaned_nodes(self, diagram: DiagramIR) -> List[ValidationIssue]:
        """Check for nodes with no connections."""
        issues = []

        # Build connection sets
        connected = set()
        for edge in diagram.edges:
            connected.add(edge.source)
            connected.add(edge.target)

        # Find orphaned nodes (not START/END)
        for node in diagram.nodes:
            if node.id not in connected and node.node_type not in [
                NodeType.START,
                NodeType.END,
            ]:
                issues.append(
                    ValidationIssue(
                        severity=Severity.WARNING,
                        message=f"Orphaned node: {node.id} ({node.label})",
                        location=node.id,
                        rule="no-orphaned-nodes",
                    )
                )

        return issues

    def _check_no_cycles(self, diagram: DiagramIR) -> List[ValidationIssue]:
        """Check for cycles in the diagram."""
        issues = []

        cycles = DiagramTransforms.find_cycles(diagram)
        if cycles:
            for cycle in cycles:
                cycle_path = " → ".join(cycle)
                issues.append(
                    ValidationIssue(
                        severity=Severity.ERROR,
                        message=f"Cycle detected: {cycle_path}",
                        rule="no-cycles",
                    )
                )

        return issues

    def _check_require_start_end(self, diagram: DiagramIR) -> List[ValidationIssue]:
        """Check for START and END nodes."""
        issues = []

        has_start = any(n.node_type == NodeType.START for n in diagram.nodes)
        has_end = any(n.node_type == NodeType.END for n in diagram.nodes)

        if not has_start:
            issues.append(
                ValidationIssue(
                    severity=Severity.ERROR,
                    message="Missing START node",
                    rule="require-start-end",
                )
            )

        if not has_end:
            issues.append(
                ValidationIssue(
                    severity=Severity.ERROR,
                    message="Missing END node",
                    rule="require-start-end",
                )
            )

        return issues

    def _check_max_complexity(self, diagram: DiagramIR) -> List[ValidationIssue]:
        """Check diagram complexity."""
        issues = []

        stats = DiagramTransforms.get_statistics(diagram)

        # Warn if too many nodes
        if stats["node_count"] > 50:
            issues.append(
                ValidationIssue(
                    severity=Severity.WARNING,
                    message=f"High node count: {stats['node_count']} (consider splitting)",
                    rule="max-complexity",
                )
            )

        # Warn if too many edges per node
        if stats["max_outgoing_degree"] > 10:
            issues.append(
                ValidationIssue(
                    severity=Severity.WARNING,
                    message=f"High branching factor: {stats['max_outgoing_degree']} edges from one node",
                    rule="max-complexity",
                )
            )

        return issues

    def _check_max_nodes(
        self, diagram: DiagramIR, max_nodes: int
    ) -> List[ValidationIssue]:
        """Check maximum node count."""
        issues = []

        if len(diagram.nodes) > max_nodes:
            issues.append(
                ValidationIssue(
                    severity=Severity.ERROR,
                    message=f"Too many nodes: {len(diagram.nodes)} > {max_nodes}",
                    rule=f"max-nodes-{max_nodes}",
                )
            )

        return issues

    def _check_max_edges(
        self, diagram: DiagramIR, max_edges: int
    ) -> List[ValidationIssue]:
        """Check maximum edge count."""
        issues = []

        if len(diagram.edges) > max_edges:
            issues.append(
                ValidationIssue(
                    severity=Severity.ERROR,
                    message=f"Too many edges: {len(diagram.edges)} > {max_edges}",
                    rule=f"max-edges-{max_edges}",
                )
            )

        return issues

    def _check_unique_node_ids(self, diagram: DiagramIR) -> List[ValidationIssue]:
        """Check that node IDs are unique."""
        issues = []

        seen_ids = set()
        for node in diagram.nodes:
            if node.id in seen_ids:
                issues.append(
                    ValidationIssue(
                        severity=Severity.ERROR,
                        message=f"Duplicate node ID: {node.id}",
                        location=node.id,
                        rule="unique-node-ids",
                    )
                )
            seen_ids.add(node.id)

        return issues

    def _check_unique_labels(self, diagram: DiagramIR) -> List[ValidationIssue]:
        """Check for duplicate labels (warning only)."""
        issues = []

        label_counts = {}
        for node in diagram.nodes:
            if node.label:
                label_counts[node.label] = label_counts.get(node.label, 0) + 1

        for label, count in label_counts.items():
            if count > 1:
                issues.append(
                    ValidationIssue(
                        severity=Severity.INFO,
                        message=f"Duplicate label '{label}' used {count} times",
                        rule="unique-labels",
                    )
                )

        return issues

    def _check_valid_edges(self, diagram: DiagramIR) -> List[ValidationIssue]:
        """Check that edges reference valid nodes."""
        issues = []

        node_ids = {n.id for n in diagram.nodes}

        for edge in diagram.edges:
            if edge.source not in node_ids:
                issues.append(
                    ValidationIssue(
                        severity=Severity.ERROR,
                        message=f"Edge references non-existent source node: {edge.source}",
                        rule="valid-edges",
                    )
                )

            if edge.target not in node_ids:
                issues.append(
                    ValidationIssue(
                        severity=Severity.ERROR,
                        message=f"Edge references non-existent target node: {edge.target}",
                        rule="valid-edges",
                    )
                )

        return issues

    def _check_no_self_loops(self, diagram: DiagramIR) -> List[ValidationIssue]:
        """Check for self-loops (edges from node to itself)."""
        issues = []

        for edge in diagram.edges:
            if edge.source == edge.target:
                issues.append(
                    ValidationIssue(
                        severity=Severity.WARNING,
                        message=f"Self-loop detected on node: {edge.source}",
                        location=edge.source,
                        rule="no-self-loops",
                    )
                )

        return issues

    def _check_connected_graph(self, diagram: DiagramIR) -> List[ValidationIssue]:
        """Check if graph is connected."""
        issues = []

        if len(diagram.nodes) == 0:
            return issues

        # BFS to find reachable nodes
        from collections import deque

        # Build adjacency list (undirected for connectivity check)
        adj = {}
        for node in diagram.nodes:
            adj[node.id] = []

        for edge in diagram.edges:
            if edge.source not in adj:
                adj[edge.source] = []
            if edge.target not in adj:
                adj[edge.target] = []
            adj[edge.source].append(edge.target)
            adj[edge.target].append(edge.source)

        # BFS from first node
        start = diagram.nodes[0].id
        visited = set([start])
        queue = deque([start])

        while queue:
            node_id = queue.popleft()
            for neighbor in adj.get(node_id, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)

        # Check if all nodes were visited
        all_node_ids = {n.id for n in diagram.nodes}
        if len(visited) < len(all_node_ids):
            disconnected = all_node_ids - visited
            issues.append(
                ValidationIssue(
                    severity=Severity.WARNING,
                    message=f"Graph not fully connected. Disconnected nodes: {', '.join(list(disconnected)[:5])}",
                    rule="connected-graph",
                )
            )

        return issues


class DiagramLinter:
    """Lint diagrams for style and best practices."""

    def __init__(self):
        """Initialize linter."""
        pass

    def lint(self, diagram: DiagramIR) -> List[ValidationIssue]:
        """Lint diagram for style issues.

        Args:
            diagram: DiagramIR to lint

        Returns:
            List of linting issues

        Example:
            >>> linter = DiagramLinter()
            >>> issues = linter.lint(diagram)
            >>> for issue in issues:
            ...     print(f"{issue.severity.value.upper()}: {issue.message}")
        """
        issues = []

        # Check label consistency
        issues.extend(self._check_label_style(diagram))

        # Check naming conventions
        issues.extend(self._check_naming_conventions(diagram))

        # Check metadata
        issues.extend(self._check_metadata(diagram))

        return issues

    def _check_label_style(self, diagram: DiagramIR) -> List[ValidationIssue]:
        """Check label style consistency."""
        issues = []

        # Check for very long labels
        for node in diagram.nodes:
            if node.label and len(node.label) > 50:
                issues.append(
                    ValidationIssue(
                        severity=Severity.INFO,
                        message=f"Long label in {node.id}: '{node.label[:40]}...'",
                        location=node.id,
                        rule="label-length",
                    )
                )

        return issues

    def _check_naming_conventions(self, diagram: DiagramIR) -> List[ValidationIssue]:
        """Check naming conventions."""
        issues = []

        # Check for generic node IDs like "n1", "n2"
        generic_pattern = r"^n\d+$"
        import re

        generic_count = 0
        for node in diagram.nodes:
            if re.match(generic_pattern, node.id):
                generic_count += 1

        if generic_count > 5:
            issues.append(
                ValidationIssue(
                    severity=Severity.INFO,
                    message=f"Many generic node IDs (n1, n2, etc.): {generic_count} nodes",
                    rule="naming-conventions",
                )
            )

        return issues

    def _check_metadata(self, diagram: DiagramIR) -> List[ValidationIssue]:
        """Check diagram metadata."""
        issues = []

        # Recommend adding a title
        if "title" not in diagram.metadata or not diagram.metadata["title"]:
            issues.append(
                ValidationIssue(
                    severity=Severity.INFO,
                    message="Consider adding a title to the diagram",
                    rule="metadata-title",
                )
            )

        return issues
