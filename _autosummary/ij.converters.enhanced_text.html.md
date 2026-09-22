# ij.converters.enhanced_text

Enhanced text to DiagramIR converter with better NLP.

Provides more sophisticated text parsing with support for:

- Conditional branches
- Parallel flows
- Loop detection
- Better natural language understanding

### Classes

| [`EnhancedTextConverter`](#ij.converters.enhanced_text.EnhancedTextConverter)()   | Enhanced text-to-diagram converter with NLP capabilities.   |
|----------------------------------------------------------------------------|-------------------------------------------------------------|

### *class* ij.converters.enhanced_text.EnhancedTextConverter

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
