"""Idea Junction - Connect vague ideas and evolve them to fully functional systems.

A bidirectional diagramming system that enables seamless movement between
natural language, visual diagrams, and code.
"""

# Core
from .analyzers import PythonCodeAnalyzer
from .core import DiagramIR, Edge, EdgeType, Node, NodeType
from .converters import EnhancedTextConverter, SimpleTextConverter
from .graph_ops import GraphOperations
from .parsers import D2Parser, MermaidParser
from .transforms import DiagramTransforms
from .renderers import (
    D2Renderer,
    GraphvizRenderer,
    InteractionAnalyzer,
    MermaidRenderer,
    PlantUMLRenderer,
    SequenceDiagramRenderer,
)

# New modules
from .validation import DiagramValidator, DiagramLinter, ValidationResult
from .git_integration import DiagramDiff, DiagramHistory
from .diagrams import ERDiagram, Entity, Field, Cardinality, StateMachine, State
from .export import ImageExporter, quick_export
from .layout import LayoutEngine, ForceDirectedLayout, HierarchicalLayout
from .plugins import PluginManager, register_plugin, register_transform
from .viewer import ViewerServer, serve_diagram

# Optional analyzers
try:
    from .analyzers.typescript import TypeScriptAnalyzer, analyze_package_json
    _has_typescript = True
except ImportError:
    _has_typescript = False

# Optional importers
try:
    from . import importers
    _has_importers = True
except ImportError:
    _has_importers = False

# LLMConverter is optional (requires openai package)
try:
    from .converters import LLMConverter
    _has_llm = True
except ImportError:
    _has_llm = False

__version__ = "0.2.0"

__all__ = [
    # Core
    "DiagramIR",
    "Node",
    "Edge",
    "NodeType",
    "EdgeType",
    "SimpleTextConverter",
    "EnhancedTextConverter",
    "MermaidRenderer",
    "PlantUMLRenderer",
    "D2Renderer",
    "GraphvizRenderer",
    "SequenceDiagramRenderer",
    "InteractionAnalyzer",
    "MermaidParser",
    "D2Parser",
    "GraphOperations",
    "PythonCodeAnalyzer",
    "DiagramTransforms",
    # Validation
    "DiagramValidator",
    "DiagramLinter",
    "ValidationResult",
    # Git integration
    "DiagramDiff",
    "DiagramHistory",
    # Diagrams
    "ERDiagram",
    "Entity",
    "Field",
    "Cardinality",
    "StateMachine",
    "State",
    # Export
    "ImageExporter",
    "quick_export",
    # Layout
    "LayoutEngine",
    "ForceDirectedLayout",
    "HierarchicalLayout",
    # Plugins
    "PluginManager",
    "register_plugin",
    "register_transform",
    # Viewer
    "ViewerServer",
    "serve_diagram",
    # Convenience
    "text_to_mermaid",
]

if _has_llm:
    __all__.append("LLMConverter")

if _has_typescript:
    __all__.extend(["TypeScriptAnalyzer", "analyze_package_json"])

if _has_importers:
    __all__.append("importers")


def text_to_mermaid(text: str, title: str = None, direction: str = "TD") -> str:
    """Convert text description to Mermaid diagram (convenience function).

    Args:
        text: Text description of the process/flow
        title: Optional diagram title
        direction: Flow direction (TD, LR, etc.)

    Returns:
        Mermaid syntax string

    Example:
        >>> mermaid = text_to_mermaid("Start -> Process data -> End")
        >>> print(mermaid)
        flowchart TD
            n0([Start])
            n1[Process data]
            n2([End])
            n0 --> n1
            n1 --> n2
    """
    converter = SimpleTextConverter()
    diagram = converter.convert(text, title=title)
    renderer = MermaidRenderer(direction=direction)
    return renderer.render(diagram)
