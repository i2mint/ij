# ij.importers.plantuml

Import diagrams from PlantUML format.

### Functions

| [`from_plantuml`](#ij.importers.plantuml.from_plantuml)(plantuml_code[, title])   | Parse PlantUML activity diagram to DiagramIR.   |
|------------------------------------------------------------------------------------------|-------------------------------------------------|
| [`from_plantuml_file`](#ij.importers.plantuml.from_plantuml_file)(file_path)           | Import PlantUML from file.                      |

### ij.importers.plantuml.from_plantuml(plantuml_code, title=None)

Parse PlantUML activity diagram to DiagramIR.

* **Parameters:**
  * **plantuml_code** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – PlantUML source code
  * **title** ([`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]) – Optional diagram title
* **Return type:**
  [`DiagramIR`](ij.core.md#ij.core.DiagramIR)
* **Returns:**
  DiagramIR representation

### Example

```pycon
>>> code = '''
... @startuml
... start
... :Process;
... stop
... @enduml
... '''
>>> diagram = from_plantuml(code)
```

#### NOTE
Currently supports basic activity diagrams.
Full PlantUML syntax support is complex and partial.

### ij.importers.plantuml.from_plantuml_file(file_path)

Import PlantUML from file.

* **Parameters:**
  **file_path** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Path to PlantUML file
* **Return type:**
  [`DiagramIR`](ij.core.md#ij.core.DiagramIR)
* **Returns:**
  DiagramIR representation
