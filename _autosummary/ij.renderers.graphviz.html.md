# ij.renderers.graphviz

Graphviz/DOT diagram renderer.

Converts DiagramIR to DOT (Graphviz) syntax, the foundational graph
visualization language.

### Classes

| [`GraphvizRenderer`](#ij.renderers.graphviz.GraphvizRenderer)([layout, graph_type])   | Renders DiagramIR to Graphviz DOT syntax.   |
|-------------------------------------------------------------------------------------------|---------------------------------------------|

### *class* ij.renderers.graphviz.GraphvizRenderer(layout='dot', graph_type='digraph')

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

Renders DiagramIR to Graphviz DOT syntax.

Graphviz is the 30-year-old foundation that underpins PlantUML,
Structurizr, and many other tools.

#### render(diagram)

Render a DiagramIR to DOT syntax.

* **Parameters:**
  **diagram** ([`DiagramIR`](ij.core.html.md#ij.core.DiagramIR)) – The diagram to render
* **Return type:**
  [`str`](https://docs.python.org/3/builtins/stdtypes.html#str)
* **Returns:**
  DOT syntax as a string

#### render_to_file(diagram, filename)

Render diagram and save to file.

* **Parameters:**
  * **diagram** ([`DiagramIR`](ij.core.html.md#ij.core.DiagramIR)) – The diagram to render
  * **filename** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Path to output file
* **Return type:**
  [`None`](https://docs.python.org/3/builtins/constants.html#None)

#### render_to_image(diagram, filename, format='png')

Render diagram directly to image using graphviz library.

* **Parameters:**
  * **diagram** ([`DiagramIR`](ij.core.html.md#ij.core.DiagramIR)) – The diagram to render
  * **filename** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Path to output file (without extension)
  * **format** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Output format (png, svg, pdf, etc.)
* **Return type:**
  [`None`](https://docs.python.org/3/builtins/constants.html#None)
