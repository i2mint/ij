# ij.cli_enhanced

Enhanced command-line interface for Idea Junction.

Provides subcommands for conversion, validation, diff, and more.

### Functions

| [`cmd_convert`](#ij.cli_enhanced.cmd_convert)(args)                                | Convert between diagram formats.          |
|---------------------------------------------------------------------------------------------------|-------------------------------------------|
| [`cmd_diff`](#ij.cli_enhanced.cmd_diff)(args)                                   | Show differences between two diagrams.    |
| [`cmd_extract`](#ij.cli_enhanced.cmd_extract)(args)                                | Extract a subgraph.                       |
| [`cmd_simplify`](#ij.cli_enhanced.cmd_simplify)(args)                               | Simplify a diagram.                       |
| [`cmd_stats`](#ij.cli_enhanced.cmd_stats)(args)                                  | Show diagram statistics.                  |
| [`cmd_validate`](#ij.cli_enhanced.cmd_validate)(args)                               | Validate diagram files.                   |
| [`cmd_watch`](#ij.cli_enhanced.cmd_watch)(args)                                  | Watch files for changes and auto-convert. |
| [`detect_format`](#ij.cli_enhanced.detect_format)(filename)                          | Detect format from file extension.        |
| [`get_parser_for_format`](#ij.cli_enhanced.get_parser_for_format)(format_name)               | Get parser instance for a format.         |
| [`get_renderer_for_format`](#ij.cli_enhanced.get_renderer_for_format)(format_name, \*\*kwargs) | Get renderer instance for a format.       |
| [`main`](#ij.cli_enhanced.main)()                                           | Enhanced CLI entry point.                 |

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

Detect format from file extension.

* **Return type:**
  [`str`](https://docs.python.org/3/builtins/stdtypes.html#str)

### ij.cli_enhanced.get_parser_for_format(format_name)

Get parser instance for a format.

### ij.cli_enhanced.get_renderer_for_format(format_name, \*\*kwargs)

Get renderer instance for a format.

### ij.cli_enhanced.main()

Enhanced CLI entry point.
