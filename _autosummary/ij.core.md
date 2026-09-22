# ij.core

Core data structures for Idea Junction.

This module provides the intermediate representation (IR) for diagrams,
following the recommendation from research to use AST-like structures
for bidirectional conversion between text, diagrams, and code.

### Classes

| [`DiagramIR`](#ij.core.DiagramIR)([nodes, edges, metadata])           | Intermediate Representation for diagrams.   |
|------------------------------------------------------------------------------------------------|---------------------------------------------|
| [`Edge`](#ij.core.Edge)(source, target[, label, edge_type, ...]) | Represents an edge in the diagram IR.       |
| [`EdgeType`](#ij.core.EdgeType)(\*values)                            | Types of edges connecting nodes.            |
| [`Node`](#ij.core.Node)(id, label[, node_type, metadata])        | Represents a node in the diagram IR.        |
| [`NodeType`](#ij.core.NodeType)(\*values)                            | Types of nodes in a diagram.                |

### *class* ij.core.DiagramIR(nodes=<factory>, edges=<factory>, metadata=<factory>)

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
  [`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`Node`](#ij.core.Node)]

#### validate()

Validate the diagram structure.

* **Return type:**
  [`bool`](https://docs.python.org/3/builtins/functions.html#bool)
* **Returns:**
  True if the diagram is valid, False otherwise

### *class* ij.core.Edge(source, target, label=None, edge_type=EdgeType.DIRECT, metadata=<factory>)

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

### *class* ij.core.EdgeType(\*values)

Bases: [`Enum`](https://docs.python.org/3/library/enum.html#enum.Enum)

Types of edges connecting nodes.

### *class* ij.core.Node(id, label, node_type=NodeType.PROCESS, metadata=<factory>)

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

### *class* ij.core.NodeType(\*values)

Bases: [`Enum`](https://docs.python.org/3/library/enum.html#enum.Enum)

Types of nodes in a diagram.
