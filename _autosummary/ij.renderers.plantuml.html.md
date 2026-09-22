# ij.renderers.plantuml

PlantUML diagram renderer.

Converts DiagramIR to PlantUML syntax, supporting activity diagrams
which are ideal for process flows.

### Classes

| [`PlantUMLRenderer`](#ij.renderers.plantuml.PlantUMLRenderer)([use_skinparam])   | Renders DiagramIR to PlantUML activity diagram syntax.   |
|--------------------------------------------------------------------------------------|----------------------------------------------------------|

### *class* ij.renderers.plantuml.PlantUMLRenderer(use_skinparam=True)

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

Renders DiagramIR to PlantUML activity diagram syntax.

PlantUML is the enterprise standard for comprehensive UML diagrams
with support for 25+ diagram types.

#### render(diagram)

Render a DiagramIR to PlantUML syntax.

* **Parameters:**
  **diagram** ([`DiagramIR`](ij.core.html.md#ij.core.DiagramIR)) – The diagram to render
* **Return type:**
  [`str`](https://docs.python.org/3/builtins/stdtypes.html#str)
* **Returns:**
  PlantUML syntax as a string

#### render_to_file(diagram, filename)

Render diagram and save to file.

* **Parameters:**
  * **diagram** ([`DiagramIR`](ij.core.html.md#ij.core.DiagramIR)) – The diagram to render
  * **filename** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Path to output file
* **Return type:**
  [`None`](https://docs.python.org/3/builtins/constants.html#None)
