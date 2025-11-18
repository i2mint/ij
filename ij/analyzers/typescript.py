"""TypeScript and JavaScript code analyzer.

Analyze TypeScript/JavaScript code to generate diagrams.
"""

import json
import re
import subprocess
import tempfile
from pathlib import Path
from typing import Optional

from ..core import DiagramIR, Edge, EdgeType, Node, NodeType


class TypeScriptAnalyzer:
    """Analyze TypeScript/JavaScript code to create diagrams."""

    def __init__(self):
        """Initialize analyzer."""
        self._check_dependencies()

    def _check_dependencies(self) -> bool:
        """Check if required tools are available."""
        try:
            result = subprocess.run(
                ["node", "--version"], capture_output=True, timeout=5
            )
            return result.returncode == 0
        except (FileNotFoundError, subprocess.TimeoutExpired):
            return False

    def analyze_function(
        self, code: str, function_name: Optional[str] = None
    ) -> DiagramIR:
        """Analyze TypeScript/JavaScript function to create flowchart.

        Args:
            code: TypeScript/JavaScript code
            function_name: Specific function to analyze (or first if None)

        Returns:
            DiagramIR representing function flow

        Example:
            >>> analyzer = TypeScriptAnalyzer()
            >>> code = '''
            ... function processData(input) {
            ...   if (input > 0) {
            ...     return input * 2;
            ...   }
            ...   return 0;
            ... }
            ... '''
            >>> diagram = analyzer.analyze_function(code)
        """
        diagram = DiagramIR(metadata={"title": f"Function: {function_name or 'code'}"})

        # Use regex-based parsing (simplified approach)
        # For production, would use @babel/parser or TypeScript compiler API

        # Find function
        if function_name:
            pattern = rf"(?:function\s+{function_name}|const\s+{function_name}\s*=.*?=>)"
        else:
            pattern = r"(?:function\s+\w+|const\s+\w+\s*=.*?=>)"

        func_match = re.search(pattern, code)
        if not func_match:
            return diagram

        # Extract function body
        start_idx = code.find("{", func_match.start())
        if start_idx == -1:
            return diagram

        # Find matching closing brace
        brace_count = 1
        end_idx = start_idx + 1
        while end_idx < len(code) and brace_count > 0:
            if code[end_idx] == "{":
                brace_count += 1
            elif code[end_idx] == "}":
                brace_count -= 1
            end_idx += 1

        func_body = code[start_idx + 1 : end_idx - 1]

        # Create start node
        diagram.add_node(
            Node(id="start", label=function_name or "Start", node_type=NodeType.START)
        )

        node_counter = [0]  # Use list for mutable counter
        last_node = ["start"]

        def add_node(label: str, node_type: NodeType = NodeType.PROCESS) -> str:
            node_id = f"n{node_counter[0]}"
            node_counter[0] += 1
            diagram.add_node(Node(id=node_id, label=label, node_type=node_type))
            return node_id

        # Parse statements
        for line in func_body.split("\n"):
            line = line.strip()
            if not line or line.startswith("//"):
                continue

            # If statement
            if line.startswith("if"):
                condition = re.search(r"if\s*\((.*?)\)", line)
                if condition:
                    cond_text = condition.group(1)
                    decision_id = add_node(cond_text, NodeType.DECISION)
                    diagram.add_edge(Edge(source=last_node[0], target=decision_id))
                    last_node[0] = decision_id

            # Return statement
            elif line.startswith("return"):
                return_value = line[6:].rstrip(";").strip()
                return_id = add_node(f"return {return_value}")
                diagram.add_edge(Edge(source=last_node[0], target=return_id))

                # Connect to end
                if not any(n.node_type == NodeType.END for n in diagram.nodes):
                    diagram.add_node(
                        Node(id="end", label="End", node_type=NodeType.END)
                    )
                diagram.add_edge(Edge(source=return_id, target="end"))

            # Function calls
            elif "(" in line and ")" in line:
                call_match = re.search(r"(\w+)\s*\(", line)
                if call_match:
                    func_call = call_match.group(1)
                    call_id = add_node(f"{func_call}()")
                    diagram.add_edge(Edge(source=last_node[0], target=call_id))
                    last_node[0] = call_id

        return diagram

    def analyze_module_imports(self, code: str) -> DiagramIR:
        """Analyze TypeScript module imports/exports.

        Args:
            code: TypeScript/JavaScript code

        Returns:
            DiagramIR showing module dependencies

        Example:
            >>> code = '''
            ... import { Component } from './components';
            ... import axios from 'axios';
            ... export default App;
            ... '''
            >>> diagram = analyzer.analyze_module_imports(code)
        """
        diagram = DiagramIR(metadata={"title": "Module Dependencies"})

        # Add module node
        diagram.add_node(
            Node(id="module", label="This Module", node_type=NodeType.START)
        )

        node_counter = 0

        # Find imports
        import_pattern = r"import\s+(?:{.*?}|\w+)\s+from\s+['\"](.+?)['\"]"
        for match in re.finditer(import_pattern, code):
            module_name = match.group(1)
            node_id = f"import_{node_counter}"
            node_counter += 1

            diagram.add_node(Node(id=node_id, label=module_name, node_type=NodeType.DATA))
            diagram.add_edge(
                Edge(source=node_id, target="module", label="import")
            )

        # Find exports
        export_pattern = r"export\s+(?:default\s+)?(\w+)"
        for match in re.finditer(export_pattern, code):
            export_name = match.group(1)
            node_id = f"export_{node_counter}"
            node_counter += 1

            diagram.add_node(
                Node(id=node_id, label=export_name, node_type=NodeType.END)
            )
            diagram.add_edge(
                Edge(source="module", target=node_id, label="export")
            )

        return diagram

    def analyze_react_component(self, code: str, component_name: str) -> DiagramIR:
        """Analyze React component to show component hierarchy.

        Args:
            code: React component code
            component_name: Name of the component

        Returns:
            DiagramIR showing component structure

        Example:
            >>> code = '''
            ... function App() {
            ...   return (
            ...     <div>
            ...       <Header />
            ...       <Content />
            ...       <Footer />
            ...     </div>
            ...   );
            ... }
            ... '''
            >>> diagram = analyzer.analyze_react_component(code, 'App')
        """
        diagram = DiagramIR(metadata={"title": f"Component: {component_name}"})

        # Add root component
        diagram.add_node(
            Node(id="root", label=component_name, node_type=NodeType.START)
        )

        # Find JSX elements (simplified)
        jsx_pattern = r"<(\w+)\s*/?>"
        found_components = set()

        for match in re.finditer(jsx_pattern, code):
            component = match.group(1)

            # Skip HTML elements
            if component.lower() == component:
                continue

            if component not in found_components:
                found_components.add(component)
                node_id = f"component_{component}"
                diagram.add_node(
                    Node(id=node_id, label=component, node_type=NodeType.PROCESS)
                )
                diagram.add_edge(
                    Edge(source="root", target=node_id, label="renders")
                )

        return diagram

    def analyze_async_flow(self, code: str) -> DiagramIR:
        """Analyze async/await flow in TypeScript/JavaScript.

        Args:
            code: Code with async operations

        Returns:
            DiagramIR showing async flow

        Example:
            >>> code = '''
            ... async function fetchData() {
            ...   const response = await fetch('/api');
            ...   const data = await response.json();
            ...   return data;
            ... }
            ... '''
            >>> diagram = analyzer.analyze_async_flow(code)
        """
        diagram = DiagramIR(metadata={"title": "Async Flow"})

        diagram.add_node(Node(id="start", label="Start", node_type=NodeType.START))

        node_counter = 0
        last_node = "start"

        # Find await statements
        await_pattern = r"await\s+(.+?)(?:;|\n)"
        for match in re.finditer(await_pattern, code):
            operation = match.group(1).strip()
            node_id = f"async_{node_counter}"
            node_counter += 1

            diagram.add_node(
                Node(id=node_id, label=f"await {operation}", node_type=NodeType.PROCESS)
            )
            diagram.add_edge(Edge(source=last_node, target=node_id))
            last_node = node_id

        # Add end node
        diagram.add_node(Node(id="end", label="End", node_type=NodeType.END))
        diagram.add_edge(Edge(source=last_node, target="end"))

        return diagram


def analyze_package_json(file_path: str) -> DiagramIR:
    """Analyze package.json to show dependency graph.

    Args:
        file_path: Path to package.json

    Returns:
        DiagramIR showing dependencies

    Example:
        >>> diagram = analyze_package_json('package.json')
    """
    with open(file_path) as f:
        package_data = json.load(f)

    diagram = DiagramIR(metadata={"title": "Package Dependencies"})

    pkg_name = package_data.get("name", "package")
    diagram.add_node(Node(id="root", label=pkg_name, node_type=NodeType.START))

    node_counter = 0

    # Add dependencies
    deps = package_data.get("dependencies", {})
    for dep_name in deps.keys():
        node_id = f"dep_{node_counter}"
        node_counter += 1
        diagram.add_node(
            Node(id=node_id, label=dep_name, node_type=NodeType.PROCESS)
        )
        diagram.add_edge(
            Edge(source="root", target=node_id, label="depends on")
        )

    # Add dev dependencies
    dev_deps = package_data.get("devDependencies", {})
    for dep_name in dev_deps.keys():
        node_id = f"dev_{node_counter}"
        node_counter += 1
        diagram.add_node(Node(id=node_id, label=dep_name, node_type=NodeType.DATA))
        diagram.add_edge(
            Edge(
                source="root",
                target=node_id,
                label="dev",
                edge_type=EdgeType.CONDITIONAL,
            )
        )

    return diagram
