# ij.parsers.d2

D2 diagram parser.

Parses D2 (Terrastruct) syntax to DiagramIR, completing bidirectional
support for the modern D2 format.

### Classes

| [`D2Parser`](#ij.parsers.d2.D2Parser)()   | Parse D2 syntax to DiagramIR.   |
|---------------------------------------------------------------|---------------------------------|

### *class* ij.parsers.d2.D2Parser

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

Parse D2 syntax to DiagramIR.

Supports basic D2 syntax including:

- Node definitions with shapes and labels
- Edge connections with labels
- Direction metadata

#### parse(d2_text)

Parse D2 syntax to DiagramIR.

* **Parameters:**
  **d2_text** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – D2 diagram source
* **Return type:**
  [`DiagramIR`](ij.core.md#ij.core.DiagramIR)
* **Returns:**
  DiagramIR representation

### Example

```pycon
>>> parser = D2Parser()
>>> d2_code = '''
... n1: "Start" {
...   shape: oval
... }
... n2: "Process" {
...   shape: rectangle
... }
... n1 -> n2
... '''
>>> diagram = parser.parse(d2_code)
```

#### parse_file(filename)

Parse D2 file to DiagramIR.

* **Parameters:**
  **filename** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Path to D2 file
* **Return type:**
  [`DiagramIR`](ij.core.md#ij.core.DiagramIR)
* **Returns:**
  DiagramIR representation
