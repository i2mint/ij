# ij.layout

Layout algorithms for diagram positioning.

### Classes

| [`LayoutEngine`](#ij.layout.LayoutEngine)([algorithm])              | Apply layout algorithms to diagrams.                        |
|-----------------------------------------------------------------------------------------|-------------------------------------------------------------|
| [`ForceDirectedLayout`](#ij.layout.ForceDirectedLayout)([iterations, ...]) | Force-directed layout using Fruchterman-Reingold algorithm. |
| [`HierarchicalLayout`](#ij.layout.HierarchicalLayout)([direction, ...])   | Hierarchical layout using Sugiyama algorithm.               |

### *class* ij.layout.ForceDirectedLayout(iterations=100, optimal_distance=100, repulsion_strength=5000, attraction_strength=0.1, cooling_factor=0.95)

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

Force-directed layout using Fruchterman-Reingold algorithm.

#### compute(diagram)

Compute node positions using force-directed layout.

* **Parameters:**
  **diagram** ([`DiagramIR`](ij.core.html.md#ij.core.DiagramIR)) – DiagramIR to layout
* **Return type:**
  [`Dict`](https://docs.python.org/3/library/typing.html#typing.Dict)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str), [`Tuple`](https://docs.python.org/3/library/typing.html#typing.Tuple)[[`float`](https://docs.python.org/3/builtins/functions.html#float), [`float`](https://docs.python.org/3/builtins/functions.html#float)]]
* **Returns:**
  Dictionary mapping node IDs to (x, y) positions

### *class* ij.layout.HierarchicalLayout(direction='TB', layer_spacing=100, node_spacing=150)

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

Hierarchical layout using Sugiyama algorithm.

#### compute(diagram)

Compute node positions using hierarchical layout.

* **Parameters:**
  **diagram** ([`DiagramIR`](ij.core.html.md#ij.core.DiagramIR)) – DiagramIR to layout
* **Return type:**
  [`Dict`](https://docs.python.org/3/library/typing.html#typing.Dict)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str), [`Tuple`](https://docs.python.org/3/library/typing.html#typing.Tuple)[[`float`](https://docs.python.org/3/builtins/functions.html#float), [`float`](https://docs.python.org/3/builtins/functions.html#float)]]
* **Returns:**
  Dictionary mapping node IDs to (x, y) positions

### *class* ij.layout.LayoutEngine(algorithm='hierarchical', \*\*kwargs)

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

Apply layout algorithms to diagrams.

#### apply(diagram)

Apply layout algorithm to diagram.

* **Parameters:**
  **diagram** ([`DiagramIR`](ij.core.html.md#ij.core.DiagramIR)) – DiagramIR to layout
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

### Modules

| [`force_directed`](ij.layout.force_directed.html.md#module-ij.layout.force_directed)   | Force-directed graph layout algorithm.         |
|---------------------------------------------------------------------------------------------------|------------------------------------------------|
| [`hierarchical`](ij.layout.hierarchical.html.md#module-ij.layout.hierarchical)       | Hierarchical (layered) graph layout algorithm. |
| [`layout_engine`](ij.layout.layout_engine.html.md#module-ij.layout.layout_engine)     | Layout engine for positioning diagram nodes.   |
