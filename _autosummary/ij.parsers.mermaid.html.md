# ij.parsers.mermaid

Mermaid diagram parser.

Converts Mermaid syntax back to DiagramIR, enabling bidirectional conversion.

Lines the parser cannot interpret are *reported* rather than dropped: each one
is recorded in `MermaidParser.unparsed_lines` and raised as a
`MermaidParseWarning` (or, with `strict=True`, a `ValueError`). Silently
discarding them used to turn generator drift into a silently wrong diagram –
e.g. an LLM emitting `check_user --|Yes|--> show_dashboard` instead of
`check_user -->|Yes| show_dashboard` cost both the edge and the
`check_user{...}` decision node it referenced, with no signal at all.

### Classes

| [`MermaidParser`](#ij.parsers.mermaid.MermaidParser)(\*[, strict])   | Parses Mermaid flowchart syntax to DiagramIR.   |
|--------------------------------------------------------------------------------|-------------------------------------------------|

### Exceptions

| [`MermaidParseWarning`](#ij.parsers.mermaid.MermaidParseWarning)   | Warns that a Mermaid line could not be interpreted and was skipped.   |
|------------------------------------------------------------------------|-----------------------------------------------------------------------|

### *exception* ij.parsers.mermaid.MermaidParseWarning

Bases: [`UserWarning`](https://docs.python.org/3/builtins/exceptions.html#UserWarning)

Warns that a Mermaid line could not be interpreted and was skipped.

### *class* ij.parsers.mermaid.MermaidParser(, strict=False)

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
