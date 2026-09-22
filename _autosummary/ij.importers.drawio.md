# ij.importers.drawio

Import diagrams from draw.io files.

### Functions

| [`from_drawio`](#ij.importers.drawio.from_drawio)(file_path[, page])   | Import diagram from draw.io file.    |
|-----------------------------------------------------------------------------------|--------------------------------------|
| [`from_drawio_xml`](#ij.importers.drawio.from_drawio_xml)(xml_content)     | Import from raw draw.io XML content. |

### ij.importers.drawio.from_drawio(file_path, page=0)

Import diagram from draw.io file.

* **Parameters:**
  * **file_path** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Path to draw.io (.drawio or .xml) file
  * **page** ([`int`](https://docs.python.org/3/builtins/functions.html#int)) – Page number to import (0-indexed)
* **Return type:**
  [`DiagramIR`](ij.core.md#ij.core.DiagramIR)
* **Returns:**
  DiagramIR representation

### Example

```pycon
>>> diagram = from_drawio('flowchart.drawio')
```

#### NOTE
draw.io files use compressed XML. This provides basic support
for flowchart elements.

### ij.importers.drawio.from_drawio_xml(xml_content)

Import from raw draw.io XML content.

* **Parameters:**
  **xml_content** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – draw.io XML string
* **Return type:**
  [`DiagramIR`](ij.core.md#ij.core.DiagramIR)
* **Returns:**
  DiagramIR representation
