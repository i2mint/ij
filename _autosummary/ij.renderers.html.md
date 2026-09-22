# ij.renderers

Diagram renderers for various formats.

### Classes

| [`MermaidRenderer`](#ij.renderers.MermaidRenderer)([direction])           | Renders DiagramIR to Mermaid syntax.                                         |
|-----------------------------------------------------------------------------------------|------------------------------------------------------------------------------|
| [`PlantUMLRenderer`](#ij.renderers.PlantUMLRenderer)([use_skinparam])      | Renders DiagramIR to PlantUML activity diagram syntax.                       |
| [`D2Renderer`](#ij.renderers.D2Renderer)([layout])                   | Renders DiagramIR to D2 syntax.                                              |
| [`GraphvizRenderer`](#ij.renderers.GraphvizRenderer)([layout, graph_type]) | Renders DiagramIR to Graphviz DOT syntax.                                    |
| [`SequenceDiagramRenderer`](#ij.renderers.SequenceDiagramRenderer)()              | Render DiagramIR as Mermaid sequence diagram.                                |
| [`InteractionAnalyzer`](#ij.renderers.InteractionAnalyzer)()                  | Analyze code or text to identify interaction patterns for sequence diagrams. |

### *class* ij.renderers.D2Renderer(layout='dagre')

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

Renders DiagramIR to D2 syntax.

D2 is a modern diagram language with clean syntax, multiple layout engines,
and PowerPoint export capabilities.

#### render(diagram)

Render a DiagramIR to D2 syntax.

* **Parameters:**
  **diagram** ([`DiagramIR`](ij.core.html.md#ij.core.DiagramIR)) – The diagram to render
* **Return type:**
  [`str`](https://docs.python.org/3/builtins/stdtypes.html#str)
* **Returns:**
  D2 syntax as a string

#### render_to_file(diagram, filename)

Render diagram and save to file.

* **Parameters:**
  * **diagram** ([`DiagramIR`](ij.core.html.md#ij.core.DiagramIR)) – The diagram to render
  * **filename** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Path to output file
* **Return type:**
  [`None`](https://docs.python.org/3/builtins/constants.html#None)

### *class* ij.renderers.GraphvizRenderer(layout='dot', graph_type='digraph')

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

Renders DiagramIR to Graphviz DOT syntax.

Graphviz is the 30-year-old foundation that underpins PlantUML,
Structurizr, and many other tools.

#### render(diagram)

Render a DiagramIR to DOT syntax.

* **Parameters:**
  **diagram** ([`DiagramIR`](ij.core.html.md#ij.core.DiagramIR)) – The diagram to render
* **Return type:**
  [`str`](https://docs.python.org/3/builtins/stdtypes.html#str)
* **Returns:**
  DOT syntax as a string

#### render_to_file(diagram, filename)

Render diagram and save to file.

* **Parameters:**
  * **diagram** ([`DiagramIR`](ij.core.html.md#ij.core.DiagramIR)) – The diagram to render
  * **filename** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Path to output file
* **Return type:**
  [`None`](https://docs.python.org/3/builtins/constants.html#None)

#### render_to_image(diagram, filename, format='png')

Render diagram directly to image using graphviz library.

* **Parameters:**
  * **diagram** ([`DiagramIR`](ij.core.html.md#ij.core.DiagramIR)) – The diagram to render
  * **filename** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Path to output file (without extension)
  * **format** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Output format (png, svg, pdf, etc.)
* **Return type:**
  [`None`](https://docs.python.org/3/builtins/constants.html#None)

### *class* ij.renderers.InteractionAnalyzer

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

Analyze code or text to identify interaction patterns for sequence diagrams.

#### analyze_function_calls(caller, code)

Analyze function calls to create a sequence diagram.

* **Parameters:**
  * **caller** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – The calling function/component name
  * **code** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Python code to analyze
* **Return type:**
  [`DiagramIR`](ij.core.html.md#ij.core.DiagramIR)
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
  [`DiagramIR`](ij.core.html.md#ij.core.DiagramIR)
* **Returns:**
  DiagramIR representing the interaction sequence

### Example

```pycon
>>> analyzer = InteractionAnalyzer()
>>> text = "User sends request to API. API queries Database. Database returns data to API. API responds to User."
>>> diagram = analyzer.from_text_description(text)
```

### *class* ij.renderers.MermaidRenderer(direction='TD')

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

Renders DiagramIR to Mermaid syntax.

Supports flowchart diagrams with various node shapes and edge types.

#### render(diagram)

Render a DiagramIR to Mermaid syntax.

* **Parameters:**
  **diagram** ([`DiagramIR`](ij.core.html.md#ij.core.DiagramIR)) – The diagram to render
* **Return type:**
  [`str`](https://docs.python.org/3/builtins/stdtypes.html#str)
* **Returns:**
  Mermaid syntax as a string

#### render_to_file(diagram, filename)

Render diagram and save to file.

* **Parameters:**
  * **diagram** ([`DiagramIR`](ij.core.html.md#ij.core.DiagramIR)) – The diagram to render
  * **filename** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Path to output file
* **Return type:**
  [`None`](https://docs.python.org/3/builtins/constants.html#None)

### *class* ij.renderers.PlantUMLRenderer(use_skinparam=True)

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

### *class* ij.renderers.SequenceDiagramRenderer

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
  **diagram** ([`DiagramIR`](ij.core.html.md#ij.core.DiagramIR)) – DiagramIR to render
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
  * **diagram** ([`DiagramIR`](ij.core.html.md#ij.core.DiagramIR)) – DiagramIR to render
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
  * **diagram** ([`DiagramIR`](ij.core.html.md#ij.core.DiagramIR)) – DiagramIR to render
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

### Modules

| [`d2`](ij.renderers.d2.html.md#module-ij.renderers.d2)             | D2 diagram renderer.                          |
|----------------------------------------------------------------------------------------|-----------------------------------------------|
| [`graphviz`](ij.renderers.graphviz.html.md#module-ij.renderers.graphviz) | Graphviz/DOT diagram renderer.                |
| [`mermaid`](ij.renderers.mermaid.html.md#module-ij.renderers.mermaid)   | Mermaid diagram renderer.                     |
| [`plantuml`](ij.renderers.plantuml.html.md#module-ij.renderers.plantuml) | PlantUML diagram renderer.                    |
| [`sequence`](ij.renderers.sequence.html.md#module-ij.renderers.sequence) | Sequence diagram renderer for Mermaid format. |
