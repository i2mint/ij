# ij

Idea Junction - Connect vague ideas and evolve them to fully functional systems.

A bidirectional diagramming system that enables seamless movement between
natural language, visual diagrams, and code.

### Functions

| [`quick_export`](#ij.quick_export)(diagram, output_path[, format, ...])   | Quick export diagram to image.                                      |
|------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------|
| [`register_plugin`](#ij.register_plugin)(plugin)                             | Register plugin with global manager.                                |
| [`register_transform`](#ij.register_transform)(name)                            | Decorator to register a transform function.                         |
| [`serve_diagram`](#ij.serve_diagram)(diagram[, port, theme, ...])          | Quickly serve a diagram in browser.                                 |
| [`text_to_mermaid`](#ij.text_to_mermaid)(text[, title, direction])           | Convert text description to Mermaid diagram (convenience function). |
| [`analyze_package_json`](#ij.analyze_package_json)(file_path)                     | Analyze package.json to show dependency graph.                      |

### Classes

| [`DiagramIR`](#ij.DiagramIR)([nodes, edges, metadata])               | Intermediate Representation for diagrams.                                    |
|----------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------|
| [`Node`](#ij.Node)(id, label[, node_type, metadata])            | Represents a node in the diagram IR.                                         |
| [`Edge`](#ij.Edge)(source, target[, label, edge_type, ...])     | Represents an edge in the diagram IR.                                        |
| [`NodeType`](#ij.NodeType)(\*values)                                | Types of nodes in a diagram.                                                 |
| [`EdgeType`](#ij.EdgeType)(\*values)                                | Types of edges connecting nodes.                                             |
| [`SimpleTextConverter`](#ij.SimpleTextConverter)()                             | Simple rule-based text to diagram converter.                                 |
| [`EnhancedTextConverter`](#ij.EnhancedTextConverter)()                           | Enhanced text-to-diagram converter with NLP capabilities.                    |
| [`MermaidRenderer`](#ij.MermaidRenderer)([direction])                      | Renders DiagramIR to Mermaid syntax.                                         |
| [`PlantUMLRenderer`](#ij.PlantUMLRenderer)([use_skinparam])                 | Renders DiagramIR to PlantUML activity diagram syntax.                       |
| [`D2Renderer`](#ij.D2Renderer)([layout])                              | Renders DiagramIR to D2 syntax.                                              |
| [`GraphvizRenderer`](#ij.GraphvizRenderer)([layout, graph_type])            | Renders DiagramIR to Graphviz DOT syntax.                                    |
| [`SequenceDiagramRenderer`](#ij.SequenceDiagramRenderer)()                         | Render DiagramIR as Mermaid sequence diagram.                                |
| [`InteractionAnalyzer`](#ij.InteractionAnalyzer)()                             | Analyze code or text to identify interaction patterns for sequence diagrams. |
| [`MermaidParser`](#ij.MermaidParser)(\*[, strict])                       | Parses Mermaid flowchart syntax to DiagramIR.                                |
| [`D2Parser`](#ij.D2Parser)()                                        | Parse D2 syntax to DiagramIR.                                                |
| [`GraphOperations`](#ij.GraphOperations)()                                 | Graph manipulation and analysis using NetworkX.                              |
| [`PythonCodeAnalyzer`](#ij.PythonCodeAnalyzer)()                              | Analyze Python code to generate diagrams.                                    |
| [`DiagramTransforms`](#ij.DiagramTransforms)()                               | Transform and optimize diagram structures.                                   |
| [`DiagramValidator`](#ij.DiagramValidator)()                                | Validate diagrams against various rules.                                     |
| [`DiagramLinter`](#ij.DiagramLinter)()                                   | Lint diagrams for style and best practices.                                  |
| [`ValidationResult`](#ij.ValidationResult)(is_valid, issues)                | Result of diagram validation.                                                |
| [`DiagramDiff`](#ij.DiagramDiff)()                                     | Compare and diff diagrams.                                                   |
| [`DiagramHistory`](#ij.DiagramHistory)()                                  | Track diagram history and changes over time.                                 |
| [`ERDiagram`](#ij.ERDiagram)([title])                                | Entity-Relationship Diagram.                                                 |
| [`Entity`](#ij.Entity)(name[, fields, metadata])                  | An entity in an ERD.                                                         |
| [`Field`](#ij.Field)(name, type[, primary_key, ...])             | A field in an entity.                                                        |
| [`Cardinality`](#ij.Cardinality)(\*values)                             | Relationship cardinality.                                                    |
| [`StateMachine`](#ij.StateMachine)([name, initial_state])               | Finite State Machine diagram.                                                |
| [`State`](#ij.State)(name[, state_type, on_enter, on_exit, ...]) | A state in a state machine.                                                  |
| [`ImageExporter`](#ij.ImageExporter)([format, engine])                   | Export diagrams to image formats.                                            |
| [`LayoutEngine`](#ij.LayoutEngine)([algorithm])                         | Apply layout algorithms to diagrams.                                         |
| [`ForceDirectedLayout`](#ij.ForceDirectedLayout)([iterations, ...])            | Force-directed layout using Fruchterman-Reingold algorithm.                  |
| [`HierarchicalLayout`](#ij.HierarchicalLayout)([direction, ...])              | Hierarchical layout using Sugiyama algorithm.                                |
| [`PluginManager`](#ij.PluginManager)()                                   | Manage and execute plugins.                                                  |
| [`ViewerServer`](#ij.ViewerServer)([port, theme])                       | Interactive web server for diagram viewing.                                  |
| [`LLMConverter`](#ij.LLMConverter)([api_key, model, temperature])       | AI-powered text to diagram converter using LLMs.                             |
| [`TypeScriptAnalyzer`](#ij.TypeScriptAnalyzer)()                              | Analyze TypeScript/JavaScript code to create diagrams.                       |

### Exceptions

| [`MermaidParseWarning`](#ij.MermaidParseWarning)   | Warns that a Mermaid line could not be interpreted and was skipped.   |
|------------------------------------------------------------------------|-----------------------------------------------------------------------|

### *class* ij.Cardinality(\*values)

Bases: [`Enum`](https://docs.python.org/3/library/enum.html#enum.Enum)

Relationship cardinality.

### *class* ij.D2Parser

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

Parse D2 syntax to DiagramIR.

Supports basic D2 syntax including:

- Node definitions with shapes and labels
- Edge connections with labels
- Direction metadata

#### parse(d2_text)

Parse D2 syntax to DiagramIR.

* **Parameters:**
  **d2_text** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – D2 diagram source
* **Return type:**
  [`DiagramIR`](ij.core.md#ij.core.DiagramIR)
* **Returns:**
  DiagramIR representation

### Example

```pycon
>>> parser = D2Parser()
>>> d2_code = '''
... n1: "Start" {
...   shape: oval
... }
... n2: "Process" {
...   shape: rectangle
... }
... n1 -> n2
... '''
>>> diagram = parser.parse(d2_code)
```

#### parse_file(filename)

Parse D2 file to DiagramIR.

* **Parameters:**
  **filename** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Path to D2 file
* **Return type:**
  [`DiagramIR`](ij.core.md#ij.core.DiagramIR)
* **Returns:**
  DiagramIR representation

### *class* ij.D2Renderer(layout='dagre')

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

Renders DiagramIR to D2 syntax.

D2 is a modern diagram language with clean syntax, multiple layout engines,
and PowerPoint export capabilities.

#### render(diagram)

Render a DiagramIR to D2 syntax.

* **Parameters:**
  **diagram** ([`DiagramIR`](ij.core.md#ij.core.DiagramIR)) – The diagram to render
* **Return type:**
  [`str`](https://docs.python.org/3/builtins/stdtypes.html#str)
* **Returns:**
  D2 syntax as a string

#### render_to_file(diagram, filename)

Render diagram and save to file.

* **Parameters:**
  * **diagram** ([`DiagramIR`](ij.core.md#ij.core.DiagramIR)) – The diagram to render
  * **filename** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Path to output file
* **Return type:**
  [`None`](https://docs.python.org/3/builtins/constants.html#None)

### *class* ij.DiagramDiff

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

Compare and diff diagrams.

#### compare(diagram1, diagram2)

Compare two diagrams.

* **Parameters:**
  * **diagram1** ([`DiagramIR`](ij.core.md#ij.core.DiagramIR)) – Original diagram
  * **diagram2** ([`DiagramIR`](ij.core.md#ij.core.DiagramIR)) – Modified diagram
* **Return type:**
  [`DiagramChanges`](ij.git_integration.md#ij.git_integration.DiagramChanges)
* **Returns:**
  DiagramChanges describing differences

### Example

```pycon
>>> differ = DiagramDiff()
>>> changes = differ.compare(old_diagram, new_diagram)
>>> print(f"Added: {len(changes.added_nodes)} nodes")
```

#### compare_files(file1, file2)

Compare two diagram files.

* **Parameters:**
  * **file1** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Path to first diagram
  * **file2** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Path to second diagram
* **Return type:**
  [`DiagramChanges`](ij.git_integration.md#ij.git_integration.DiagramChanges)
* **Returns:**
  DiagramChanges describing differences

#### generate_diff_report(changes)

Generate human-readable diff report.

* **Parameters:**
  **changes** ([`DiagramChanges`](ij.git_integration.md#ij.git_integration.DiagramChanges)) – DiagramChanges to report
* **Return type:**
  [`str`](https://docs.python.org/3/builtins/stdtypes.html#str)
* **Returns:**
  Formatted diff report string

#### merge(base, branch1, branch2, strategy='union')

Merge two diagram versions with a common base.

* **Parameters:**
  * **base** ([`DiagramIR`](ij.core.md#ij.core.DiagramIR)) – Common ancestor diagram
  * **branch1** ([`DiagramIR`](ij.core.md#ij.core.DiagramIR)) – First modified version
  * **branch2** ([`DiagramIR`](ij.core.md#ij.core.DiagramIR)) – Second modified version
  * **strategy** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Merge strategy (‘union’, ‘intersection’, ‘ours’, ‘theirs’)
* **Return type:**
  [`DiagramIR`](ij.core.md#ij.core.DiagramIR)
* **Returns:**
  Merged DiagramIR

### Example

```pycon
>>> differ = DiagramDiff()
>>> merged = differ.merge(base, branch1, branch2, strategy='union')
```

### *class* ij.DiagramHistory

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

Track diagram history and changes over time.

#### add_version(name, diagram)

Add a version to history.

* **Parameters:**
  * **name** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Version name/identifier
  * **diagram** ([`DiagramIR`](ij.core.md#ij.core.DiagramIR)) – DiagramIR snapshot

#### compare_versions(name1, name2)

Compare two versions.

* **Parameters:**
  * **name1** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – First version name
  * **name2** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Second version name
* **Return type:**
  [`DiagramChanges`](ij.git_integration.md#ij.git_integration.DiagramChanges)
* **Returns:**
  DiagramChanges between versions

#### get_changelog()

Generate changelog across all versions.

* **Return type:**
  [`str`](https://docs.python.org/3/builtins/stdtypes.html#str)
* **Returns:**
  Formatted changelog string

#### get_version(name)

Get a specific version.

* **Parameters:**
  **name** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Version name
* **Return type:**
  [`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`DiagramIR`](ij.core.md#ij.core.DiagramIR)]
* **Returns:**
  DiagramIR if found, None otherwise

#### list_versions()

List all version names.

* **Return type:**
  [`List`](https://docs.python.org/3/library/typing.html#typing.List)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]

### *class* ij.DiagramIR(nodes=<factory>, edges=<factory>, metadata=<factory>)

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

Intermediate Representation for diagrams.

This serves as the central data structure that can be:

- Generated from natural language
- Converted to various diagram formats (Mermaid, PlantUML, D2)
- Manipulated programmatically
- Parsed back from diagram syntax

#### nodes

List of nodes in the diagram

#### edges

List of edges connecting nodes

#### metadata

Diagram-level properties (title, description, etc.)

#### add_edge(edge)

Add an edge to the diagram.

* **Return type:**
  [`None`](https://docs.python.org/3/builtins/constants.html#None)

#### add_node(node)

Add a node to the diagram.

* **Return type:**
  [`None`](https://docs.python.org/3/builtins/constants.html#None)

#### get_node(node_id)

Get a node by ID.

* **Return type:**
  [`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`Node`](ij.core.md#ij.core.Node)]

#### validate()

Validate the diagram structure.

* **Return type:**
  [`bool`](https://docs.python.org/3/builtins/functions.html#bool)
* **Returns:**
  True if the diagram is valid, False otherwise

### *class* ij.DiagramLinter

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

Lint diagrams for style and best practices.

#### lint(diagram)

Lint diagram for style issues.

* **Parameters:**
  **diagram** ([`DiagramIR`](ij.core.md#ij.core.DiagramIR)) – DiagramIR to lint
* **Return type:**
  [`List`](https://docs.python.org/3/library/typing.html#typing.List)[[`ValidationIssue`](ij.validation.md#ij.validation.ValidationIssue)]
* **Returns:**
  List of linting issues

### Example

```pycon
>>> linter = DiagramLinter()
>>> issues = linter.lint(diagram)
>>> for issue in issues:
...     print(f"{issue.severity.value.upper()}: {issue.message}")
```

### *class* ij.DiagramTransforms

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

Transform and optimize diagram structures.

#### *static* apply_node_filter(diagram, predicate)

Filter nodes using a custom predicate function.

* **Parameters:**
  * **diagram** ([`DiagramIR`](ij.core.md#ij.core.DiagramIR)) – DiagramIR to filter
  * **predicate** ([`Callable`](https://docs.python.org/3/library/typing.html#typing.Callable)[[[`Node`](ij.core.md#ij.core.Node)], [`bool`](https://docs.python.org/3/builtins/functions.html#bool)]) – Function that returns True for nodes to keep
* **Return type:**
  [`DiagramIR`](ij.core.md#ij.core.DiagramIR)
* **Returns:**
  Filtered DiagramIR

### Example

```pycon
>>> # Keep only nodes with labels containing "error"
>>> filtered = DiagramTransforms.apply_node_filter(
...     diagram, lambda n: "error" in n.label.lower()
... )
```

#### *static* extract_subgraph(diagram, root_node_id, max_depth=None)

Extract subgraph starting from a root node.

* **Parameters:**
  * **diagram** ([`DiagramIR`](ij.core.md#ij.core.DiagramIR)) – Source DiagramIR
  * **root_node_id** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – ID of root node
  * **max_depth** ([`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`int`](https://docs.python.org/3/builtins/functions.html#int)]) – Maximum depth to traverse (None = unlimited)
* **Return type:**
  [`DiagramIR`](ij.core.md#ij.core.DiagramIR)
* **Returns:**
  DiagramIR containing subgraph

### Example

```pycon
>>> # Extract subgraph from node 'start' with depth 2
>>> subgraph = DiagramTransforms.extract_subgraph(diagram, "start", max_depth=2)
```

#### *static* filter_by_node_type(diagram, node_types, keep=True)

Filter diagram by node types.

* **Parameters:**
  * **diagram** ([`DiagramIR`](ij.core.md#ij.core.DiagramIR)) – DiagramIR to filter
  * **node_types** ([`List`](https://docs.python.org/3/library/typing.html#typing.List)[[`NodeType`](ij.core.md#ij.core.NodeType)]) – List of NodeTypes to filter
  * **keep** ([`bool`](https://docs.python.org/3/builtins/functions.html#bool)) – If True, keep only these types; if False, remove these types
* **Return type:**
  [`DiagramIR`](ij.core.md#ij.core.DiagramIR)
* **Returns:**
  Filtered DiagramIR

### Example

```pycon
>>> # Keep only PROCESS nodes
>>> filtered = DiagramTransforms.filter_by_node_type(
...     diagram, [NodeType.PROCESS], keep=True
... )
```

#### *static* find_cycles(diagram)

Find all cycles in the diagram.

* **Parameters:**
  **diagram** ([`DiagramIR`](ij.core.md#ij.core.DiagramIR)) – DiagramIR to analyze
* **Return type:**
  [`List`](https://docs.python.org/3/library/typing.html#typing.List)[[`List`](https://docs.python.org/3/library/typing.html#typing.List)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]]
* **Returns:**
  List of cycles, where each cycle is a list of node IDs

### Example

```pycon
>>> cycles = DiagramTransforms.find_cycles(diagram)
>>> if cycles:
...     print(f"Found {len(cycles)} cycles")
```

#### *static* get_statistics(diagram)

Get statistics about the diagram.

* **Parameters:**
  **diagram** ([`DiagramIR`](ij.core.md#ij.core.DiagramIR)) – DiagramIR to analyze
* **Return type:**
  [`dict`](https://docs.python.org/3/builtins/stdtypes.html#dict)
* **Returns:**
  Dictionary containing diagram statistics

### Example

```pycon
>>> stats = DiagramTransforms.get_statistics(diagram)
>>> print(f"Nodes: {stats['node_count']}, Edges: {stats['edge_count']}")
```

#### *static* merge_diagrams(diagrams, title=None)

Merge multiple diagrams into one.

* **Parameters:**
  * **diagrams** ([`List`](https://docs.python.org/3/library/typing.html#typing.List)[[`DiagramIR`](ij.core.md#ij.core.DiagramIR)]) – List of DiagramIR to merge
  * **title** ([`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]) – Optional title for merged diagram
* **Return type:**
  [`DiagramIR`](ij.core.md#ij.core.DiagramIR)
* **Returns:**
  Merged DiagramIR

### Example

```pycon
>>> diagram1 = DiagramIR()
>>> diagram2 = DiagramIR()
>>> merged = DiagramTransforms.merge_diagrams([diagram1, diagram2])
```

#### *static* merge_sequential_nodes(diagram, separator=' → ')

Merge sequential nodes into single nodes.

Combines nodes that form a linear sequence with no branching.

* **Parameters:**
  * **diagram** ([`DiagramIR`](ij.core.md#ij.core.DiagramIR)) – DiagramIR to transform
  * **separator** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – String to join labels
* **Return type:**
  [`DiagramIR`](ij.core.md#ij.core.DiagramIR)
* **Returns:**
  DiagramIR with merged nodes

#### *static* reverse_edges(diagram)

Reverse all edge directions in the diagram.

* **Parameters:**
  **diagram** ([`DiagramIR`](ij.core.md#ij.core.DiagramIR)) – DiagramIR to reverse
* **Return type:**
  [`DiagramIR`](ij.core.md#ij.core.DiagramIR)
* **Returns:**
  DiagramIR with reversed edges

### Example

```pycon
>>> reversed_diagram = DiagramTransforms.reverse_edges(diagram)
```

#### *static* simplify(diagram, remove_isolated=True)

Simplify diagram by removing redundant nodes and edges.

* **Parameters:**
  * **diagram** ([`DiagramIR`](ij.core.md#ij.core.DiagramIR)) – DiagramIR to simplify
  * **remove_isolated** ([`bool`](https://docs.python.org/3/builtins/functions.html#bool)) – Remove nodes with no connections
* **Return type:**
  [`DiagramIR`](ij.core.md#ij.core.DiagramIR)
* **Returns:**
  Simplified DiagramIR

### Example

```pycon
>>> from ij import DiagramIR, Node, Edge
>>> diagram = DiagramIR()
>>> diagram.add_node(Node(id="a", label="A"))
>>> diagram.add_node(Node(id="isolated", label="Isolated"))
>>> diagram.add_edge(Edge(source="a", target="b"))
>>> simplified = DiagramTransforms.simplify(diagram)
>>> len(simplified.nodes)  # isolated node removed; "b" was never added as a Node
1
```

### *class* ij.DiagramValidator

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

Validate diagrams against various rules.

#### validate(diagram, rules=None)

Validate diagram against rules.

* **Parameters:**
  * **diagram** ([`DiagramIR`](ij.core.md#ij.core.DiagramIR)) – DiagramIR to validate
  * **rules** ([`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`List`](https://docs.python.org/3/library/typing.html#typing.List)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]]) – List of rule names to check (None = all rules)
* **Return type:**
  [`ValidationResult`](ij.validation.md#ij.validation.ValidationResult)
* **Returns:**
  ValidationResult with issues found

### Example

```pycon
>>> validator = DiagramValidator()
>>> result = validator.validate(diagram, rules=['no-cycles', 'no-orphaned-nodes'])
>>> if not result.is_valid:
...     for issue in result.errors:
...         print(f"ERROR: {issue.message}")
```

### *class* ij.ERDiagram(title=None)

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

Entity-Relationship Diagram.

#### add_entity(entity)

Add an entity to the diagram.

#### add_relationship(from_entity, to_entity, cardinality, label=None)

Add a relationship between entities.

#### to_d2()

Render ERD as D2 diagram.

* **Return type:**
  [`str`](https://docs.python.org/3/builtins/stdtypes.html#str)
* **Returns:**
  D2 syntax

#### to_mermaid()

Render ERD as Mermaid ER diagram.

* **Return type:**
  [`str`](https://docs.python.org/3/builtins/stdtypes.html#str)
* **Returns:**
  Mermaid ER diagram syntax

#### to_plantuml()

Render ERD as PlantUML class diagram.

* **Return type:**
  [`str`](https://docs.python.org/3/builtins/stdtypes.html#str)
* **Returns:**
  PlantUML syntax

### *class* ij.Edge(source, target, label=None, edge_type=EdgeType.DIRECT, metadata=<factory>)

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

Represents an edge in the diagram IR.

#### source

Source node ID

#### target

Target node ID

#### label

Optional edge label

#### edge_type

Type of edge

#### metadata

Additional properties for extensibility

### *class* ij.EdgeType(\*values)

Bases: [`Enum`](https://docs.python.org/3/library/enum.html#enum.Enum)

Types of edges connecting nodes.

### *class* ij.EnhancedTextConverter

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

Enhanced text-to-diagram converter with NLP capabilities.

Supports:

- Conditional branches (if/else)
- Parallel flows (parallel keyword)
- Loops (while, repeat)
- Better keyword detection
- Multiple sentence formats

#### convert(text, title=None)

Convert enhanced text to DiagramIR.

* **Parameters:**
  * **text** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Input text describing a process/flow
  * **title** ([`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]) – Optional diagram title
* **Return type:**
  [`DiagramIR`](ij.core.md#ij.core.DiagramIR)
* **Returns:**
  DiagramIR representation

### Examples

```pycon
>>> converter = EnhancedTextConverter()
>>> # Conditional
>>> diagram = converter.convert("Start -> Check user. If authenticated: Show dashboard, else: Show login")
>>> # Parallel
>>> diagram = converter.convert("Start -> [parallel: Process A, Process B] -> End")
```

### *class* ij.Entity(name, fields=<factory>, metadata=<factory>)

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

An entity in an ERD.

#### add_field(name, field_type, primary_key=False, foreign_key=None, nullable=True, unique=False)

Add a field to the entity.

### *class* ij.Field(name, type, primary_key=False, foreign_key=None, nullable=True, unique=False)

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

A field in an entity.

### *class* ij.ForceDirectedLayout(iterations=100, optimal_distance=100, repulsion_strength=5000, attraction_strength=0.1, cooling_factor=0.95)

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

Force-directed layout using Fruchterman-Reingold algorithm.

#### compute(diagram)

Compute node positions using force-directed layout.

* **Parameters:**
  **diagram** ([`DiagramIR`](ij.core.md#ij.core.DiagramIR)) – DiagramIR to layout
* **Return type:**
  [`Dict`](https://docs.python.org/3/library/typing.html#typing.Dict)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str), [`Tuple`](https://docs.python.org/3/library/typing.html#typing.Tuple)[[`float`](https://docs.python.org/3/builtins/functions.html#float), [`float`](https://docs.python.org/3/builtins/functions.html#float)]]
* **Returns:**
  Dictionary mapping node IDs to (x, y) positions

### *class* ij.GraphOperations

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

Graph manipulation and analysis using NetworkX.

#### *static* find_critical_nodes(diagram)

Find nodes whose removal would disconnect the graph.

* **Parameters:**
  **diagram** ([`DiagramIR`](ij.core.md#ij.core.DiagramIR)) – DiagramIR to analyze
* **Return type:**
  [`Set`](https://docs.python.org/3/library/typing.html#typing.Set)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]
* **Returns:**
  Set of critical node IDs

#### *static* find_cycles(diagram)

Find all cycles in the diagram.

* **Parameters:**
  **diagram** ([`DiagramIR`](ij.core.md#ij.core.DiagramIR)) – DiagramIR to analyze
* **Return type:**
  [`List`](https://docs.python.org/3/library/typing.html#typing.List)[[`List`](https://docs.python.org/3/library/typing.html#typing.List)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]]
* **Returns:**
  List of cycles (each cycle is a list of node IDs)

#### *static* find_paths(diagram, source, target)

Find all paths between two nodes.

* **Parameters:**
  * **diagram** ([`DiagramIR`](ij.core.md#ij.core.DiagramIR)) – DiagramIR to analyze
  * **source** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Source node ID
  * **target** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Target node ID
* **Return type:**
  [`List`](https://docs.python.org/3/library/typing.html#typing.List)[[`List`](https://docs.python.org/3/library/typing.html#typing.List)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]]
* **Returns:**
  List of paths (each path is a list of node IDs)

#### *static* from_networkx(G)

Convert NetworkX graph to DiagramIR.

* **Parameters:**
  **G** (`DiGraph`) – NetworkX directed graph
* **Return type:**
  [`DiagramIR`](ij.core.md#ij.core.DiagramIR)
* **Returns:**
  DiagramIR representation

#### *static* simplify_diagram(diagram, remove_redundant=True)

Simplify diagram by removing redundant edges and nodes.

* **Parameters:**
  * **diagram** ([`DiagramIR`](ij.core.md#ij.core.DiagramIR)) – DiagramIR to simplify
  * **remove_redundant** ([`bool`](https://docs.python.org/3/builtins/functions.html#bool)) – If True, remove transitive edges
* **Return type:**
  [`DiagramIR`](ij.core.md#ij.core.DiagramIR)
* **Returns:**
  Simplified DiagramIR

#### *static* to_networkx(diagram)

Convert DiagramIR to NetworkX directed graph.

* **Parameters:**
  **diagram** ([`DiagramIR`](ij.core.md#ij.core.DiagramIR)) – DiagramIR to convert
* **Return type:**
  `DiGraph`
* **Returns:**
  NetworkX DiGraph

#### *static* topological_sort(diagram)

Get topological ordering of nodes (for DAGs).

* **Parameters:**
  **diagram** ([`DiagramIR`](ij.core.md#ij.core.DiagramIR)) – DiagramIR to sort
* **Return type:**
  [`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`List`](https://docs.python.org/3/library/typing.html#typing.List)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]]
* **Returns:**
  List of node IDs in topological order, or None if graph has cycles

### *class* ij.GraphvizRenderer(layout='dot', graph_type='digraph')

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

Renders DiagramIR to Graphviz DOT syntax.

Graphviz is the 30-year-old foundation that underpins PlantUML,
Structurizr, and many other tools.

#### render(diagram)

Render a DiagramIR to DOT syntax.

* **Parameters:**
  **diagram** ([`DiagramIR`](ij.core.md#ij.core.DiagramIR)) – The diagram to render
* **Return type:**
  [`str`](https://docs.python.org/3/builtins/stdtypes.html#str)
* **Returns:**
  DOT syntax as a string

#### render_to_file(diagram, filename)

Render diagram and save to file.

* **Parameters:**
  * **diagram** ([`DiagramIR`](ij.core.md#ij.core.DiagramIR)) – The diagram to render
  * **filename** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Path to output file
* **Return type:**
  [`None`](https://docs.python.org/3/builtins/constants.html#None)

#### render_to_image(diagram, filename, format='png')

Render diagram directly to image using graphviz library.

* **Parameters:**
  * **diagram** ([`DiagramIR`](ij.core.md#ij.core.DiagramIR)) – The diagram to render
  * **filename** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Path to output file (without extension)
  * **format** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Output format (png, svg, pdf, etc.)
* **Return type:**
  [`None`](https://docs.python.org/3/builtins/constants.html#None)

### *class* ij.HierarchicalLayout(direction='TB', layer_spacing=100, node_spacing=150)

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

Hierarchical layout using Sugiyama algorithm.

#### compute(diagram)

Compute node positions using hierarchical layout.

* **Parameters:**
  **diagram** ([`DiagramIR`](ij.core.md#ij.core.DiagramIR)) – DiagramIR to layout
* **Return type:**
  [`Dict`](https://docs.python.org/3/library/typing.html#typing.Dict)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str), [`Tuple`](https://docs.python.org/3/library/typing.html#typing.Tuple)[[`float`](https://docs.python.org/3/builtins/functions.html#float), [`float`](https://docs.python.org/3/builtins/functions.html#float)]]
* **Returns:**
  Dictionary mapping node IDs to (x, y) positions

### *class* ij.ImageExporter(format='svg', engine='mermaid-cli')

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

Export diagrams to image formats.

#### check_dependencies()

Check which rendering engines are available.

* **Return type:**
  [`dict`](https://docs.python.org/3/builtins/stdtypes.html#dict)
* **Returns:**
  Dictionary of engine availability

### Example

```pycon
>>> exporter = ImageExporter()
>>> available = exporter.check_dependencies()
>>> if available['graphviz']:
...     print("Graphviz is installed")
```

#### render(diagram, output_path, width=None, height=None, background='white', theme='default')

Render diagram to image file.

* **Parameters:**
  * **diagram** ([`DiagramIR`](ij.core.md#ij.core.DiagramIR)) – DiagramIR to render
  * **output_path** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Output file path
  * **width** ([`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`int`](https://docs.python.org/3/builtins/functions.html#int)]) – Image width in pixels (optional)
  * **height** ([`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`int`](https://docs.python.org/3/builtins/functions.html#int)]) – Image height in pixels (optional)
  * **background** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Background color
  * **theme** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Diagram theme (‘default’, ‘dark’, ‘forest’, ‘neutral’)
* **Return type:**
  [`bool`](https://docs.python.org/3/builtins/functions.html#bool)
* **Returns:**
  True if successful, False otherwise

### Example

```pycon
>>> exporter = ImageExporter(format='png', engine='mermaid-cli')
>>> success = exporter.render(diagram, 'output.png', width=800)
```

### *class* ij.InteractionAnalyzer

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

Analyze code or text to identify interaction patterns for sequence diagrams.

#### analyze_function_calls(caller, code)

Analyze function calls to create a sequence diagram.

* **Parameters:**
  * **caller** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – The calling function/component name
  * **code** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Python code to analyze
* **Return type:**
  [`DiagramIR`](ij.core.md#ij.core.DiagramIR)
* **Returns:**
  DiagramIR representing the call sequence

### Example

```pycon
>>> analyzer = InteractionAnalyzer()
>>> code = '''
... api.authenticate(user)
... db.query(user_id)
... cache.store(result)
... '''
>>> diagram = analyzer.analyze_function_calls("client", code)
```

#### from_text_description(text)

Create sequence diagram from text description.

* **Parameters:**
  **text** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Natural language description of interactions
* **Return type:**
  [`DiagramIR`](ij.core.md#ij.core.DiagramIR)
* **Returns:**
  DiagramIR representing the interaction sequence

### Example

```pycon
>>> analyzer = InteractionAnalyzer()
>>> text = "User sends request to API. API queries Database. Database returns data to API. API responds to User."
>>> diagram = analyzer.from_text_description(text)
```

### *class* ij.LLMConverter(api_key=None, model='gpt-4o-mini', temperature=0.3)

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

AI-powered text to diagram converter using LLMs.

Uses OpenAI API with carefully crafted prompts to generate diagrams
from natural language descriptions. Supports iterative refinement.

#### convert(text, title=None, direction='TD')

Convert natural language to DiagramIR using LLM.

* **Parameters:**
  * **text** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Natural language description
  * **title** ([`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]) – Optional diagram title
  * **direction** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Diagram direction (TD, LR, etc.)
* **Return type:**
  [`DiagramIR`](ij.core.md#ij.core.DiagramIR)
* **Returns:**
  DiagramIR representation

### Example

```pycon
>>> converter = LLMConverter()
>>> diagram = converter.convert(
...     "A user logs into the system. If authentication succeeds, "
...     "they see the dashboard. Otherwise, they see an error message."
... )
```

#### convert_with_examples(text, examples, title=None)

Convert with few-shot examples for better quality.

* **Parameters:**
  * **text** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Natural language description
  * **examples** ([`List`](https://docs.python.org/3/library/typing.html#typing.List)[[`Dict`](https://docs.python.org/3/library/typing.html#typing.Dict)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str), [`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]]) – List of {“description”: “…”, “mermaid”: “…”} examples
  * **title** ([`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]) – Optional diagram title
* **Return type:**
  [`DiagramIR`](ij.core.md#ij.core.DiagramIR)
* **Returns:**
  DiagramIR representation

#### refine(diagram, feedback, current_mermaid)

Refine an existing diagram based on feedback.

* **Parameters:**
  * **diagram** ([`DiagramIR`](ij.core.md#ij.core.DiagramIR)) – Current diagram
  * **feedback** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – User feedback/instructions
  * **current_mermaid** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Current Mermaid representation
* **Return type:**
  [`DiagramIR`](ij.core.md#ij.core.DiagramIR)
* **Returns:**
  Refined DiagramIR

### Example

```pycon
>>> diagram = converter.convert("User login process")
>>> from ij.renderers import MermaidRenderer
>>> mermaid = MermaidRenderer().render(diagram)
>>> refined = converter.refine(
...     diagram,
...     "Add a step for password reset if login fails",
...     mermaid
... )
```

### *class* ij.LayoutEngine(algorithm='hierarchical', \*\*kwargs)

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

Apply layout algorithms to diagrams.

#### apply(diagram)

Apply layout algorithm to diagram.

* **Parameters:**
  **diagram** ([`DiagramIR`](ij.core.md#ij.core.DiagramIR)) – DiagramIR to layout
* **Return type:**
  [`Dict`](https://docs.python.org/3/library/typing.html#typing.Dict)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str), [`Tuple`](https://docs.python.org/3/library/typing.html#typing.Tuple)[[`float`](https://docs.python.org/3/builtins/functions.html#float), [`float`](https://docs.python.org/3/builtins/functions.html#float)]]
* **Returns:**
  Dictionary mapping node IDs to (x, y) positions

### Example

```pycon
>>> engine = LayoutEngine(algorithm='force-directed')
>>> positions = engine.apply(diagram)
>>> print(positions['node1'])  # (x, y)
(150.0, 200.0)
```

### *exception* ij.MermaidParseWarning

Bases: [`UserWarning`](https://docs.python.org/3/builtins/exceptions.html#UserWarning)

Warns that a Mermaid line could not be interpreted and was skipped.

### *class* ij.MermaidParser(, strict=False)

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

Parses Mermaid flowchart syntax to DiagramIR.

Supports basic flowchart syntax including:

- Node definitions with various shapes, standalone or inline on an edge line
- Edge connections with labels, including chained edges
- Title metadata

A line matching none of the above is reported instead of being dropped:
see `unparsed_lines` and the `strict` argument.

#### strict

Whether an unparseable line raises instead of warning

#### nodes

Nodes found by the last parse, keyed by node id

#### edges

Edges found by the last parse

#### metadata

Diagram-level metadata (title, direction) from the last parse

#### unparsed_lines

Lines the last parse could not interpret

#### parse(mermaid_text)

Parse Mermaid syntax to DiagramIR.

* **Parameters:**
  **mermaid_text** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Mermaid flowchart syntax
* **Return type:**
  [`DiagramIR`](ij.core.md#ij.core.DiagramIR)
* **Returns:**
  DiagramIR representation
* **Raises:**
  [**ValueError**](https://docs.python.org/3/builtins/exceptions.html#ValueError) – If `strict` is set and a line cannot be parsed

### Example

```pycon
>>> parser = MermaidParser()
>>> diagram = parser.parse('''flowchart TD
...     start([Start]) --> check{Ok?}
...     check --|Yes|--> done([Done])''')
```

```pycon
>>> [(node.id, node.node_type.value) for node in diagram.nodes]
[('start', 'start'), ('check', 'decision'), ('done', 'end')]
>>> [(edge.source, edge.target, edge.label) for edge in diagram.edges]
[('start', 'check', None), ('check', 'done', 'Yes')]
```

#### parse_file(filename)

Parse Mermaid file to DiagramIR.

* **Parameters:**
  **filename** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Path to Mermaid file
* **Return type:**
  [`DiagramIR`](ij.core.md#ij.core.DiagramIR)
* **Returns:**
  DiagramIR representation

### *class* ij.MermaidRenderer(direction='TD')

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

Renders DiagramIR to Mermaid syntax.

Supports flowchart diagrams with various node shapes and edge types.

#### render(diagram)

Render a DiagramIR to Mermaid syntax.

* **Parameters:**
  **diagram** ([`DiagramIR`](ij.core.md#ij.core.DiagramIR)) – The diagram to render
* **Return type:**
  [`str`](https://docs.python.org/3/builtins/stdtypes.html#str)
* **Returns:**
  Mermaid syntax as a string

#### render_to_file(diagram, filename)

Render diagram and save to file.

* **Parameters:**
  * **diagram** ([`DiagramIR`](ij.core.md#ij.core.DiagramIR)) – The diagram to render
  * **filename** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Path to output file
* **Return type:**
  [`None`](https://docs.python.org/3/builtins/constants.html#None)

### *class* ij.Node(id, label, node_type=NodeType.PROCESS, metadata=<factory>)

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

Represents a node in the diagram IR.

#### id

Unique identifier for the node

#### label

Display label/text

#### node_type

Type of node (process, decision, etc.)

#### metadata

Additional properties for extensibility

### *class* ij.NodeType(\*values)

Bases: [`Enum`](https://docs.python.org/3/library/enum.html#enum.Enum)

Types of nodes in a diagram.

### *class* ij.PlantUMLRenderer(use_skinparam=True)

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

Renders DiagramIR to PlantUML activity diagram syntax.

PlantUML is the enterprise standard for comprehensive UML diagrams
with support for 25+ diagram types.

#### render(diagram)

Render a DiagramIR to PlantUML syntax.

* **Parameters:**
  **diagram** ([`DiagramIR`](ij.core.md#ij.core.DiagramIR)) – The diagram to render
* **Return type:**
  [`str`](https://docs.python.org/3/builtins/stdtypes.html#str)
* **Returns:**
  PlantUML syntax as a string

#### render_to_file(diagram, filename)

Render diagram and save to file.

* **Parameters:**
  * **diagram** ([`DiagramIR`](ij.core.md#ij.core.DiagramIR)) – The diagram to render
  * **filename** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Path to output file
* **Return type:**
  [`None`](https://docs.python.org/3/builtins/constants.html#None)

### *class* ij.PluginManager

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

Manage and execute plugins.

#### apply_transform(transform_name, diagram, \*\*kwargs)

Apply a registered transform.

* **Parameters:**
  * **transform_name** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Name of transform
  * **diagram** ([`DiagramIR`](ij.core.md#ij.core.DiagramIR)) – DiagramIR to transform
  * **\*\*kwargs** – Transform arguments
* **Return type:**
  [`DiagramIR`](ij.core.md#ij.core.DiagramIR)
* **Returns:**
  Transformed DiagramIR

#### execute_plugin(plugin_name, diagram, \*\*kwargs)

Execute a plugin on a diagram.

* **Parameters:**
  * **plugin_name** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Name of plugin to execute
  * **diagram** ([`DiagramIR`](ij.core.md#ij.core.DiagramIR)) – DiagramIR to process
  * **\*\*kwargs** – Plugin-specific arguments
* **Return type:**
  [`DiagramIR`](ij.core.md#ij.core.DiagramIR)
* **Returns:**
  Transformed DiagramIR

#### list_plugins()

List all registered plugins.

* **Return type:**
  [`List`](https://docs.python.org/3/library/typing.html#typing.List)[[`Dict`](https://docs.python.org/3/library/typing.html#typing.Dict)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str), [`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]]
* **Returns:**
  List of plugin information dictionaries

#### list_transforms()

List all registered transforms.

* **Return type:**
  [`List`](https://docs.python.org/3/library/typing.html#typing.List)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]

#### load_plugin_file(file_path)

Load plugin from a Python file.

* **Parameters:**
  **file_path** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Path to plugin file

### Example

```pycon
>>> manager.load_plugin_file('plugins/my_plugin.py')
```

#### load_plugins_directory(directory)

Load all plugins from a directory.

* **Parameters:**
  **directory** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Directory containing plugin files

### Example

```pycon
>>> manager.load_plugins_directory('~/.ij/plugins')
```

#### register_hook(event, func)

Register a hook for an event.

* **Parameters:**
  * **event** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Event name (‘pre_render’, ‘post_parse’, etc.)
  * **func** ([`Callable`](https://docs.python.org/3/library/typing.html#typing.Callable)) – Hook function

### Example

```pycon
>>> def on_render(diagram):
...     print(f"Rendering {len(diagram.nodes)} nodes")
>>> manager.register_hook('pre_render', on_render)
```

#### register_plugin(plugin)

Register a plugin.

* **Parameters:**
  **plugin** ([`Plugin`](ij.plugins.plugin_manager.md#ij.plugins.plugin_manager.Plugin)) – Plugin instance to register

### Example

```pycon
>>> class MyPlugin(Plugin):
...     name = "my_plugin"
...     def process(self, diagram, **kwargs):
...         # Transform diagram
...         return diagram
>>> manager = PluginManager()
>>> manager.register_plugin(MyPlugin())
```

#### register_transform(name, func)

Register a transform function.

* **Parameters:**
  * **name** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Transform name
  * **func** ([`Callable`](https://docs.python.org/3/library/typing.html#typing.Callable)) – Transform function (diagram, \*\*kwargs) -> diagram

### Example

```pycon
>>> def highlight_critical(diagram, start, end):
...     # Highlight path from start to end
...     return diagram
>>> manager.register_transform('highlight-critical', highlight_critical)
```

#### trigger_hooks(event, \*args, \*\*kwargs)

Trigger all hooks for an event.

* **Parameters:**
  * **event** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Event name
  * **\*args** – Event arguments
  * **\*\*kwargs** – Event keyword arguments

### *class* ij.PythonCodeAnalyzer

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

Analyze Python code to generate diagrams.

Supports:

- Function call graphs
- Control flow diagrams
- Class relationship diagrams

#### analyze_class(code, class_name=None)

Analyze a Python class to create a class diagram.

* **Parameters:**
  * **code** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Python source code
  * **class_name** ([`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]) – Specific class to analyze (None = first class)
* **Return type:**
  [`DiagramIR`](ij.core.md#ij.core.DiagramIR)
* **Returns:**
  DiagramIR representation of the class structure

#### analyze_function(code, function_name=None)

Analyze a Python function to create a flowchart.

* **Parameters:**
  * **code** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Python source code
  * **function_name** ([`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]) – Specific function to analyze (None = first function)
* **Return type:**
  [`DiagramIR`](ij.core.md#ij.core.DiagramIR)
* **Returns:**
  DiagramIR representation of the function’s control flow

### Example

```pycon
>>> code = '''
... def process_order(order):
...     if order.is_valid():
...         save_to_database(order)
...         send_confirmation(order)
...     else:
...         send_error_notification(order)
... '''
>>> analyzer = PythonCodeAnalyzer()
>>> diagram = analyzer.analyze_function(code)
```

#### analyze_module_calls(code)

Analyze function calls in a module to create a call graph.

* **Parameters:**
  **code** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Python source code
* **Return type:**
  [`DiagramIR`](ij.core.md#ij.core.DiagramIR)
* **Returns:**
  DiagramIR representation of function call relationships

### *class* ij.SequenceDiagramRenderer

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

Render DiagramIR as Mermaid sequence diagram.

Maps DiagramIR concepts to sequence diagrams:

- Nodes -> Participants
- Edges -> Messages between participants
- Edge labels -> Message content
- EdgeType.DIRECT -> Solid arrows (synchronous)
- EdgeType.CONDITIONAL -> Dashed arrows (asynchronous/return)
- EdgeType.BIDIRECTIONAL -> Bidirectional arrows

#### render(diagram)

Render DiagramIR as Mermaid sequence diagram.

* **Parameters:**
  **diagram** ([`DiagramIR`](ij.core.md#ij.core.DiagramIR)) – DiagramIR to render
* **Return type:**
  [`str`](https://docs.python.org/3/builtins/stdtypes.html#str)
* **Returns:**
  Mermaid sequence diagram syntax

### Example

```pycon
>>> from ij import DiagramIR, Node, Edge
>>> diagram = DiagramIR()
>>> diagram.add_node(Node(id="user", label="User"))
>>> diagram.add_node(Node(id="api", label="API"))
>>> diagram.add_edge(Edge(source="user", target="api", label="Request"))
>>> renderer = SequenceDiagramRenderer()
>>> print(renderer.render(diagram))
sequenceDiagram
    participant user as User
    participant api as API
    user->>api: Request
```

#### render_with_activations(diagram, activations)

Render sequence diagram with participant activations.

* **Parameters:**
  * **diagram** ([`DiagramIR`](ij.core.md#ij.core.DiagramIR)) – DiagramIR to render
  * **activations** ([`List`](https://docs.python.org/3/library/typing.html#typing.List)[[`tuple`](https://docs.python.org/3/builtins/stdtypes.html#tuple)]) – List of (participant_id, “activate”/”deactivate”) tuples
* **Return type:**
  [`str`](https://docs.python.org/3/builtins/stdtypes.html#str)
* **Returns:**
  Mermaid sequence diagram with activations

### Example

```pycon
>>> activations = [("api", "activate"), ("api", "deactivate")]
>>> renderer.render_with_activations(diagram, activations)
```

#### render_with_notes(diagram, notes)

Render sequence diagram with notes.

* **Parameters:**
  * **diagram** ([`DiagramIR`](ij.core.md#ij.core.DiagramIR)) – DiagramIR to render
  * **notes** ([`Dict`](https://docs.python.org/3/library/typing.html#typing.Dict)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str), [`List`](https://docs.python.org/3/library/typing.html#typing.List)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]]) – Dict mapping participant IDs to list of notes
* **Return type:**
  [`str`](https://docs.python.org/3/builtins/stdtypes.html#str)
* **Returns:**
  Mermaid sequence diagram with notes

### Example

```pycon
>>> notes = {"user": ["Note about user"], "api": ["API note"]}
>>> renderer.render_with_notes(diagram, notes)
```

### *class* ij.SimpleTextConverter

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

Simple rule-based text to diagram converter.

Parses structured text like:

- “Start -> Process A -> Decision B”
- “If condition: Process C, else: Process D”

#### convert(text, title=None)

Convert structured text to DiagramIR.

* **Parameters:**
  * **text** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Input text describing a process/flow
  * **title** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Optional diagram title
* **Return type:**
  [`DiagramIR`](ij.core.md#ij.core.DiagramIR)
* **Returns:**
  DiagramIR representation

### *class* ij.State(name, state_type=StateType.NORMAL, on_enter=None, on_exit=None, metadata=<factory>)

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

A state in a state machine.

### *class* ij.StateMachine(name='StateMachine', initial_state=None)

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

Finite State Machine diagram.

#### add_state(name, state_type=StateType.NORMAL, on_enter=None, on_exit=None)

Add a state to the machine.

* **Parameters:**
  * **name** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – State name
  * **state_type** ([`StateType`](ij.diagrams.state_machine.md#ij.diagrams.state_machine.StateType)) – Type of state (NORMAL, INITIAL, FINAL)
  * **on_enter** ([`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]) – Action to perform on entering state
  * **on_exit** ([`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]) – Action to perform on exiting state

#### add_transition(from_state, trigger, to_state, condition=None, action=None)

Add a transition between states.

* **Parameters:**
  * **from_state** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Source state name
  * **trigger** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Event that triggers the transition
  * **to_state** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Target state name
  * **condition** ([`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]) – Optional condition guard
  * **action** ([`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]) – Optional action to perform during transition

#### get_triggers_from_state(state_name)

Get all possible triggers from a given state.

* **Parameters:**
  **state_name** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – State name
* **Return type:**
  [`List`](https://docs.python.org/3/library/typing.html#typing.List)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]
* **Returns:**
  List of trigger names

#### simulate(initial_state, events)

Simulate state machine execution.

* **Parameters:**
  * **initial_state** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Starting state
  * **events** ([`List`](https://docs.python.org/3/library/typing.html#typing.List)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]) – List of trigger events
* **Return type:**
  [`List`](https://docs.python.org/3/library/typing.html#typing.List)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]
* **Returns:**
  List of states visited (including initial)

#### to_d2()

Render state machine as D2 diagram.

* **Return type:**
  [`str`](https://docs.python.org/3/builtins/stdtypes.html#str)
* **Returns:**
  D2 syntax

#### to_mermaid()

Render state machine as Mermaid state diagram.

* **Return type:**
  [`str`](https://docs.python.org/3/builtins/stdtypes.html#str)
* **Returns:**
  Mermaid state diagram syntax

#### to_plantuml()

Render state machine as PlantUML state diagram.

* **Return type:**
  [`str`](https://docs.python.org/3/builtins/stdtypes.html#str)
* **Returns:**
  PlantUML syntax

#### validate()

Validate state machine for common issues.

* **Return type:**
  [`List`](https://docs.python.org/3/library/typing.html#typing.List)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]
* **Returns:**
  List of validation issues (empty if valid)

### *class* ij.TypeScriptAnalyzer

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

Analyze TypeScript/JavaScript code to create diagrams.

#### analyze_async_flow(code)

Analyze async/await flow in TypeScript/JavaScript.

* **Parameters:**
  **code** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Code with async operations
* **Return type:**
  [`DiagramIR`](ij.core.md#ij.core.DiagramIR)
* **Returns:**
  DiagramIR showing async flow

### Example

```pycon
>>> code = '''
... async function fetchData() {
...   const response = await fetch('/api');
...   const data = await response.json();
...   return data;
... }
... '''
>>> diagram = analyzer.analyze_async_flow(code)
```

#### analyze_function(code, function_name=None)

Analyze TypeScript/JavaScript function to create flowchart.

* **Parameters:**
  * **code** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – TypeScript/JavaScript code
  * **function_name** ([`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]) – Specific function to analyze (or first if None)
* **Return type:**
  [`DiagramIR`](ij.core.md#ij.core.DiagramIR)
* **Returns:**
  DiagramIR representing function flow

### Example

```pycon
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
```

#### analyze_module_imports(code)

Analyze TypeScript module imports/exports.

* **Parameters:**
  **code** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – TypeScript/JavaScript code
* **Return type:**
  [`DiagramIR`](ij.core.md#ij.core.DiagramIR)
* **Returns:**
  DiagramIR showing module dependencies

### Example

```pycon
>>> code = '''
... import { Component } from './components';
... import axios from 'axios';
... export default App;
... '''
>>> diagram = analyzer.analyze_module_imports(code)
```

#### analyze_react_component(code, component_name)

Analyze React component to show component hierarchy.

* **Parameters:**
  * **code** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – React component code
  * **component_name** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Name of the component
* **Return type:**
  [`DiagramIR`](ij.core.md#ij.core.DiagramIR)
* **Returns:**
  DiagramIR showing component structure

### Example

```pycon
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
```

### *class* ij.ValidationResult(is_valid, issues)

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

Result of diagram validation.

#### *property* errors *: [List](https://docs.python.org/3/library/typing.html#typing.List)[[ValidationIssue](ij.validation.md#ij.validation.ValidationIssue)]*

Get only error-level issues.

#### *property* warnings *: [List](https://docs.python.org/3/library/typing.html#typing.List)[[ValidationIssue](ij.validation.md#ij.validation.ValidationIssue)]*

Get only warning-level issues.

### *class* ij.ViewerServer(port=8080, theme='default')

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

Interactive web server for diagram viewing.

#### start(diagram, open_browser=True)

Start the viewer server.

* **Parameters:**
  * **diagram** ([`DiagramIR`](ij.core.md#ij.core.DiagramIR)) – DiagramIR to display
  * **open_browser** ([`bool`](https://docs.python.org/3/builtins/functions.html#bool)) – Whether to open browser automatically

### Example

```pycon
>>> server = ViewerServer(port=8080)
>>> server.start(diagram)
Server running at http://localhost:8080
Press Ctrl+C to stop
```

#### stop()

Stop the server.

#### update_diagram(diagram)

Update the displayed diagram.

* **Parameters:**
  **diagram** ([`DiagramIR`](ij.core.md#ij.core.DiagramIR)) – New DiagramIR to display

### ij.analyze_package_json(file_path)

Analyze package.json to show dependency graph.

* **Parameters:**
  **file_path** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Path to package.json
* **Return type:**
  [`DiagramIR`](ij.core.md#ij.core.DiagramIR)
* **Returns:**
  DiagramIR showing dependencies

### Example

```pycon
>>> diagram = analyze_package_json('package.json')
```

### ij.quick_export(diagram, output_path, format='svg', engine=None)

Quick export diagram to image.

* **Parameters:**
  * **diagram** ([`DiagramIR`](ij.core.md#ij.core.DiagramIR)) – DiagramIR to export
  * **output_path** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Output file path
  * **format** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Image format (‘svg’, ‘png’, ‘pdf’)
  * **engine** ([`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]) – Rendering engine (auto-detected if None)
* **Return type:**
  [`bool`](https://docs.python.org/3/builtins/functions.html#bool)
* **Returns:**
  True if successful

### Example

```pycon
>>> from ij import DiagramIR, Node, Edge
>>> diagram = DiagramIR()
>>> # ... build diagram ...
>>> quick_export(diagram, 'diagram.png', format='png')
```

### ij.register_plugin(plugin)

Register plugin with global manager.

### ij.register_transform(name)

Decorator to register a transform function.

### Example

```pycon
>>> @register_transform('my-transform')
... def my_transform(diagram, **kwargs):
...     return diagram
```

### ij.serve_diagram(diagram, port=8080, theme='default', open_browser=True)

Quickly serve a diagram in browser.

* **Parameters:**
  * **diagram** ([`DiagramIR`](ij.core.md#ij.core.DiagramIR)) – DiagramIR to display
  * **port** ([`int`](https://docs.python.org/3/builtins/functions.html#int)) – Port number
  * **theme** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Mermaid theme
  * **open_browser** ([`bool`](https://docs.python.org/3/builtins/functions.html#bool)) – Whether to open browser

### Example

```pycon
>>> from ij import DiagramIR, Node, Edge
>>> diagram = DiagramIR()
>>> # ... build diagram ...
>>> serve_diagram(diagram)
```

### ij.text_to_mermaid(text, title=None, direction='TD')

Convert text description to Mermaid diagram (convenience function).

* **Parameters:**
  * **text** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Text description of the process/flow
  * **title** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Optional diagram title
  * **direction** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Flow direction (TD, LR, etc.)
* **Return type:**
  [`str`](https://docs.python.org/3/builtins/stdtypes.html#str)
* **Returns:**
  Mermaid syntax string

### Example

```pycon
>>> mermaid = text_to_mermaid("Start -> Process data -> End")
>>> print(mermaid)
flowchart TD
    n0([Start])
    n1[Process data]
    n2([End])
    n0 --> n1
    n1 --> n2
```

### Modules

| [`importers`](ij.importers.md#module-ij.importers)             | Import diagrams from external sources.                     |
|--------------------------------------------------------------------------------------------|------------------------------------------------------------|
| [`analyzers`](ij.analyzers.md#module-ij.analyzers)             | Code analyzers for reverse engineering diagrams from code. |
| [`cli`](ij.cli.md#module-ij.cli)                         | Command-line interface for Idea Junction.                  |
| [`cli_enhanced`](ij.cli_enhanced.md#module-ij.cli_enhanced)       | Enhanced command-line interface for Idea Junction.         |
| [`converters`](ij.converters.md#module-ij.converters)           | Converters between different representations.              |
| [`core`](ij.core.md#module-ij.core)                       | Core data structures for Idea Junction.                    |
| [`diagrams`](ij.diagrams.md#module-ij.diagrams)               | Advanced diagram types.                                    |
| [`export`](ij.export.md#module-ij.export)                   | Export functionality.                                      |
| [`git_integration`](ij.git_integration.md#module-ij.git_integration) | Git integration for diagram version control and diffing.   |
| [`graph_ops`](ij.graph_ops.md#module-ij.graph_ops)             | Graph operations using NetworkX.                           |
| [`layout`](ij.layout.md#module-ij.layout)                   | Layout algorithms for diagram positioning.                 |
| [`parsers`](ij.parsers.md#module-ij.parsers)                 | Diagram parsers for various formats.                       |
| [`plugins`](ij.plugins.md#module-ij.plugins)                 | Plugin system for extensibility.                           |
| [`renderers`](ij.renderers.md#module-ij.renderers)             | Diagram renderers for various formats.                     |
| [`transforms`](ij.transforms.md#module-ij.transforms)           | Diagram transformation and optimization utilities.         |
| [`validation`](ij.validation.md#module-ij.validation)           | Diagram validation and linting.                            |
| [`viewer`](ij.viewer.md#module-ij.viewer)                   | Interactive web viewer for diagrams.                       |
