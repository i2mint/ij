# ij.validation

Diagram validation and linting.

Provides rules and validators to ensure diagram quality and consistency.

### Classes

| [`DiagramLinter`](#ij.validation.DiagramLinter)()                           | Lint diagrams for style and best practices.   |
|--------------------------------------------------------------------------------------------|-----------------------------------------------|
| [`DiagramValidator`](#ij.validation.DiagramValidator)()                        | Validate diagrams against various rules.      |
| [`Severity`](#ij.validation.Severity)(\*values)                        | Issue severity levels.                        |
| [`ValidationIssue`](#ij.validation.ValidationIssue)(severity, message[, ...]) | A validation issue found in a diagram.        |
| [`ValidationResult`](#ij.validation.ValidationResult)(is_valid, issues)        | Result of diagram validation.                 |

### *class* ij.validation.DiagramLinter

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

Lint diagrams for style and best practices.

#### lint(diagram)

Lint diagram for style issues.

* **Parameters:**
  **diagram** ([`DiagramIR`](ij.core.md#ij.core.DiagramIR)) – DiagramIR to lint
* **Return type:**
  [`List`](https://docs.python.org/3/library/typing.html#typing.List)[[`ValidationIssue`](#ij.validation.ValidationIssue)]
* **Returns:**
  List of linting issues

### Example

```pycon
>>> linter = DiagramLinter()
>>> issues = linter.lint(diagram)
>>> for issue in issues:
...     print(f"{issue.severity.value.upper()}: {issue.message}")
```

### *class* ij.validation.DiagramValidator

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

Validate diagrams against various rules.

#### validate(diagram, rules=None)

Validate diagram against rules.

* **Parameters:**
  * **diagram** ([`DiagramIR`](ij.core.md#ij.core.DiagramIR)) – DiagramIR to validate
  * **rules** ([`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`List`](https://docs.python.org/3/library/typing.html#typing.List)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]]) – List of rule names to check (None = all rules)
* **Return type:**
  [`ValidationResult`](#ij.validation.ValidationResult)
* **Returns:**
  ValidationResult with issues found

### Example

```pycon
>>> validator = DiagramValidator()
>>> result = validator.validate(diagram, rules=['no-cycles', 'no-orphaned-nodes'])
>>> if not result.is_valid:
...     for issue in result.errors:
...         print(f"ERROR: {issue.message}")
```

### *class* ij.validation.Severity(\*values)

Bases: [`Enum`](https://docs.python.org/3/library/enum.html#enum.Enum)

Issue severity levels.

### *class* ij.validation.ValidationIssue(severity, message, location=None, rule=None)

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

A validation issue found in a diagram.

### *class* ij.validation.ValidationResult(is_valid, issues)

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

Result of diagram validation.

#### *property* errors *: [List](https://docs.python.org/3/library/typing.html#typing.List)[[ValidationIssue](#ij.validation.ValidationIssue)]*

Get only error-level issues.

#### *property* warnings *: [List](https://docs.python.org/3/library/typing.html#typing.List)[[ValidationIssue](#ij.validation.ValidationIssue)]*

Get only warning-level issues.
