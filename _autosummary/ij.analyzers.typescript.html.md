# ij.analyzers.typescript

TypeScript and JavaScript code analyzer.

Analyze TypeScript/JavaScript code to generate diagrams.

### Functions

| [`analyze_package_json`](#ij.analyzers.typescript.analyze_package_json)(file_path)   | Analyze package.json to show dependency graph.   |
|------------------------------------------------------------------------------------|--------------------------------------------------|

### Classes

| [`TypeScriptAnalyzer`](#ij.analyzers.typescript.TypeScriptAnalyzer)()   | Analyze TypeScript/JavaScript code to create diagrams.   |
|-------------------------------------------------------------------------|----------------------------------------------------------|

### *class* ij.analyzers.typescript.TypeScriptAnalyzer

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

Analyze TypeScript/JavaScript code to create diagrams.

#### analyze_async_flow(code)

Analyze async/await flow in TypeScript/JavaScript.

* **Parameters:**
  **code** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Code with async operations
* **Return type:**
  [`DiagramIR`](ij.core.html.md#ij.core.DiagramIR)
* **Returns:**
  DiagramIR showing async flow

### Example

```pycon
>>> code = '''
... async function fetchData() {
...   const response = await fetch('/api');
...   const data = await response.json();
...   return data;
... }
... '''
>>> diagram = analyzer.analyze_async_flow(code)
```

#### analyze_function(code, function_name=None)

Analyze TypeScript/JavaScript function to create flowchart.

* **Parameters:**
  * **code** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – TypeScript/JavaScript code
  * **function_name** ([`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]) – Specific function to analyze (or first if None)
* **Return type:**
  [`DiagramIR`](ij.core.html.md#ij.core.DiagramIR)
* **Returns:**
  DiagramIR representing function flow

### Example

```pycon
>>> analyzer = TypeScriptAnalyzer()
>>> code = '''
... function processData(input) {
...   if (input > 0) {
...     return input * 2;
...   }
...   return 0;
... }
... '''
>>> diagram = analyzer.analyze_function(code)
```

#### analyze_module_imports(code)

Analyze TypeScript module imports/exports.

* **Parameters:**
  **code** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – TypeScript/JavaScript code
* **Return type:**
  [`DiagramIR`](ij.core.html.md#ij.core.DiagramIR)
* **Returns:**
  DiagramIR showing module dependencies

### Example

```pycon
>>> code = '''
... import { Component } from './components';
... import axios from 'axios';
... export default App;
... '''
>>> diagram = analyzer.analyze_module_imports(code)
```

#### analyze_react_component(code, component_name)

Analyze React component to show component hierarchy.

* **Parameters:**
  * **code** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – React component code
  * **component_name** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Name of the component
* **Return type:**
  [`DiagramIR`](ij.core.html.md#ij.core.DiagramIR)
* **Returns:**
  DiagramIR showing component structure

### Example

```pycon
>>> code = '''
... function App() {
...   return (
...     <div>
...       <Header />
...       <Content />
...       <Footer />
...     </div>
...   );
... }
... '''
>>> diagram = analyzer.analyze_react_component(code, 'App')
```

### ij.analyzers.typescript.analyze_package_json(file_path)

Analyze package.json to show dependency graph.

* **Parameters:**
  **file_path** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Path to package.json
* **Return type:**
  [`DiagramIR`](ij.core.html.md#ij.core.DiagramIR)
* **Returns:**
  DiagramIR showing dependencies

### Example

```pycon
>>> diagram = analyze_package_json('package.json')
```
