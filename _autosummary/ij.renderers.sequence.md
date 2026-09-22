# ij.renderers.sequence

Sequence diagram renderer for Mermaid format.

Renders DiagramIR as Mermaid sequence diagrams for showing interactions
and message flows between participants over time.

### Classes

| [`InteractionAnalyzer`](#ij.renderers.sequence.InteractionAnalyzer)()     | Analyze code or text to identify interaction patterns for sequence diagrams.   |
|----------------------------------------------------------------------------|--------------------------------------------------------------------------------|
| [`SequenceDiagramRenderer`](#ij.renderers.sequence.SequenceDiagramRenderer)() | Render DiagramIR as Mermaid sequence diagram.                                  |

### *class* ij.renderers.sequence.InteractionAnalyzer

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

Analyze code or text to identify interaction patterns for sequence diagrams.

#### analyze_function_calls(caller, code)

Analyze function calls to create a sequence diagram.

* **Parameters:**
  * **caller** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – The calling function/component name
  * **code** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Python code to analyze
* **Return type:**
  [`DiagramIR`](ij.core.md#ij.core.DiagramIR)
* **Returns:**
  DiagramIR representing the call sequence

### Example

```pycon
>>> analyzer = InteractionAnalyzer()
>>> code = '''
... api.authenticate(user)
... db.query(user_id)
... cache.store(result)
... '''
>>> diagram = analyzer.analyze_function_calls("client", code)
```

#### from_text_description(text)

Create sequence diagram from text description.

* **Parameters:**
  **text** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Natural language description of interactions
* **Return type:**
  [`DiagramIR`](ij.core.md#ij.core.DiagramIR)
* **Returns:**
  DiagramIR representing the interaction sequence

### Example

```pycon
>>> analyzer = InteractionAnalyzer()
>>> text = "User sends request to API. API queries Database. Database returns data to API. API responds to User."
>>> diagram = analyzer.from_text_description(text)
```

### *class* ij.renderers.sequence.SequenceDiagramRenderer

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

Render DiagramIR as Mermaid sequence diagram.

Maps DiagramIR concepts to sequence diagrams:

- Nodes -> Participants
- Edges -> Messages between participants
- Edge labels -> Message content
- EdgeType.DIRECT -> Solid arrows (synchronous)
- EdgeType.CONDITIONAL -> Dashed arrows (asynchronous/return)
- EdgeType.BIDIRECTIONAL -> Bidirectional arrows

#### render(diagram)

Render DiagramIR as Mermaid sequence diagram.

* **Parameters:**
  **diagram** ([`DiagramIR`](ij.core.md#ij.core.DiagramIR)) – DiagramIR to render
* **Return type:**
  [`str`](https://docs.python.org/3/builtins/stdtypes.html#str)
* **Returns:**
  Mermaid sequence diagram syntax

### Example

```pycon
>>> from ij import DiagramIR, Node, Edge
>>> diagram = DiagramIR()
>>> diagram.add_node(Node(id="user", label="User"))
>>> diagram.add_node(Node(id="api", label="API"))
>>> diagram.add_edge(Edge(source="user", target="api", label="Request"))
>>> renderer = SequenceDiagramRenderer()
>>> print(renderer.render(diagram))
sequenceDiagram
    participant user as User
    participant api as API
    user->>api: Request
```

#### render_with_activations(diagram, activations)

Render sequence diagram with participant activations.

* **Parameters:**
  * **diagram** ([`DiagramIR`](ij.core.md#ij.core.DiagramIR)) – DiagramIR to render
  * **activations** ([`List`](https://docs.python.org/3/library/typing.html#typing.List)[[`tuple`](https://docs.python.org/3/builtins/stdtypes.html#tuple)]) – List of (participant_id, “activate”/”deactivate”) tuples
* **Return type:**
  [`str`](https://docs.python.org/3/builtins/stdtypes.html#str)
* **Returns:**
  Mermaid sequence diagram with activations

### Example

```pycon
>>> activations = [("api", "activate"), ("api", "deactivate")]
>>> renderer.render_with_activations(diagram, activations)
```

#### render_with_notes(diagram, notes)

Render sequence diagram with notes.

* **Parameters:**
  * **diagram** ([`DiagramIR`](ij.core.md#ij.core.DiagramIR)) – DiagramIR to render
  * **notes** ([`Dict`](https://docs.python.org/3/library/typing.html#typing.Dict)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str), [`List`](https://docs.python.org/3/library/typing.html#typing.List)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]]) – Dict mapping participant IDs to list of notes
* **Return type:**
  [`str`](https://docs.python.org/3/builtins/stdtypes.html#str)
* **Returns:**
  Mermaid sequence diagram with notes

### Example

```pycon
>>> notes = {"user": ["Note about user"], "api": ["API note"]}
>>> renderer.render_with_notes(diagram, notes)
```
