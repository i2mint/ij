"""Mermaid diagram parser.

Converts Mermaid syntax back to DiagramIR, enabling bidirectional conversion.

Lines the parser cannot interpret are *reported* rather than dropped: each one
is recorded in ``MermaidParser.unparsed_lines`` and raised as a
``MermaidParseWarning`` (or, with ``strict=True``, a ``ValueError``). Silently
discarding them used to turn generator drift into a silently wrong diagram --
e.g. an LLM emitting ``check_user --|Yes|--> show_dashboard`` instead of
``check_user -->|Yes| show_dashboard`` cost both the edge and the
``check_user{...}`` decision node it referenced, with no signal at all.
"""

import re
import warnings
from typing import Dict, List

from ..core import DiagramIR, Edge, EdgeType, Node, NodeType


class MermaidParseWarning(UserWarning):
    """Warns that a Mermaid line could not be interpreted and was skipped."""


class MermaidParser:
    """Parses Mermaid flowchart syntax to DiagramIR.

    Supports basic flowchart syntax including:
    - Node definitions with various shapes, standalone or inline on an edge line
    - Edge connections with labels, including chained edges
    - Title metadata

    A line matching none of the above is reported instead of being dropped:
    see ``unparsed_lines`` and the ``strict`` argument.

    Attributes:
        strict: Whether an unparseable line raises instead of warning
        nodes: Nodes found by the last parse, keyed by node id
        edges: Edges found by the last parse
        metadata: Diagram-level metadata (title, direction) from the last parse
        unparsed_lines: Lines the last parse could not interpret
    """

    # Pattern for flowchart declaration ('graph' is Mermaid's legacy synonym)
    FLOWCHART_PATTERN = re.compile(r"(?:flowchart|graph)\s+(TD|LR|BT|RL)")

    # Pattern for title
    TITLE_PATTERN = re.compile(r"title:\s*(.+)")

    # Valid Mermaid lines that carry no IR content (comments, subgraph
    # bookkeeping, styling directives). Recognized explicitly so that they are
    # skipped quietly instead of being reported as unparseable.
    IGNORED_LINE_PATTERN = re.compile(
        r"^(?:"
        r"%%"  # comment
        r"|(?:subgraph|direction|style|classDef|class|click|linkStyle)\s"
        r"|end\s*$"  # subgraph terminator
        r")"
    )

    # Node shapes, in match order: (opening delimiter, closing delimiter, type).
    # Single source of truth for both NODE_PATTERNS and ENDPOINT_PATTERN.
    NODE_SHAPES = [
        ("([", "])", NodeType.START),  # Stadium: n1([Label])
        ("{", "}", NodeType.DECISION),  # Rhombus: n1{Label}
        ("[(", ")]", NodeType.DATA),  # Cylindrical: n1[(Label)]
        ("[[", "]]", NodeType.SUBPROCESS),  # Subroutine: n1[[Label]]
        ("[", "]", NodeType.PROCESS),  # Rectangle: n1[Label]
    ]

    # Pattern for node with shape
    NODE_PATTERNS = [
        (
            re.compile(rf"(\w+){re.escape(opening)}(.+?){re.escape(closing)}"),
            node_type,
        )
        for opening, closing, node_type in NODE_SHAPES
    ]

    # A node id carrying no shape; Mermaid allows a bare `n1` on its own line
    BARE_ID_PATTERN = re.compile(r"\w+")

    # One endpoint of an edge: a node id with an optional inline shape, as in
    # `check_user{Is user authenticated?}`
    ENDPOINT_PATTERN = re.compile(
        r"\w+(?:"
        + "|".join(
            re.escape(opening) + ".+?" + re.escape(closing)
            for opening, closing, _ in NODE_SHAPES
        )
        + r")?"
    )

    # Link arrows, longest first so the alternation below is unambiguous
    ARROW_TO_EDGE_TYPE = {
        "<-->": EdgeType.BIDIRECTIONAL,
        "-.->": EdgeType.CONDITIONAL,
        "-->": EdgeType.DIRECT,
    }

    _ARROWS = "|".join(re.escape(arrow) for arrow in ARROW_TO_EDGE_TYPE)

    # An edge link: an arrow with an optional `|label|`. Used with re.split, so
    # an edge line becomes [endpoint, arrow, label, endpoint, arrow, label, ...]
    LINK_PATTERN = re.compile(rf"\s*({_ARROWS})(?:\|([^|]*)\|)?\s*")

    # Non-canonical link spellings, normalized to the `ARROW|label|` form before
    # parsing. The first is *invalid* Mermaid but a frequent LLM drift (observed
    # from gpt-4o-mini: `check_user --|Yes|--> show_dashboard`); the other two
    # are valid Mermaid alternatives to `-->|label|`.
    LINK_NORMALIZATIONS = [
        (re.compile(r"--\|([^|]*)\|(-->|-\.->)"), r"\2|\1|"),  # a --|L|--> b
        (re.compile(r"--\s+([^|>]+?)\s+(-->)"), r"\2|\1|"),  # a -- L --> b
        (re.compile(r"-\.\s+([^|>]+?)\s+\.->"), r"-.->|\1|"),  # a -. L .-> b
    ]

    # A stadium-shaped node whose label reads like a terminus is an END, not a
    # START (Mermaid uses the same shape for both)
    END_LABEL_WORDS = ("end", "finish", "complete", "done")

    def __init__(self, *, strict: bool = False):
        """Initialize parser.

        Args:
            strict: If True, raise ValueError on a line that cannot be parsed
                instead of warning and skipping it
        """
        self.strict = strict
        self.nodes: Dict[str, Node] = {}
        self.edges: List[Edge] = []
        self.metadata: Dict = {}
        self.unparsed_lines: List[str] = []

    def parse(self, mermaid_text: str) -> DiagramIR:
        """Parse Mermaid syntax to DiagramIR.

        Args:
            mermaid_text: Mermaid flowchart syntax

        Returns:
            DiagramIR representation

        Raises:
            ValueError: If ``strict`` is set and a line cannot be parsed

        Example:
            >>> parser = MermaidParser()
            >>> diagram = parser.parse('''flowchart TD
            ...     start([Start]) --> check{Ok?}
            ...     check --|Yes|--> done([Done])''')
            >>> [(node.id, node.node_type.value) for node in diagram.nodes]
            [('start', 'start'), ('check', 'decision'), ('done', 'end')]
            >>> [(edge.source, edge.target, edge.label) for edge in diagram.edges]
            [('start', 'check', None), ('check', 'done', 'Yes')]
        """
        self.nodes = {}
        self.edges = []
        self.metadata = {}
        self.unparsed_lines = []

        lines = mermaid_text.strip().split("\n")

        for lineno, raw_line in enumerate(lines, start=1):
            line = raw_line.strip()
            if (
                not line
                or line.startswith("---")
                or self.IGNORED_LINE_PATTERN.match(line)
            ):
                continue

            # Check for title
            title_match = self.TITLE_PATTERN.match(line)
            if title_match:
                self.metadata["title"] = title_match.group(1).strip()
                continue

            # Check for flowchart declaration
            flowchart_match = self.FLOWCHART_PATTERN.match(line)
            if flowchart_match:
                self.metadata["direction"] = flowchart_match.group(1)
                continue

            # Try to parse as edge, then as node
            if self._parse_edge(line) or self._parse_node(line):
                continue

            self._report_unparsed(line, lineno)

        # Build DiagramIR
        diagram = DiagramIR(metadata=self.metadata)
        for node in self.nodes.values():
            diagram.add_node(node)
        for edge in self.edges:
            diagram.add_edge(edge)

        return diagram

    def _parse_node(self, line: str) -> bool:
        """Parse a standalone node definition.

        Args:
            line: Line containing node definition

        Returns:
            True if successfully parsed, False otherwise
        """
        for pattern, node_type in self.NODE_PATTERNS:
            match = pattern.search(line)
            if match:
                self._add_node(match.group(1), match.group(2), node_type)
                return True

        # A bare id on its own line declares a node labelled by its id
        if self.BARE_ID_PATTERN.fullmatch(line):
            self._add_node(line, line, NodeType.PROCESS)
            return True

        return False

    def _parse_edge(self, line: str) -> bool:
        """Parse an edge definition, including chains and inline node shapes.

        Args:
            line: Line containing one or more edge connections

        Returns:
            True if successfully parsed, False otherwise
        """
        # re.split on a two-group pattern alternates text and groups, giving
        # [endpoint, arrow, label, endpoint, arrow, label, ..., endpoint]
        parts = self.LINK_PATTERN.split(self._normalize_links(line))
        endpoints, arrows, labels = parts[0::3], parts[1::3], parts[2::3]
        if not arrows:
            return False

        endpoints = [endpoint.strip() for endpoint in endpoints]
        if not all(self.ENDPOINT_PATTERN.fullmatch(e) for e in endpoints):
            # Something on this line is not a node reference (e.g. an arrow
            # inside a node label); let the node parser have it instead
            return False

        node_ids = [self._resolve_endpoint(e) for e in endpoints]
        for source, target, arrow, label in zip(node_ids, node_ids[1:], arrows, labels):
            self.edges.append(
                Edge(
                    source=source,
                    target=target,
                    label=label.strip() if label else None,
                    edge_type=self.ARROW_TO_EDGE_TYPE.get(arrow, EdgeType.DIRECT),
                )
            )

        return True

    def _normalize_links(self, line: str) -> str:
        """Rewrite non-canonical link spellings to the `ARROW|label|` form.

        Args:
            line: Line to normalize

        Returns:
            The line with every known link-label variant canonicalized
        """
        for pattern, replacement in self.LINK_NORMALIZATIONS:
            line = pattern.sub(replacement, line)
        return line

    def _resolve_endpoint(self, endpoint: str) -> str:
        """Resolve an edge endpoint to a node id, defining the node if needed.

        Args:
            endpoint: Endpoint text, e.g. `check_user` or `check_user{Ok?}`

        Returns:
            The node id the endpoint refers to
        """
        for pattern, node_type in self.NODE_PATTERNS:
            match = pattern.fullmatch(endpoint)
            if match:
                self._add_node(match.group(1), match.group(2), node_type)
                return match.group(1)

        # Bare id: give it a placeholder definition on first mention
        self._add_node(endpoint, endpoint, NodeType.PROCESS)
        return endpoint

    def _add_node(self, node_id: str, label: str, node_type: NodeType) -> None:
        """Register a node the first time it is seen.

        Args:
            node_id: Node identifier
            label: Node label
            node_type: Shape-derived node type; a START whose label reads like a
                terminus (see END_LABEL_WORDS) is recorded as an END
        """
        if node_type == NodeType.START and any(
            word in label.lower() for word in self.END_LABEL_WORDS
        ):
            node_type = NodeType.END

        if node_id not in self.nodes:
            self.nodes[node_id] = Node(id=node_id, label=label, node_type=node_type)

    def _report_unparsed(self, line: str, lineno: int) -> None:
        """Record and surface a line the parser could not interpret.

        Args:
            line: The offending line
            lineno: Its 1-based position in the parsed text

        Raises:
            ValueError: If ``strict`` is set
        """
        self.unparsed_lines.append(line)
        message = (
            f"Could not parse Mermaid line {lineno}: {line!r}. "
            "The line was skipped, so the diagram is incomplete."
        )
        if self.strict:
            raise ValueError(message)
        warnings.warn(message, MermaidParseWarning, stacklevel=3)

    def parse_file(self, filename: str) -> DiagramIR:
        """Parse Mermaid file to DiagramIR.

        Args:
            filename: Path to Mermaid file

        Returns:
            DiagramIR representation
        """
        with open(filename, "r") as f:
            return self.parse(f.read())
