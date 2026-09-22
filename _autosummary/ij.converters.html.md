# ij.converters

Converters between different representations.

### Classes

| [`SimpleTextConverter`](#ij.converters.SimpleTextConverter)()                       | Simple rule-based text to diagram converter.              |
|----------------------------------------------------------------------------------------------|-----------------------------------------------------------|
| [`EnhancedTextConverter`](#ij.converters.EnhancedTextConverter)()                     | Enhanced text-to-diagram converter with NLP capabilities. |
| [`LLMConverter`](#ij.converters.LLMConverter)([api_key, model, temperature]) | AI-powered text to diagram converter using LLMs.          |

### *class* ij.converters.EnhancedTextConverter

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

Enhanced text-to-diagram converter with NLP capabilities.

Supports:

- Conditional branches (if/else)
- Parallel flows (parallel keyword)
- Loops (while, repeat)
- Better keyword detection
- Multiple sentence formats

#### convert(text, title=None)

Convert enhanced text to DiagramIR.

* **Parameters:**
  * **text** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Input text describing a process/flow
  * **title** ([`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]) – Optional diagram title
* **Return type:**
  [`DiagramIR`](ij.core.html.md#ij.core.DiagramIR)
* **Returns:**
  DiagramIR representation

### Examples

```pycon
>>> converter = EnhancedTextConverter()
>>> # Conditional
>>> diagram = converter.convert("Start -> Check user. If authenticated: Show dashboard, else: Show login")
>>> # Parallel
>>> diagram = converter.convert("Start -> [parallel: Process A, Process B] -> End")
```

### *class* ij.converters.LLMConverter(api_key=None, model='gpt-4o-mini', temperature=0.3)

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

AI-powered text to diagram converter using LLMs.

Uses OpenAI API with carefully crafted prompts to generate diagrams
from natural language descriptions. Supports iterative refinement.

#### convert(text, title=None, direction='TD')

Convert natural language to DiagramIR using LLM.

* **Parameters:**
  * **text** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Natural language description
  * **title** ([`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]) – Optional diagram title
  * **direction** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Diagram direction (TD, LR, etc.)
* **Return type:**
  [`DiagramIR`](ij.core.html.md#ij.core.DiagramIR)
* **Returns:**
  DiagramIR representation

### Example

```pycon
>>> converter = LLMConverter()
>>> diagram = converter.convert(
...     "A user logs into the system. If authentication succeeds, "
...     "they see the dashboard. Otherwise, they see an error message."
... )
```

#### convert_with_examples(text, examples, title=None)

Convert with few-shot examples for better quality.

* **Parameters:**
  * **text** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Natural language description
  * **examples** ([`List`](https://docs.python.org/3/library/typing.html#typing.List)[[`Dict`](https://docs.python.org/3/library/typing.html#typing.Dict)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str), [`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]]) – List of {“description”: “…”, “mermaid”: “…”} examples
  * **title** ([`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]) – Optional diagram title
* **Return type:**
  [`DiagramIR`](ij.core.html.md#ij.core.DiagramIR)
* **Returns:**
  DiagramIR representation

#### refine(diagram, feedback, current_mermaid)

Refine an existing diagram based on feedback.

* **Parameters:**
  * **diagram** ([`DiagramIR`](ij.core.html.md#ij.core.DiagramIR)) – Current diagram
  * **feedback** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – User feedback/instructions
  * **current_mermaid** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Current Mermaid representation
* **Return type:**
  [`DiagramIR`](ij.core.html.md#ij.core.DiagramIR)
* **Returns:**
  Refined DiagramIR

### Example

```pycon
>>> diagram = converter.convert("User login process")
>>> from ij.renderers import MermaidRenderer
>>> mermaid = MermaidRenderer().render(diagram)
>>> refined = converter.refine(
...     diagram,
...     "Add a step for password reset if login fails",
...     mermaid
... )
```

### *class* ij.converters.SimpleTextConverter

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

Simple rule-based text to diagram converter.

Parses structured text like:

- “Start -> Process A -> Decision B”
- “If condition: Process C, else: Process D”

#### convert(text, title=None)

Convert structured text to DiagramIR.

* **Parameters:**
  * **text** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Input text describing a process/flow
  * **title** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Optional diagram title
* **Return type:**
  [`DiagramIR`](ij.core.html.md#ij.core.DiagramIR)
* **Returns:**
  DiagramIR representation

### Modules

| [`enhanced_text`](ij.converters.enhanced_text.html.md#module-ij.converters.enhanced_text)   | Enhanced text to DiagramIR converter with better NLP.   |
|-----------------------------------------------------------------------------------------------------|---------------------------------------------------------|
| [`llm_converter`](ij.converters.llm_converter.html.md#module-ij.converters.llm_converter)   | AI/LLM-based text to diagram converter.                 |
| [`text_to_ir`](ij.converters.text_to_ir.html.md#module-ij.converters.text_to_ir)         | Text to DiagramIR converters.                           |
