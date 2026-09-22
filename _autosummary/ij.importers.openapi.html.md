# ij.importers.openapi

Import diagrams from OpenAPI specifications.

### Functions

| [`from_openapi`](#ij.importers.openapi.from_openapi)(spec[, title])            | Import diagram from OpenAPI specification.                      |
|-----------------------------------------------------------------------------------------|-----------------------------------------------------------------|
| [`from_openapi_to_sequence`](#ij.importers.openapi.from_openapi_to_sequence)(spec[, flow]) | Create sequence diagram from OpenAPI spec showing request flow. |

### ij.importers.openapi.from_openapi(spec, title=None)

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

### ij.importers.openapi.from_openapi_to_sequence(spec, flow='default')

Create sequence diagram from OpenAPI spec showing request flow.

* **Parameters:**
  * **spec** (`Union`[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str), [`Dict`](https://docs.python.org/3/library/typing.html#typing.Dict)]) – Path to OpenAPI file or dict
  * **flow** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Flow to diagram (e.g., ‘auth’, ‘crud’)
* **Return type:**
  [`DiagramIR`](ij.core.html.md#ij.core.DiagramIR)
* **Returns:**
  DiagramIR as sequence diagram

### Example

```pycon
>>> diagram = from_openapi_to_sequence('api.yaml', flow='auth')
```
