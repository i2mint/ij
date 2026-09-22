# ij.renderers.d2

D2 diagram renderer.

Converts DiagramIR to D2 (Terrastruct) syntax, a modern diagram-as-code
language with excellent aesthetics and bidirectional editing support.

### Classes

| [`D2Renderer`](#ij.renderers.d2.D2Renderer)([layout])   | Renders DiagramIR to D2 syntax.   |
|-------------------------------------------------------------------------|-----------------------------------|

### *class* ij.renderers.d2.D2Renderer(layout='dagre')

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
