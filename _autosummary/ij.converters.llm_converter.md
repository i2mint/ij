# ij.converters.llm_converter

AI/LLM-based text to diagram converter.

Uses OpenAI API for intelligent natural language understanding and
diagram generation. Follows research recommendations for AI-powered
diagram generation (10-20x faster initial drafts).

### Classes

| [`LLMConverter`](#ij.converters.llm_converter.LLMConverter)([api_key, model, temperature])   | AI-powered text to diagram converter using LLMs.   |
|------------------------------------------------------------------------------------------------|----------------------------------------------------|

### *class* ij.converters.llm_converter.LLMConverter(api_key=None, model='gpt-4o-mini', temperature=0.3)

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
  [`DiagramIR`](ij.core.md#ij.core.DiagramIR)
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
  [`DiagramIR`](ij.core.md#ij.core.DiagramIR)
* **Returns:**
  DiagramIR representation

#### refine(diagram, feedback, current_mermaid)

Refine an existing diagram based on feedback.

* **Parameters:**
  * **diagram** ([`DiagramIR`](ij.core.md#ij.core.DiagramIR)) – Current diagram
  * **feedback** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – User feedback/instructions
  * **current_mermaid** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Current Mermaid representation
* **Return type:**
  [`DiagramIR`](ij.core.md#ij.core.DiagramIR)
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
