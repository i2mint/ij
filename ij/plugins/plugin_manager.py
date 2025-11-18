"""Plugin manager for extensible functionality."""

import importlib.util
import inspect
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

from ..core import DiagramIR


class Plugin:
    """Base class for plugins."""

    name: str = "base_plugin"
    version: str = "1.0.0"
    description: str = ""

    def initialize(self):
        """Initialize plugin (called once when loaded)."""
        pass

    def process(self, diagram: DiagramIR, **kwargs) -> DiagramIR:
        """Process diagram (override in subclass)."""
        return diagram


class PluginManager:
    """Manage and execute plugins."""

    def __init__(self):
        """Initialize plugin manager."""
        self.plugins: Dict[str, Plugin] = {}
        self.transforms: Dict[str, Callable] = {}
        self.hooks: Dict[str, List[Callable]] = {}

    def register_plugin(self, plugin: Plugin):
        """Register a plugin.

        Args:
            plugin: Plugin instance to register

        Example:
            >>> class MyPlugin(Plugin):
            ...     name = "my_plugin"
            ...     def process(self, diagram, **kwargs):
            ...         # Transform diagram
            ...         return diagram
            >>> manager = PluginManager()
            >>> manager.register_plugin(MyPlugin())
        """
        plugin.initialize()
        self.plugins[plugin.name] = plugin

    def register_transform(self, name: str, func: Callable):
        """Register a transform function.

        Args:
            name: Transform name
            func: Transform function (diagram, **kwargs) -> diagram

        Example:
            >>> def highlight_critical(diagram, start, end):
            ...     # Highlight path from start to end
            ...     return diagram
            >>> manager.register_transform('highlight-critical', highlight_critical)
        """
        self.transforms[name] = func

    def register_hook(self, event: str, func: Callable):
        """Register a hook for an event.

        Args:
            event: Event name ('pre_render', 'post_parse', etc.)
            func: Hook function

        Example:
            >>> def on_render(diagram):
            ...     print(f"Rendering {len(diagram.nodes)} nodes")
            >>> manager.register_hook('pre_render', on_render)
        """
        if event not in self.hooks:
            self.hooks[event] = []
        self.hooks[event].append(func)

    def execute_plugin(self, plugin_name: str, diagram: DiagramIR, **kwargs) -> DiagramIR:
        """Execute a plugin on a diagram.

        Args:
            plugin_name: Name of plugin to execute
            diagram: DiagramIR to process
            **kwargs: Plugin-specific arguments

        Returns:
            Transformed DiagramIR
        """
        if plugin_name not in self.plugins:
            raise ValueError(f"Plugin not found: {plugin_name}")

        plugin = self.plugins[plugin_name]
        return plugin.process(diagram, **kwargs)

    def apply_transform(self, transform_name: str, diagram: DiagramIR, **kwargs) -> DiagramIR:
        """Apply a registered transform.

        Args:
            transform_name: Name of transform
            diagram: DiagramIR to transform
            **kwargs: Transform arguments

        Returns:
            Transformed DiagramIR
        """
        if transform_name not in self.transforms:
            raise ValueError(f"Transform not found: {transform_name}")

        transform = self.transforms[transform_name]
        return transform(diagram, **kwargs)

    def trigger_hooks(self, event: str, *args, **kwargs):
        """Trigger all hooks for an event.

        Args:
            event: Event name
            *args: Event arguments
            **kwargs: Event keyword arguments
        """
        for hook in self.hooks.get(event, []):
            hook(*args, **kwargs)

    def load_plugin_file(self, file_path: str):
        """Load plugin from a Python file.

        Args:
            file_path: Path to plugin file

        Example:
            >>> manager.load_plugin_file('plugins/my_plugin.py')
        """
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Plugin file not found: {file_path}")

        # Load module
        spec = importlib.util.spec_from_file_location(path.stem, file_path)
        if spec and spec.loader:
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            # Find Plugin subclasses in module
            for name, obj in inspect.getmembers(module):
                if (
                    inspect.isclass(obj)
                    and issubclass(obj, Plugin)
                    and obj is not Plugin
                ):
                    self.register_plugin(obj())

    def load_plugins_directory(self, directory: str):
        """Load all plugins from a directory.

        Args:
            directory: Directory containing plugin files

        Example:
            >>> manager.load_plugins_directory('~/.ij/plugins')
        """
        dir_path = Path(directory).expanduser()
        if not dir_path.exists():
            return

        for file_path in dir_path.glob("*.py"):
            if file_path.name.startswith("_"):
                continue
            try:
                self.load_plugin_file(str(file_path))
            except Exception as e:
                print(f"Error loading plugin {file_path}: {e}")

    def list_plugins(self) -> List[Dict[str, str]]:
        """List all registered plugins.

        Returns:
            List of plugin information dictionaries
        """
        return [
            {
                "name": plugin.name,
                "version": plugin.version,
                "description": plugin.description,
            }
            for plugin in self.plugins.values()
        ]

    def list_transforms(self) -> List[str]:
        """List all registered transforms."""
        return list(self.transforms.keys())


# Global plugin manager instance
_global_manager = PluginManager()


def register_plugin(plugin: Plugin):
    """Register plugin with global manager."""
    _global_manager.register_plugin(plugin)


def register_transform(name: str):
    """Decorator to register a transform function.

    Example:
        >>> @register_transform('my-transform')
        ... def my_transform(diagram, **kwargs):
        ...     return diagram
    """

    def decorator(func: Callable):
        _global_manager.register_transform(name, func)
        return func

    return decorator


def get_global_manager() -> PluginManager:
    """Get the global plugin manager."""
    return _global_manager
