# ij.cli_enhanced

Enhanced command-line interface for Idea Junction.

Provides subcommands for conversion, validation, diff, and more.

### Module Attributes

| [`DEFAULT_OUTPUT_FORMAT`](#ij.cli_enhanced.DEFAULT_OUTPUT_FORMAT)   | Output format of a file whose extension names no renderable format.   |
|--------------------------------------------------------------------------|-----------------------------------------------------------------------|

### Functions

| [`cmd_convert`](#ij.cli_enhanced.cmd_convert)(args)                                 | Convert between diagram formats.                                                                                                                                                       |
|----------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| [`cmd_diff`](#ij.cli_enhanced.cmd_diff)(args)                                    | Show differences between two diagrams.                                                                                                                                                 |
| [`cmd_extract`](#ij.cli_enhanced.cmd_extract)(args)                                 | Extract a subgraph.                                                                                                                                                                    |
| [`cmd_simplify`](#ij.cli_enhanced.cmd_simplify)(args)                                | Simplify a diagram.                                                                                                                                                                    |
| [`cmd_stats`](#ij.cli_enhanced.cmd_stats)(args)                                   | Show diagram statistics.                                                                                                                                                               |
| [`cmd_validate`](#ij.cli_enhanced.cmd_validate)(args)                                | Validate diagram files.                                                                                                                                                                |
| [`cmd_watch`](#ij.cli_enhanced.cmd_watch)(args)                                   | Watch files for changes and auto-convert.                                                                                                                                              |
| [`detect_format`](#ij.cli_enhanced.detect_format)(filename)                           | Detect format from file extension (mermaid when the extension is unknown).                                                                                                             |
| [`detect_output_format`](#ij.cli_enhanced.detect_output_format)(filename)                    | Detect the format to write `filename` in: its extension's format if there is a renderer for it, else `DEFAULT_OUTPUT_FORMAT` (e.g. `.txt`, read as plain text but written as mermaid). |
| [`get_parser_for_format`](#ij.cli_enhanced.get_parser_for_format)(format_name)                | Get parser instance for a format.                                                                                                                                                      |
| [`get_renderer_for_format`](#ij.cli_enhanced.get_renderer_for_format)(format_name, \*\*kwargs)  | Get renderer instance for a format.                                                                                                                                                    |
| [`main`](#ij.cli_enhanced.main)()                                            | Enhanced CLI entry point.                                                                                                                                                              |
| [`resolve_output_format`](#ij.cli_enhanced.resolve_output_format)([format_name, output, ...]) | The format a command writes in.                                                                                                                                                        |

### ij.cli_enhanced.DEFAULT_OUTPUT_FORMAT *= 'mermaid'*

Output format of a file whose extension names no renderable format.

### ij.cli_enhanced.cmd_convert(args)

Convert between diagram formats.

### ij.cli_enhanced.cmd_diff(args)

Show differences between two diagrams.

### ij.cli_enhanced.cmd_extract(args)

Extract a subgraph.

### ij.cli_enhanced.cmd_simplify(args)

Simplify a diagram.

### ij.cli_enhanced.cmd_stats(args)

Show diagram statistics.

### ij.cli_enhanced.cmd_validate(args)

Validate diagram files.

### ij.cli_enhanced.cmd_watch(args)

Watch files for changes and auto-convert.

### ij.cli_enhanced.detect_format(filename)

Detect format from file extension (mermaid when the extension is unknown).

* **Return type:**
  [`str`](https://docs.python.org/3/builtins/stdtypes.html#str)

### ij.cli_enhanced.detect_output_format(filename)

Detect the format to write `filename` in: its extension’s format if there is a
renderer for it, else `DEFAULT_OUTPUT_FORMAT` (e.g. `.txt`, read as plain text
but written as mermaid).

```pycon
>>> detect_output_format("out.d2"), detect_output_format("out.txt")
('d2', 'mermaid')
```

* **Return type:**
  [`str`](https://docs.python.org/3/builtins/stdtypes.html#str)

### ij.cli_enhanced.get_parser_for_format(format_name)

Get parser instance for a format.

### ij.cli_enhanced.get_renderer_for_format(format_name, \*\*kwargs)

Get renderer instance for a format.

### ij.cli_enhanced.main()

Enhanced CLI entry point.

### ij.cli_enhanced.resolve_output_format(format_name=None, , output=None, input_format=None)

The format a command writes in. Every rendering command uses this one rule.

In order: the explicit `format_name`; else the `output` file’s format, if its
extension is known and has a renderer; else `input_format`, if it has a renderer
(`simplify` and `extract` keep the input’s format); else
`DEFAULT_OUTPUT_FORMAT`. So a `.txt` file (read as plain text, no renderer) is
never asked to be rendered as `text`.

```pycon
>>> resolve_output_format(output="out.d2"), resolve_output_format(output="out.txt")
('d2', 'mermaid')
>>> resolve_output_format(output="out.txt", input_format="d2")
'd2'
>>> resolve_output_format(input_format="text")
'mermaid'
```

* **Return type:**
  [`str`](https://docs.python.org/3/builtins/stdtypes.html#str)
