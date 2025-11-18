"""Plugin system for extensibility."""

from .plugin_manager import PluginManager, register_plugin, register_transform

__all__ = ["PluginManager", "register_plugin", "register_transform"]
