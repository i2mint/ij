# ij.transforms

Diagram transformation and optimization utilities.

Provides operations for manipulating, simplifying, and optimizing diagrams.

### Classes

| [`DiagramTransforms`](#ij.transforms.DiagramTransforms)()   | Transform and optimize diagram structures.   |
|------------------------------------------------------------------------|----------------------------------------------|

### *class* ij.transforms.DiagramTransforms

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

Transform and optimize diagram structures.

#### *static* apply_node_filter(diagram, predicate)

Filter nodes using a custom predicate function.

* **Parameters:**
  * **diagram** ([`DiagramIR`](ij.core.html.md#ij.core.DiagramIR)) – DiagramIR to filter
  * **predicate** ([`Callable`](https://docs.python.org/3/library/typing.html#typing.Callable)[[[`Node`](ij.core.html.md#ij.core.Node)], [`bool`](https://docs.python.org/3/builtins/functions.html#bool)]) – Function that returns True for nodes to keep
* **Return type:**
  [`DiagramIR`](ij.core.html.md#ij.core.DiagramIR)
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
  * **diagram** ([`DiagramIR`](ij.core.html.md#ij.core.DiagramIR)) – Source DiagramIR
  * **root_node_id** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – ID of root node
  * **max_depth** ([`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`int`](https://docs.python.org/3/builtins/functions.html#int)]) – Maximum depth to traverse (None = unlimited)
* **Return type:**
  [`DiagramIR`](ij.core.html.md#ij.core.DiagramIR)
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
  * **diagram** ([`DiagramIR`](ij.core.html.md#ij.core.DiagramIR)) – DiagramIR to filter
  * **node_types** ([`List`](https://docs.python.org/3/library/typing.html#typing.List)[[`NodeType`](ij.core.html.md#ij.core.NodeType)]) – List of NodeTypes to filter
  * **keep** ([`bool`](https://docs.python.org/3/builtins/functions.html#bool)) – If True, keep only these types; if False, remove these types
* **Return type:**
  [`DiagramIR`](ij.core.html.md#ij.core.DiagramIR)
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
  **diagram** ([`DiagramIR`](ij.core.html.md#ij.core.DiagramIR)) – DiagramIR to analyze
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
  **diagram** ([`DiagramIR`](ij.core.html.md#ij.core.DiagramIR)) – DiagramIR to analyze
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
  * **diagrams** ([`List`](https://docs.python.org/3/library/typing.html#typing.List)[[`DiagramIR`](ij.core.html.md#ij.core.DiagramIR)]) – List of DiagramIR to merge
  * **title** ([`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]) – Optional title for merged diagram
* **Return type:**
  [`DiagramIR`](ij.core.html.md#ij.core.DiagramIR)
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
  * **diagram** ([`DiagramIR`](ij.core.html.md#ij.core.DiagramIR)) – DiagramIR to transform
  * **separator** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – String to join labels
* **Return type:**
  [`DiagramIR`](ij.core.html.md#ij.core.DiagramIR)
* **Returns:**
  DiagramIR with merged nodes

#### *static* reverse_edges(diagram)

Reverse all edge directions in the diagram.

* **Parameters:**
  **diagram** ([`DiagramIR`](ij.core.html.md#ij.core.DiagramIR)) – DiagramIR to reverse
* **Return type:**
  [`DiagramIR`](ij.core.html.md#ij.core.DiagramIR)
* **Returns:**
  DiagramIR with reversed edges

### Example

```pycon
>>> reversed_diagram = DiagramTransforms.reverse_edges(diagram)
```

#### *static* simplify(diagram, remove_isolated=True)

Simplify diagram by removing redundant nodes and edges.

* **Parameters:**
  * **diagram** ([`DiagramIR`](ij.core.html.md#ij.core.DiagramIR)) – DiagramIR to simplify
  * **remove_isolated** ([`bool`](https://docs.python.org/3/builtins/functions.html#bool)) – Remove nodes with no connections
* **Return type:**
  [`DiagramIR`](ij.core.html.md#ij.core.DiagramIR)
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
>>> len(simplified.nodes)  # isolated node removed
2
```
