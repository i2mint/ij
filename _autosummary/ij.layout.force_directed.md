# ij.layout.force_directed

Force-directed graph layout algorithm.

### Classes

| [`ForceDirectedLayout`](#ij.layout.force_directed.ForceDirectedLayout)([iterations, ...])   | Force-directed layout using Fruchterman-Reingold algorithm.   |
|-------------------------------------------------------------------------------------------|---------------------------------------------------------------|

### *class* ij.layout.force_directed.ForceDirectedLayout(iterations=100, optimal_distance=100, repulsion_strength=5000, attraction_strength=0.1, cooling_factor=0.95)

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
