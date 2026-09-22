# ij.layout.layout_engine

Layout engine for positioning diagram nodes.

### Classes

| [`LayoutEngine`](#ij.layout.layout_engine.LayoutEngine)([algorithm])   | Apply layout algorithms to diagrams.   |
|------------------------------------------------------------------------------|----------------------------------------|

### *class* ij.layout.layout_engine.LayoutEngine(algorithm='hierarchical', \*\*kwargs)

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
