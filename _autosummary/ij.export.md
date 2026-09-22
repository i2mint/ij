# ij.export

Export functionality.

### Functions

| [`quick_export`](#ij.export.quick_export)(diagram, output_path[, format, ...])   | Quick export diagram to image.   |
|------------------------------------------------------------------------------------------------------|----------------------------------|

### Classes

| [`ImageExporter`](#ij.export.ImageExporter)([format, engine])   | Export diagrams to image formats.   |
|------------------------------------------------------------------------------------|-------------------------------------|

### *class* ij.export.ImageExporter(format='svg', engine='mermaid-cli')

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

Export diagrams to image formats.

#### check_dependencies()

Check which rendering engines are available.

* **Return type:**
  [`dict`](https://docs.python.org/3/builtins/stdtypes.html#dict)
* **Returns:**
  Dictionary of engine availability

### Example

```pycon
>>> exporter = ImageExporter()
>>> available = exporter.check_dependencies()
>>> if available['graphviz']:
...     print("Graphviz is installed")
```

#### render(diagram, output_path, width=None, height=None, background='white', theme='default')

Render diagram to image file.

* **Parameters:**
  * **diagram** ([`DiagramIR`](ij.core.md#ij.core.DiagramIR)) – DiagramIR to render
  * **output_path** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Output file path
  * **width** ([`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`int`](https://docs.python.org/3/builtins/functions.html#int)]) – Image width in pixels (optional)
  * **height** ([`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`int`](https://docs.python.org/3/builtins/functions.html#int)]) – Image height in pixels (optional)
  * **background** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Background color
  * **theme** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Diagram theme (‘default’, ‘dark’, ‘forest’, ‘neutral’)
* **Return type:**
  [`bool`](https://docs.python.org/3/builtins/functions.html#bool)
* **Returns:**
  True if successful, False otherwise

### Example

```pycon
>>> exporter = ImageExporter(format='png', engine='mermaid-cli')
>>> success = exporter.render(diagram, 'output.png', width=800)
```

### ij.export.quick_export(diagram, output_path, format='svg', engine=None)

Quick export diagram to image.

* **Parameters:**
  * **diagram** ([`DiagramIR`](ij.core.md#ij.core.DiagramIR)) – DiagramIR to export
  * **output_path** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Output file path
  * **format** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Image format (‘svg’, ‘png’, ‘pdf’)
  * **engine** ([`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]) – Rendering engine (auto-detected if None)
* **Return type:**
  [`bool`](https://docs.python.org/3/builtins/functions.html#bool)
* **Returns:**
  True if successful

### Example

```pycon
>>> from ij import DiagramIR, Node, Edge
>>> diagram = DiagramIR()
>>> # ... build diagram ...
>>> quick_export(diagram, 'diagram.png', format='png')
```

### Modules

| [`image`](ij.export.image.md#module-ij.export.image)   | Image export functionality for diagrams.   |
|---------------------------------------------------------------------------------|--------------------------------------------|
