# ij.analyzers

Code analyzers for reverse engineering diagrams from code.

### Classes

| [`PythonCodeAnalyzer`](#ij.analyzers.PythonCodeAnalyzer)()   | Analyze Python code to generate diagrams.   |
|-------------------------------------------------------------------------|---------------------------------------------|

### *class* ij.analyzers.PythonCodeAnalyzer

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

Analyze Python code to generate diagrams.

Supports:

- Function call graphs
- Control flow diagrams
- Class relationship diagrams

#### analyze_class(code, class_name=None)

Analyze a Python class to create a class diagram.

* **Parameters:**
  * **code** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Python source code
  * **class_name** ([`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]) – Specific class to analyze (None = first class)
* **Return type:**
  [`DiagramIR`](ij.core.html.md#ij.core.DiagramIR)
* **Returns:**
  DiagramIR representation of the class structure

#### analyze_function(code, function_name=None)

Analyze a Python function to create a flowchart.

* **Parameters:**
  * **code** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Python source code
  * **function_name** ([`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]) – Specific function to analyze (None = first function)
* **Return type:**
  [`DiagramIR`](ij.core.html.md#ij.core.DiagramIR)
* **Returns:**
  DiagramIR representation of the function’s control flow

### Example

```pycon
>>> code = '''
... def process_order(order):
...     if order.is_valid():
...         save_to_database(order)
...         send_confirmation(order)
...     else:
...         send_error_notification(order)
... '''
>>> analyzer = PythonCodeAnalyzer()
>>> diagram = analyzer.analyze_function(code)
```

#### analyze_module_calls(code)

Analyze function calls in a module to create a call graph.

* **Parameters:**
  **code** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Python source code
* **Return type:**
  [`DiagramIR`](ij.core.html.md#ij.core.DiagramIR)
* **Returns:**
  DiagramIR representation of function call relationships

### Modules

| [`python_analyzer`](ij.analyzers.python_analyzer.html.md#module-ij.analyzers.python_analyzer)   | Python code analyzer for reverse engineering diagrams.   |
|--------------------------------------------------------------------------------------------------------|----------------------------------------------------------|
| [`typescript`](ij.analyzers.typescript.html.md#module-ij.analyzers.typescript)             | TypeScript and JavaScript code analyzer.                 |
