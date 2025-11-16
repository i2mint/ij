# ij - Idea Junction

**Connect vague ideas and evolve them to fully functional systems**

Idea Junction (ij) is a bidirectional diagramming system that enables seamless movement between natural language, visual diagrams, and code. Built on research into modern diagramming tools and best practices, it provides a foundation for transforming ideas into structured, analyzable diagrams.

## Features

- **Text-to-Diagram Conversion**: Convert simple text descriptions into Mermaid diagrams
- **Intermediate Representation (IR)**: AST-like structure for bidirectional conversion
- **Graph Analysis**: Powered by NetworkX for path finding, cycle detection, and graph manipulation
- **Multiple Formats**: Currently supports Mermaid (GitHub-native), extensible to PlantUML, D2, and more
- **CLI & Python API**: Use as a command-line tool or integrate into your Python projects
- **Type-Safe**: Full type hints and validation

## Installation

```bash
pip install ij
```

Or install from source:

```bash
git clone https://github.com/i2mint/ij
cd ij
pip install -e .
```

## Quick Start

### Command Line

```bash
# Convert text to Mermaid diagram
ij "Start -> Process data -> Make decision -> End"

# Save to file
ij "Step 1 -> Step 2 -> Step 3" -o diagram.mmd

# Specify direction
ij "A -> B -> C" -d LR -o horizontal.mmd

# Read from file
ij -f process.txt -o output.mmd
```

### Python API

```python
from ij import text_to_mermaid

# Simple conversion
mermaid = text_to_mermaid("Start -> Process -> End")
print(mermaid)
```

Output:
```mermaid
flowchart TD
    n0([Start])
    n1[Process]
    n2([End])
    n0 --> n1
    n1 --> n2
```

### Manual Diagram Creation

```python
from ij import DiagramIR, Node, Edge, NodeType, MermaidRenderer

# Create diagram programmatically
diagram = DiagramIR(metadata={"title": "My Process"})

diagram.add_node(Node(id="start", label="Start", node_type=NodeType.START))
diagram.add_node(Node(id="process", label="Do work", node_type=NodeType.PROCESS))
diagram.add_node(Node(id="end", label="End", node_type=NodeType.END))

diagram.add_edge(Edge(source="start", target="process"))
diagram.add_edge(Edge(source="process", target="end"))

# Render to Mermaid
renderer = MermaidRenderer(direction="LR")
print(renderer.render(diagram))
```

### Graph Analysis

```python
from ij import DiagramIR, Node, Edge
from ij.graph_ops import GraphOperations

# Create a workflow
diagram = DiagramIR()
diagram.add_node(Node(id="a", label="Start"))
diagram.add_node(Node(id="b", label="Task 1"))
diagram.add_node(Node(id="c", label="Task 2"))
diagram.add_node(Node(id="d", label="End"))

diagram.add_edge(Edge(source="a", target="b"))
diagram.add_edge(Edge(source="b", target="c"))
diagram.add_edge(Edge(source="c", target="d"))
diagram.add_edge(Edge(source="a", target="d"))  # Shortcut path

# Find all paths
paths = GraphOperations.find_paths(diagram, "a", "d")
print(f"Found {len(paths)} paths")  # Output: Found 2 paths

# Get topological order
order = GraphOperations.topological_sort(diagram)
print(order)  # Output: ['a', 'b', 'c', 'd']

# Simplify (remove redundant edges)
simplified = GraphOperations.simplify_diagram(diagram)
```

## Architecture

Based on comprehensive research into bidirectional diagramming systems, ij uses:

- **AST-based IR**: Core data structure for diagram representation
- **Graph Model**: NetworkX for analysis and transformation
- **Extensible Renderers**: Pluggable output formats (Mermaid, PlantUML, D2, etc.)
- **Text-based DSL**: Git-friendly, version-controllable diagram source

```
Natural Language → DiagramIR → Mermaid/PlantUML/D2
                      ↓
                  NetworkX Graph
                      ↓
                Analysis & Transformation
```

## Node Types

ij supports several node types with automatic inference:

- `START`: Beginning of a process (stadium shape in Mermaid)
- `END`: End of a process (stadium shape)
- `PROCESS`: Processing step (rectangle)
- `DECISION`: Decision point (diamond)
- `DATA`: Data storage (cylinder)
- `SUBPROCESS`: Sub-process (double rectangle)

Keywords like "Start", "End", "decide", "database" automatically set the correct type.

## Examples

See the [examples/](examples/) directory for comprehensive usage examples:

```bash
python examples/basic_usage.py
```

Examples include:
- Simple text-to-diagram conversion
- Manual diagram creation
- Graph analysis (path finding, topological sort)
- Different diagram directions
- Natural language processing
- Saving diagrams to files

## Viewing Diagrams

Generated Mermaid diagrams can be viewed in:

1. **GitHub/GitLab** - Paste in markdown files (native support)
2. **Mermaid Live Editor** - https://mermaid.live/
3. **VS Code** - Install Mermaid preview extension
4. **Command line** - Use `mmdc` (Mermaid CLI)

Example in markdown:

````markdown
```mermaid
flowchart TD
    A[Start] --> B{Decision?}
    B -->|Yes| C[Process]
    B -->|No| D[Skip]
    C --> E[End]
    D --> E
```
````

## Development

### Running Tests

```bash
pip install -e ".[dev]"
pytest tests/ -v
```

All tests should pass:
```
26 passed in 0.37s
```

### Code Quality

```bash
# Run linter
ruff check ij/

# Format code
ruff format ij/
```

## Roadmap

### Phase 1 (Current) ✅
- [x] Core DiagramIR architecture
- [x] Mermaid renderer
- [x] NetworkX integration
- [x] CLI interface
- [x] Basic text-to-diagram conversion
- [x] Comprehensive tests

### Phase 2 (Next)
- [ ] Diagram parser (Mermaid → IR)
- [ ] PlantUML renderer
- [ ] D2 renderer
- [ ] Enhanced NLP for text conversion
- [ ] Graphviz renderer

### Phase 3 (Future)
- [ ] AI/LLM integration for natural language
- [ ] Visual editor integration
- [ ] Real-time collaboration (CRDT-based)
- [ ] Code-to-diagram reverse engineering
- [ ] Multiple diagram views from single source

## Research Foundation

This project is built on comprehensive research into:

- Diagram-as-code languages (Mermaid, PlantUML, D2, Graphviz)
- Python libraries (NetworkX, diagrams, graphviz)
- JavaScript frameworks (React Flow, Cytoscape.js)
- Bidirectional editing patterns
- AI-powered generation
- Technical architecture patterns

See [misc/REASEARCH.md](misc/REASEARCH.md) for the full research report.

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## License

MIT License - see LICENSE file for details

## Links

- **Repository**: https://github.com/i2mint/ij
- **Issues**: https://github.com/i2mint/ij/issues
- **Mermaid Docs**: https://mermaid.js.org
- **NetworkX Docs**: https://networkx.org

---

**Idea Junction** - From vague ideas to fully functional systems
