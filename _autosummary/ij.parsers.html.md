# ij.parsers

Diagram parsers for various formats.

### Classes

| [`MermaidParser`](#ij.parsers.MermaidParser)(\*[, strict])   | Parses Mermaid flowchart syntax to DiagramIR.   |
|--------------------------------------------------------------------------------|-------------------------------------------------|
| [`D2Parser`](#ij.parsers.D2Parser)()                    | Parse D2 syntax to DiagramIR.                   |

### Exceptions

| [`MermaidParseWarning`](#ij.parsers.MermaidParseWarning)   | Warns that a Mermaid line could not be interpreted and was skipped.   |
|------------------------------------------------------------------------|-----------------------------------------------------------------------|

### *class* ij.parsers.D2Parser

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
  [`DiagramIR`](ij.core.html.md#ij.core.DiagramIR)
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
  [`DiagramIR`](ij.core.html.md#ij.core.DiagramIR)
* **Returns:**
  DiagramIR representation

### *exception* ij.parsers.MermaidParseWarning

Bases: [`UserWarning`](https://docs.python.org/3/builtins/exceptions.html#UserWarning)

Warns that a Mermaid line could not be interpreted and was skipped.

### *class* ij.parsers.MermaidParser(, strict=False)

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

Parses Mermaid flowchart syntax to DiagramIR.

Supports basic flowchart syntax including:

- Node definitions with various shapes, standalone or inline on an edge line
- Edge connections with labels, including chained edges
- Title metadata

A line matching none of the above is reported instead of being dropped:
see `unparsed_lines` and the `strict` argument.

#### strict

Whether an unparseable line raises instead of warning

#### nodes

Nodes found by the last parse, keyed by node id

#### edges

Edges found by the last parse

#### metadata

Diagram-level metadata (title, direction) from the last parse

#### unparsed_lines

Lines the last parse could not interpret

#### parse(mermaid_text)

Parse Mermaid syntax to DiagramIR.

* **Parameters:**
  **mermaid_text** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Mermaid flowchart syntax
* **Return type:**
  [`DiagramIR`](ij.core.html.md#ij.core.DiagramIR)
* **Returns:**
  DiagramIR representation
* **Raises:**
  [**ValueError**](https://docs.python.org/3/builtins/exceptions.html#ValueError) – If `strict` is set and a line cannot be parsed

### Example

```pycon
>>> parser = MermaidParser()
>>> diagram = parser.parse('''flowchart TD
...     start([Start]) --> check{Ok?}
...     check --|Yes|--> done([Done])''')
```

```pycon
>>> [(node.id, node.node_type.value) for node in diagram.nodes]
[('start', 'start'), ('check', 'decision'), ('done', 'end')]
>>> [(edge.source, edge.target, edge.label) for edge in diagram.edges]
[('start', 'check', None), ('check', 'done', 'Yes')]
```

#### parse_file(filename)

Parse Mermaid file to DiagramIR.

* **Parameters:**
  **filename** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Path to Mermaid file
* **Return type:**
  [`DiagramIR`](ij.core.html.md#ij.core.DiagramIR)
* **Returns:**
  DiagramIR representation

### Modules

| [`d2`](ij.parsers.d2.html.md#module-ij.parsers.d2)           | D2 diagram parser.      |
|------------------------------------------------------------------------------------|-------------------------|
| [`mermaid`](ij.parsers.mermaid.html.md#module-ij.parsers.mermaid) | Mermaid diagram parser. |
