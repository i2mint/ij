# ij.layout.hierarchical

Hierarchical (layered) graph layout algorithm.

### Classes

| [`HierarchicalLayout`](#ij.layout.hierarchical.HierarchicalLayout)([direction, ...])   | Hierarchical layout using Sugiyama algorithm.   |
|-----------------------------------------------------------------------------------------|-------------------------------------------------|

### *class* ij.layout.hierarchical.HierarchicalLayout(direction='TB', layer_spacing=100, node_spacing=150)

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
