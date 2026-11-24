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

### *class* ij.core.DiagramIR(nodes=list(), edges=list(), metadata=dict())

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

Intermediate Representation for diagrams.

This serves as the central data structure that can be:

- Generated from natural language
- Converted to various diagram formats (Mermaid, PlantUML, D2)
- Manipulated programmatically
- Parsed back from diagram syntax

#### nodes

List of nodes in the diagram

* **Type:**
  [`List`](https://docs.python.org/3/library/typing.html#typing.List)[[`Node`](#ij.core.Node)]

#### edges

List of edges connecting nodes

* **Type:**
  [`List`](https://docs.python.org/3/library/typing.html#typing.List)[[`Edge`](#ij.core.Edge)]

#### metadata

Diagram-level properties (title, description, etc.)

* **Type:**
  [`Dict`](https://docs.python.org/3/library/typing.html#typing.Dict)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str), [`Any`](https://docs.python.org/3/library/typing.html#typing.Any)]

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

### *class* ij.core.Edge(source, target, label=None, edge_type=EdgeType.DIRECT, metadata=dict())

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

Represents an edge in the diagram IR.

#### source

Source node ID

* **Type:**
  [`str`](https://docs.python.org/3/builtins/stdtypes.html#str)

#### target

Target node ID

* **Type:**
  [`str`](https://docs.python.org/3/builtins/stdtypes.html#str)

#### label

Optional edge label

* **Type:**
  [`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]

#### edge_type

Type of edge

* **Type:**
  [`EdgeType`](#ij.core.EdgeType)

#### metadata

Additional properties for extensibility

* **Type:**
  [`Dict`](https://docs.python.org/3/library/typing.html#typing.Dict)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str), [`Any`](https://docs.python.org/3/library/typing.html#typing.Any)]

### *class* ij.core.EdgeType(\*values)

Bases: [`Enum`](https://docs.python.org/3/library/enum.html#enum.Enum)

Types of edges connecting nodes.

#### UNDIRECTED *= 'undirected'*

one edge,
never two opposite ones; `source`/`target` keep the written order.

* **Type:**
  A link with no direction (Mermaid’s open link `a --- b`)

### *class* ij.core.Node(id, label, node_type=NodeType.PROCESS, metadata=dict())

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

Represents a node in the diagram IR.

#### id

Unique identifier for the node

* **Type:**
  [`str`](https://docs.python.org/3/builtins/stdtypes.html#str)

#### label

Display label/text

* **Type:**
  [`str`](https://docs.python.org/3/builtins/stdtypes.html#str)

#### node_type

Type of node (process, decision, etc.)

* **Type:**
  [`NodeType`](#ij.core.NodeType)

#### metadata

Additional properties for extensibility

* **Type:**
  [`Dict`](https://docs.python.org/3/library/typing.html#typing.Dict)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str), [`Any`](https://docs.python.org/3/library/typing.html#typing.Any)]

### *class* ij.core.NodeType(\*values)

Bases: [`Enum`](https://docs.python.org/3/library/enum.html#enum.Enum)

Types of nodes in a diagram.
