"""Comprehensive example showcasing ALL ij features (Phases 1-5).

This example demonstrates every major feature implemented in the ij package,
including the 10 new enhancements added in the latest release.
"""


def example_1_enhanced_cli():
    """Feature 1: Enhanced CLI (use from terminal)."""
    print("=" * 70)
    print("Feature 1: Enhanced CLI with Multi-Format Conversion")
    print("=" * 70)
    print("""
The enhanced CLI (ij2 command) provides powerful features:

# Convert between formats
$ ij2 convert diagram.mmd output.d2
$ ij2 convert --from mermaid --to plantuml flow.mmd

# Validate diagrams
$ ij2 validate *.mmd --no-cycles --max-nodes 50

# Show statistics
$ ij2 stats diagram.mmd

# Simplify diagrams
$ ij2 simplify complex.mmd -o simple.mmd

# Diff two diagrams
$ ij2 diff v1.mmd v2.mmd --verbose

# Extract subgraph
$ ij2 extract diagram.mmd start_node -o subgraph.mmd --depth 3

# Watch for changes
$ ij2 watch input.mmd -o output.d2
""")
    print()


def example_2_validation_and_linting():
    """Feature 2: Diagram Validation & Linting."""
    print("=" * 70)
    print("Feature 2: Diagram Validation & Linting")
    print("=" * 70)

    from ij import DiagramIR, DiagramValidator, DiagramLinter, Edge, Node, NodeType

    # Create a diagram with issues
    diagram = DiagramIR()
    diagram.add_node(Node(id="start", label="Start", node_type=NodeType.START))
    diagram.add_node(Node(id="process", label="Process"))
    diagram.add_node(Node(id="orphan", label="Orphaned Node"))  # Issue!
    diagram.add_edge(Edge(source="start", target="process"))
    diagram.add_edge(Edge(source="process", target="start"))  # Cycle!

    # Validate
    validator = DiagramValidator()
    result = validator.validate(
        diagram, rules=["no-cycles", "no-orphaned-nodes", "require-start-end"]
    )

    print(f"Validation: {'✅ PASS' if result.is_valid else '❌ FAIL'}")
    for issue in result.issues:
        print(f"  [{issue.severity.value.upper()}] {issue.message}")

    # Lint for style
    linter = DiagramLinter()
    lint_issues = linter.lint(diagram)
    print(f"\nLinting found {len(lint_issues)} style issues")
    print()


def example_3_git_integration():
    """Feature 3: Git Integration & Diagram Diff."""
    print("=" * 70)
    print("Feature 3: Git Integration & Diagram Diff")
    print("=" * 70)

    from ij import DiagramIR, DiagramDiff, DiagramHistory, Edge, Node

    # Create two versions
    v1 = DiagramIR()
    v1.add_node(Node(id="a", label="Step A"))
    v1.add_node(Node(id="b", label="Step B"))
    v1.add_edge(Edge(source="a", target="b"))

    v2 = DiagramIR()
    v2.add_node(Node(id="a", label="Step A (Updated)"))  # Modified
    v2.add_node(Node(id="b", label="Step B"))
    v2.add_node(Node(id="c", label="Step C"))  # Added
    v2.add_edge(Edge(source="a", target="b"))
    v2.add_edge(Edge(source="b", target="c"))  # Added

    # Diff
    differ = DiagramDiff()
    changes = differ.compare(v1, v2)

    print(f"Changes detected: {changes.total_changes}")
    print(f"  Added nodes: {len(changes.added_nodes)}")
    print(f"  Modified nodes: {len(changes.modified_nodes)}")
    print(f"  Added edges: {len(changes.added_edges)}")

    # History tracking
    history = DiagramHistory()
    history.add_version("v1.0", v1)
    history.add_version("v2.0", v2)

    print(f"\nVersion history: {history.list_versions()}")
    print()


def example_4_erd_diagrams():
    """Feature 4: Entity-Relationship Diagrams."""
    print("=" * 70)
    print("Feature 4: Entity-Relationship Diagrams")
    print("=" * 70)

    from ij.diagrams import Cardinality, ERDiagram, Entity

    # Create ERD
    erd = ERDiagram(title="E-commerce Database")

    # Add entities
    user = Entity(name="User")
    user.add_field("id", "int", primary_key=True)
    user.add_field("email", "varchar", unique=True, nullable=False)
    user.add_field("name", "varchar")
    erd.add_entity(user)

    order = Entity(name="Order")
    order.add_field("id", "int", primary_key=True)
    order.add_field("user_id", "int", foreign_key="User.id")
    order.add_field("total", "decimal")
    erd.add_entity(order)

    # Add relationship
    erd.add_relationship("User", "Order", Cardinality.ONE_TO_MANY, label="places")

    # Render
    print("Mermaid ER Diagram:")
    print(erd.to_mermaid()[:200] + "...")
    print()


def example_5_state_machines():
    """Feature 5: State Machine Diagrams."""
    print("=" * 70)
    print("Feature 5: State Machine Diagrams")
    print("=" * 70)

    from ij.diagrams import StateMachine, StateType

    # Create state machine
    sm = StateMachine(name="Door Lock", initial_state="locked")
    sm.add_state("locked", state_type=StateType.INITIAL)
    sm.add_state("unlocked", state_type=StateType.NORMAL)
    sm.add_transition("locked", "unlock", "unlocked", action="beep()")
    sm.add_transition("unlocked", "lock", "locked", action="beep()")
    sm.add_transition("unlocked", "timeout", "locked", action="auto_lock()")

    # Validate
    issues = sm.validate()
    print(f"State machine validation: {'✅ Valid' if not issues else f'❌ {len(issues)} issues'}")

    # Simulate
    events = ["unlock", "lock", "unlock", "timeout"]
    path = sm.simulate("locked", events)
    print(f"Simulation path: {' → '.join(path)}")

    print(f"\nMermaid state diagram:\n{sm.to_mermaid()[:150]}...")
    print()


def example_6_image_export():
    """Feature 6: Image Export (SVG/PNG)."""
    print("=" * 70)
    print("Feature 6: Image Export to SVG/PNG/PDF")
    print("=" * 70)

    from ij import DiagramIR, Edge, ImageExporter, Node

    diagram = DiagramIR()
    diagram.add_node(Node(id="a", label="Start"))
    diagram.add_node(Node(id="b", label="Process"))
    diagram.add_edge(Edge(source="a", target="b"))

    # Check available engines
    exporter = ImageExporter()
    available = exporter.check_dependencies()

    print("Available rendering engines:")
    for engine, is_available in available.items():
        status = "✅" if is_available else "❌"
        print(f"  {status} {engine}")

    # Example export (requires graphviz/mermaid-cli/playwright)
    print("\nTo export:")
    print("  exporter = ImageExporter(format='svg', engine='graphviz')")
    print("  exporter.render(diagram, 'output.svg')")
    print()


def example_7_importers():
    """Feature 7: Import from External Sources."""
    print("=" * 70)
    print("Feature 7: Import from External Sources")
    print("=" * 70)

    print("Import from various sources:")
    print("""
# From database schema
from ij.importers import from_database
erd = from_database('postgresql://user:pass@localhost/mydb')

# From OpenAPI spec
from ij.importers import from_openapi
diagram = from_openapi('api.yaml')

# From PlantUML
from ij.importers import from_plantuml
diagram = from_plantuml(plantuml_code)

# From draw.io
from ij.importers import from_drawio
diagram = from_drawio('flowchart.drawio')
""")
    print()


def example_8_typescript_analysis():
    """Feature 8: TypeScript/JavaScript Code Analysis."""
    print("=" * 70)
    print("Feature 8: TypeScript/JavaScript Code Analysis")
    print("=" * 70)

    try:
        from ij.analyzers.typescript import TypeScriptAnalyzer

        code = """
function processPayment(amount) {
  if (amount > 0) {
    validateCard();
    chargeCard(amount);
    return true;
  }
  return false;
}
"""

        analyzer = TypeScriptAnalyzer()
        diagram = analyzer.analyze_function(code, "processPayment")

        print(f"Analyzed TypeScript function:")
        print(f"  Nodes: {len(diagram.nodes)}")
        print(f"  Edges: {len(diagram.edges)}")
        print(f"  Title: {diagram.metadata.get('title')}")
    except:
        print("TypeScript analyzer available but needs Node.js installed")

    print()


def example_9_layout_algorithms():
    """Feature 9: Advanced Layout Algorithms."""
    print("=" * 70)
    print("Feature 9: Advanced Layout Algorithms")
    print("=" * 70)

    from ij import DiagramIR, Edge, LayoutEngine, Node

    # Create diagram
    diagram = DiagramIR()
    for i in range(6):
        diagram.add_node(Node(id=f"n{i}", label=f"Node {i}"))

    diagram.add_edge(Edge(source="n0", target="n1"))
    diagram.add_edge(Edge(source="n0", target="n2"))
    diagram.add_edge(Edge(source="n1", target="n3"))
    diagram.add_edge(Edge(source="n2", target="n4"))
    diagram.add_edge(Edge(source="n3", target="n5"))

    # Try different layouts
    algorithms = ["hierarchical", "force-directed", "circular", "grid"]

    for algo in algorithms:
        engine = LayoutEngine(algorithm=algo)
        positions = engine.apply(diagram)
        print(f"{algo.title()} layout:")
        print(f"  n0 position: {positions['n0']}")

    print()


def example_10_plugin_system():
    """Feature 10: Plugin System."""
    print("=" * 70)
    print("Feature 10: Plugin System for Extensibility")
    print("=" * 70)

    from ij import DiagramIR, PluginManager, register_transform
    from ij.plugins.plugin_manager import Plugin

    # Create custom plugin
    class HighlightPlugin(Plugin):
        name = "highlight_plugin"
        version = "1.0.0"
        description = "Highlight specific nodes"

        def process(self, diagram, node_id=None):
            if node_id:
                for node in diagram.nodes:
                    if node.id == node_id:
                        node.metadata["highlight"] = True
            return diagram

    # Register plugin
    manager = PluginManager()
    manager.register_plugin(HighlightPlugin())

    # Use plugin
    diagram = DiagramIR()
    # ... add nodes ...

    print("Plugin system features:")
    print("  ✅ Custom plugins")
    print("  ✅ Transform functions")
    print("  ✅ Event hooks")
    print("  ✅ Plugin discovery")
    print()


def example_11_web_viewer():
    """Feature 11: Interactive Web Viewer."""
    print("=" * 70)
    print("Feature 11: Interactive Web Viewer")
    print("=" * 70)

    print("Start interactive web viewer:")
    print("""
from ij import serve_diagram, DiagramIR, Node, Edge

diagram = DiagramIR()
# ... build diagram ...

# Launch interactive viewer
serve_diagram(diagram, port=8080, theme='dark')

Features:
  🌐 Web-based viewing
  🔄 Live auto-refresh
  🎨 Multiple themes
  🖨️ Print support
  📱 Responsive design
""")
    print()


def example_12_complete_workflow():
    """Example 12: Complete end-to-end workflow."""
    print("=" * 70)
    print("Example 12: Complete End-to-End Workflow")
    print("=" * 70)

    from ij import (
        DiagramIR,
        DiagramTransforms,
        DiagramValidator,
        Edge,
        MermaidRenderer,
        Node,
        NodeType,
    )

    # 1. Create diagram
    diagram = DiagramIR(metadata={"title": "Order Processing"})
    diagram.add_node(Node(id="start", label="Receive Order", node_type=NodeType.START))
    diagram.add_node(Node(id="validate", label="Validate", node_type=NodeType.DECISION))
    diagram.add_node(Node(id="process", label="Process Payment"))
    diagram.add_node(Node(id="ship", label="Ship Order"))
    diagram.add_node(Node(id="end", label="Complete", node_type=NodeType.END))

    diagram.add_edge(Edge(source="start", target="validate"))
    diagram.add_edge(Edge(source="validate", target="process", label="Valid"))
    diagram.add_edge(Edge(source="validate", target="end", label="Invalid"))
    diagram.add_edge(Edge(source="process", target="ship"))
    diagram.add_edge(Edge(source="ship", target="end"))

    # 2. Validate
    validator = DiagramValidator()
    result = validator.validate(diagram)
    print(f"Step 1: Validation {'✅ Passed' if result.is_valid else '❌ Failed'}")

    # 3. Get statistics
    stats = DiagramTransforms.get_statistics(diagram)
    print(f"Step 2: Statistics - {stats['node_count']} nodes, {stats['edge_count']} edges")

    # 4. Simplify
    simplified = DiagramTransforms.simplify(diagram)
    print(f"Step 3: Simplified to {len(simplified.nodes)} nodes")

    # 5. Render to multiple formats
    renderer = MermaidRenderer()
    mermaid = renderer.render(diagram)
    print(f"Step 4: Rendered to Mermaid ({len(mermaid)} chars)")

    # 6. Export
    print("Step 5: Ready to export as SVG/PNG or serve in web viewer")
    print()


if __name__ == "__main__":
    print("\n")
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 15 + "IJ - Idea Junction v0.2.0" + " " * 28 + "║")
    print("║" + " " * 12 + "Comprehensive Feature Showcase" + " " * 25 + "║")
    print("╚" + "═" * 68 + "╝")
    print("\n")

    # Run all examples
    example_1_enhanced_cli()
    example_2_validation_and_linting()
    example_3_git_integration()
    example_4_erd_diagrams()
    example_5_state_machines()
    example_6_image_export()
    example_7_importers()
    example_8_typescript_analysis()
    example_9_layout_algorithms()
    example_10_plugin_system()
    example_11_web_viewer()
    example_12_complete_workflow()

    print("=" * 70)
    print("🎉 All Features Demonstrated!")
    print("=" * 70)
    print("\n📚 For more information:")
    print("  - Documentation: See PHASE*.md files")
    print("  - Examples: See examples/ directory")
    print("  - CLI Help: ij2 --help")
    print("\n✨ Happy diagramming with ij!")
