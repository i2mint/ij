# ij.graph_ops

Graph operations using NetworkX.

Provides graph manipulation, analysis, and transformation capabilities
following the research recommendation to use NetworkX as the foundation
for graph-based operations.

### Classes

| [`GraphOperations`](#ij.graph_ops.GraphOperations)()   | Graph manipulation and analysis using NetworkX.   |
|----------------------------------------------------------------------|---------------------------------------------------|

### *class* ij.graph_ops.GraphOperations

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
