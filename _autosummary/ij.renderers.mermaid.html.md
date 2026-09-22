# ij.renderers.mermaid

Mermaid diagram renderer.

Converts DiagramIR to Mermaid syntax, following the research recommendation
to use Mermaid for its GitHub integration and simplicity.

### Classes

| [`MermaidRenderer`](#ij.renderers.mermaid.MermaidRenderer)([direction])   | Renders DiagramIR to Mermaid syntax.   |
|---------------------------------------------------------------------------------|----------------------------------------|

### *class* ij.renderers.mermaid.MermaidRenderer(direction='TD')

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

Renders DiagramIR to Mermaid syntax.

Supports flowchart diagrams with various node shapes and edge types.

#### render(diagram)

Render a DiagramIR to Mermaid syntax.

* **Parameters:**
  **diagram** ([`DiagramIR`](ij.core.html.md#ij.core.DiagramIR)) – The diagram to render
* **Return type:**
  [`str`](https://docs.python.org/3/builtins/stdtypes.html#str)
* **Returns:**
  Mermaid syntax as a string

#### render_to_file(diagram, filename)

Render diagram and save to file.

* **Parameters:**
  * **diagram** ([`DiagramIR`](ij.core.html.md#ij.core.DiagramIR)) – The diagram to render
  * **filename** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Path to output file
* **Return type:**
  [`None`](https://docs.python.org/3/builtins/constants.html#None)
