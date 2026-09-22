# ij.converters.text_to_ir

Text to DiagramIR converters.

This module provides simple rule-based conversion from structured text
to DiagramIR. Future versions can integrate AI/LLM-based conversion.

### Classes

| [`SimpleTextConverter`](#ij.converters.text_to_ir.SimpleTextConverter)()     | Simple rule-based text to diagram converter.                 |
|----------------------------------------------------------------------------|--------------------------------------------------------------|
| [`StructuredTextConverter`](#ij.converters.text_to_ir.StructuredTextConverter)() | More advanced converter supporting branching and conditions. |

### *class* ij.converters.text_to_ir.SimpleTextConverter

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
  [`DiagramIR`](ij.core.md#ij.core.DiagramIR)
* **Returns:**
  DiagramIR representation

### *class* ij.converters.text_to_ir.StructuredTextConverter

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

More advanced converter supporting branching and conditions.

Planned for future implementation to handle:

- Conditional branches
- Parallel flows
- Subprocesses
- Loops
