# ij.importers

Import diagrams from external sources.

### Functions

| [`from_database`](#ij.importers.from_database)(connection_string[, schema])   | Import ERD from database schema.              |
|-----------------------------------------------------------------------------------------------|-----------------------------------------------|
| [`from_openapi`](#ij.importers.from_openapi)(spec[, title])                  | Import diagram from OpenAPI specification.    |
| [`from_drawio`](#ij.importers.from_drawio)(file_path[, page])               | Import diagram from draw.io file.             |
| [`from_plantuml`](#ij.importers.from_plantuml)(plantuml_code[, title])        | Parse PlantUML activity diagram to DiagramIR. |

### ij.importers.from_database(connection_string, schema=None)

Import ERD from database schema.

* **Parameters:**
  * **connection_string** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Database connection string
  * **schema** ([`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]) – Optional schema name
* **Return type:**
  [`ERDiagram`](ij.diagrams.erd.html.md#ij.diagrams.erd.ERDiagram)
* **Returns:**
  ERDiagram representing database schema

### Example

```pycon
>>> erd = from_database('postgresql://user:pass@localhost/mydb')
>>> erd = from_database('sqlite:///path/to/db.sqlite')
```

#### NOTE
Requires sqlalchemy: pip install sqlalchemy

### ij.importers.from_drawio(file_path, page=0)

Import diagram from draw.io file.

* **Parameters:**
  * **file_path** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Path to draw.io (.drawio or .xml) file
  * **page** ([`int`](https://docs.python.org/3/builtins/functions.html#int)) – Page number to import (0-indexed)
* **Return type:**
  [`DiagramIR`](ij.core.html.md#ij.core.DiagramIR)
* **Returns:**
  DiagramIR representation

### Example

```pycon
>>> diagram = from_drawio('flowchart.drawio')
```

#### NOTE
draw.io files use compressed XML. This provides basic support
for flowchart elements.

### ij.importers.from_openapi(spec, title=None)

Import diagram from OpenAPI specification.

Creates a diagram showing API endpoints and their relationships.

* **Parameters:**
  * **spec** (`Union`[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str), [`Dict`](https://docs.python.org/3/library/typing.html#typing.Dict)]) – Path to OpenAPI file or dict specification
  * **title** ([`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]) – Optional diagram title
* **Return type:**
  [`DiagramIR`](ij.core.html.md#ij.core.DiagramIR)
* **Returns:**
  DiagramIR representing API structure

### Example

```pycon
>>> diagram = from_openapi('openapi.yaml')
>>> diagram = from_openapi({'openapi': '3.0.0', ...})
```

#### NOTE
Requires pyyaml for YAML files: pip install pyyaml

### ij.importers.from_plantuml(plantuml_code, title=None)

Parse PlantUML activity diagram to DiagramIR.

* **Parameters:**
  * **plantuml_code** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – PlantUML source code
  * **title** ([`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]) – Optional diagram title
* **Return type:**
  [`DiagramIR`](ij.core.html.md#ij.core.DiagramIR)
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

### Modules

| [`database`](ij.importers.database.html.md#module-ij.importers.database)   | Import diagrams from database schemas.       |
|------------------------------------------------------------------------------------------|----------------------------------------------|
| [`drawio`](ij.importers.drawio.html.md#module-ij.importers.drawio)       | Import diagrams from draw.io files.          |
| [`openapi`](ij.importers.openapi.html.md#module-ij.importers.openapi)     | Import diagrams from OpenAPI specifications. |
| [`plantuml`](ij.importers.plantuml.html.md#module-ij.importers.plantuml)   | Import diagrams from PlantUML format.        |
