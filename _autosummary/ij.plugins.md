# ij.plugins

Plugin system for extensibility.

### Functions

| [`register_plugin`](#ij.plugins.register_plugin)(plugin)   | Register plugin with global manager.        |
|----------------------------------------------------------------------------|---------------------------------------------|
| [`register_transform`](#ij.plugins.register_transform)(name)  | Decorator to register a transform function. |

### Classes

| [`PluginManager`](#ij.plugins.PluginManager)()   | Manage and execute plugins.   |
|--------------------------------------------------------------------|-------------------------------|

### *class* ij.plugins.PluginManager

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

Manage and execute plugins.

#### apply_transform(transform_name, diagram, \*\*kwargs)

Apply a registered transform.

* **Parameters:**
  * **transform_name** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Name of transform
  * **diagram** ([`DiagramIR`](ij.core.md#ij.core.DiagramIR)) – DiagramIR to transform
  * **\*\*kwargs** – Transform arguments
* **Return type:**
  [`DiagramIR`](ij.core.md#ij.core.DiagramIR)
* **Returns:**
  Transformed DiagramIR

#### execute_plugin(plugin_name, diagram, \*\*kwargs)

Execute a plugin on a diagram.

* **Parameters:**
  * **plugin_name** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Name of plugin to execute
  * **diagram** ([`DiagramIR`](ij.core.md#ij.core.DiagramIR)) – DiagramIR to process
  * **\*\*kwargs** – Plugin-specific arguments
* **Return type:**
  [`DiagramIR`](ij.core.md#ij.core.DiagramIR)
* **Returns:**
  Transformed DiagramIR

#### list_plugins()

List all registered plugins.

* **Return type:**
  [`List`](https://docs.python.org/3/library/typing.html#typing.List)[[`Dict`](https://docs.python.org/3/library/typing.html#typing.Dict)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str), [`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]]
* **Returns:**
  List of plugin information dictionaries

#### list_transforms()

List all registered transforms.

* **Return type:**
  [`List`](https://docs.python.org/3/library/typing.html#typing.List)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]

#### load_plugin_file(file_path)

Load plugin from a Python file.

* **Parameters:**
  **file_path** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Path to plugin file

### Example

```pycon
>>> manager.load_plugin_file('plugins/my_plugin.py')
```

#### load_plugins_directory(directory)

Load all plugins from a directory.

* **Parameters:**
  **directory** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Directory containing plugin files

### Example

```pycon
>>> manager.load_plugins_directory('~/.ij/plugins')
```

#### register_hook(event, func)

Register a hook for an event.

* **Parameters:**
  * **event** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Event name (‘pre_render’, ‘post_parse’, etc.)
  * **func** ([`Callable`](https://docs.python.org/3/library/typing.html#typing.Callable)) – Hook function

### Example

```pycon
>>> def on_render(diagram):
...     print(f"Rendering {len(diagram.nodes)} nodes")
>>> manager.register_hook('pre_render', on_render)
```

#### register_plugin(plugin)

Register a plugin.

* **Parameters:**
  **plugin** ([`Plugin`](ij.plugins.plugin_manager.md#ij.plugins.plugin_manager.Plugin)) – Plugin instance to register

### Example

```pycon
>>> class MyPlugin(Plugin):
...     name = "my_plugin"
...     def process(self, diagram, **kwargs):
...         # Transform diagram
...         return diagram
>>> manager = PluginManager()
>>> manager.register_plugin(MyPlugin())
```

#### register_transform(name, func)

Register a transform function.

* **Parameters:**
  * **name** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Transform name
  * **func** ([`Callable`](https://docs.python.org/3/library/typing.html#typing.Callable)) – Transform function (diagram, \*\*kwargs) -> diagram

### Example

```pycon
>>> def highlight_critical(diagram, start, end):
...     # Highlight path from start to end
...     return diagram
>>> manager.register_transform('highlight-critical', highlight_critical)
```

#### trigger_hooks(event, \*args, \*\*kwargs)

Trigger all hooks for an event.

* **Parameters:**
  * **event** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Event name
  * **\*args** – Event arguments
  * **\*\*kwargs** – Event keyword arguments

### ij.plugins.register_plugin(plugin)

Register plugin with global manager.

### ij.plugins.register_transform(name)

Decorator to register a transform function.

### Example

```pycon
>>> @register_transform('my-transform')
... def my_transform(diagram, **kwargs):
...     return diagram
```

### Modules

| [`plugin_manager`](ij.plugins.plugin_manager.md#module-ij.plugins.plugin_manager)   | Plugin manager for extensible functionality.   |
|----------------------------------------------------------------------------------------------------|------------------------------------------------|
