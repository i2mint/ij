"""Enhanced command-line interface for Idea Junction.

Provides subcommands for conversion, validation, diff, and more.
"""

import argparse
import sys
from pathlib import Path
from typing import Optional

from . import (
    D2Parser,
    D2Renderer,
    DiagramIR,
    DiagramTransforms,
    GraphvizRenderer,
    MermaidParser,
    MermaidRenderer,
    PlantUMLRenderer,
    SimpleTextConverter,
)


def get_parser_for_format(format_name: str):
    """Get parser instance for a format."""
    parsers = {
        "mermaid": MermaidParser,
        "mmd": MermaidParser,
        "d2": D2Parser,
    }
    parser_class = parsers.get(format_name.lower())
    if parser_class:
        return parser_class()
    raise ValueError(f"No parser available for format: {format_name}")


def get_renderer_for_format(format_name: str, **kwargs):
    """Get renderer instance for a format."""
    renderers = {
        "mermaid": MermaidRenderer,
        "mmd": MermaidRenderer,
        "d2": D2Renderer,
        "plantuml": PlantUMLRenderer,
        "puml": PlantUMLRenderer,
        "graphviz": GraphvizRenderer,
        "dot": GraphvizRenderer,
    }
    renderer_class = renderers.get(format_name.lower())
    if renderer_class:
        return renderer_class(**kwargs)
    raise ValueError(f"No renderer available for format: {format_name}")


def detect_format(filename: str) -> str:
    """Detect format from file extension."""
    ext = Path(filename).suffix.lower()
    format_map = {
        ".mmd": "mermaid",
        ".mermaid": "mermaid",
        ".d2": "d2",
        ".puml": "plantuml",
        ".plantuml": "plantuml",
        ".dot": "graphviz",
        ".gv": "graphviz",
    }
    return format_map.get(ext, "mermaid")


def cmd_convert(args):
    """Convert between diagram formats."""
    # Determine input format
    if args.from_format:
        input_format = args.from_format
    else:
        input_format = detect_format(args.input)

    # Determine output format
    if args.to_format:
        output_format = args.to_format
    elif args.output:
        output_format = detect_format(args.output)
    else:
        output_format = "mermaid"

    # Read input
    try:
        input_text = Path(args.input).read_text()
    except FileNotFoundError:
        print(f"Error: Input file '{args.input}' not found", file=sys.stderr)
        sys.exit(1)

    # Parse input
    try:
        parser = get_parser_for_format(input_format)
        diagram = parser.parse(input_text)
    except ValueError as e:
        # Try text converter as fallback
        converter = SimpleTextConverter()
        diagram = converter.convert(input_text)

    # Render output
    renderer_kwargs = {}
    if args.direction:
        renderer_kwargs["direction"] = args.direction

    renderer = get_renderer_for_format(output_format, **renderer_kwargs)
    output_text = renderer.render(diagram)

    # Write output
    if args.output:
        Path(args.output).write_text(output_text)
        print(f"✅ Converted {input_format} → {output_format}: {args.output}")
    else:
        print(output_text)


def cmd_validate(args):
    """Validate diagram files."""
    from .validation import DiagramValidator

    validator = DiagramValidator()

    # Collect files
    files = []
    for pattern in args.files:
        path = Path(pattern)
        if path.is_file():
            files.append(path)
        elif "*" in pattern or "?" in pattern:
            # Glob pattern
            files.extend(Path(".").glob(pattern))

    if not files:
        print("No files found to validate", file=sys.stderr)
        sys.exit(1)

    total_issues = 0
    for file_path in files:
        # Parse file
        format_name = detect_format(str(file_path))
        try:
            parser = get_parser_for_format(format_name)
            input_text = file_path.read_text()
            diagram = parser.parse(input_text)
        except Exception as e:
            print(f"❌ {file_path}: Parse error - {e}")
            total_issues += 1
            continue

        # Validate
        rules = []
        if args.no_orphans:
            rules.append("no-orphaned-nodes")
        if args.no_cycles:
            rules.append("no-cycles")
        if args.require_start_end:
            rules.append("require-start-end")
        if args.max_nodes:
            rules.append(f"max-nodes-{args.max_nodes}")
        if args.max_edges:
            rules.append(f"max-edges-{args.max_edges}")

        if not rules:
            rules = ["no-orphaned-nodes", "no-cycles"]  # Default rules

        results = validator.validate(diagram, rules=rules)

        if results.is_valid:
            print(f"✅ {file_path}: Valid")
        else:
            print(f"❌ {file_path}: {len(results.issues)} issue(s)")
            for issue in results.issues:
                print(f"   {issue.severity.upper()}: {issue.message}")
                total_issues += 1

    if total_issues > 0:
        sys.exit(1)


def cmd_stats(args):
    """Show diagram statistics."""
    file_path = Path(args.file)
    if not file_path.exists():
        print(f"Error: File '{args.file}' not found", file=sys.stderr)
        sys.exit(1)

    # Parse file
    format_name = detect_format(str(file_path))
    parser = get_parser_for_format(format_name)
    input_text = file_path.read_text()
    diagram = parser.parse(input_text)

    # Get statistics
    stats = DiagramTransforms.get_statistics(diagram)

    # Display
    print(f"Statistics for {file_path}:")
    print(f"  Nodes: {stats['node_count']}")
    print(f"  Edges: {stats['edge_count']}")
    print(f"  Isolated nodes: {stats['isolated_nodes']}")
    print(f"  Has cycles: {stats['has_cycles']}")
    print(f"  Max incoming degree: {stats['max_incoming_degree']}")
    print(f"  Max outgoing degree: {stats['max_outgoing_degree']}")

    if stats["node_types"]:
        print(f"  Node types:")
        for node_type, count in stats["node_types"].items():
            print(f"    {node_type.value}: {count}")

    if stats["edge_types"]:
        print(f"  Edge types:")
        for edge_type, count in stats["edge_types"].items():
            print(f"    {edge_type.value}: {count}")


def cmd_simplify(args):
    """Simplify a diagram."""
    file_path = Path(args.input)
    if not file_path.exists():
        print(f"Error: File '{args.input}' not found", file=sys.stderr)
        sys.exit(1)

    # Parse
    format_name = detect_format(str(file_path))
    parser = get_parser_for_format(format_name)
    input_text = file_path.read_text()
    diagram = parser.parse(input_text)

    # Simplify
    simplified = DiagramTransforms.simplify(
        diagram, remove_isolated=not args.keep_isolated
    )

    # Render
    output_format = args.format or format_name
    renderer = get_renderer_for_format(output_format)
    output_text = renderer.render(simplified)

    # Write
    if args.output:
        Path(args.output).write_text(output_text)
        print(f"✅ Simplified diagram saved to {args.output}")
        print(f"   Before: {len(diagram.nodes)} nodes, {len(diagram.edges)} edges")
        print(
            f"   After:  {len(simplified.nodes)} nodes, {len(simplified.edges)} edges"
        )
    else:
        print(output_text)


def cmd_diff(args):
    """Show differences between two diagrams."""
    from .git_integration import DiagramDiff

    # Parse both files
    file1 = Path(args.file1)
    file2 = Path(args.file2)

    if not file1.exists():
        print(f"Error: File '{args.file1}' not found", file=sys.stderr)
        sys.exit(1)
    if not file2.exists():
        print(f"Error: File '{args.file2}' not found", file=sys.stderr)
        sys.exit(1)

    differ = DiagramDiff()
    changes = differ.compare_files(str(file1), str(file2))

    # Display changes
    print(f"Comparing {file1} → {file2}:")
    print(f"  Added nodes: {len(changes.added_nodes)}")
    print(f"  Removed nodes: {len(changes.removed_nodes)}")
    print(f"  Modified nodes: {len(changes.modified_nodes)}")
    print(f"  Added edges: {len(changes.added_edges)}")
    print(f"  Removed edges: {len(changes.removed_edges)}")

    if args.verbose:
        if changes.added_nodes:
            print("\nAdded nodes:")
            for node in changes.added_nodes:
                print(f"  + {node.id}: {node.label}")

        if changes.removed_nodes:
            print("\nRemoved nodes:")
            for node in changes.removed_nodes:
                print(f"  - {node.id}: {node.label}")

        if changes.modified_nodes:
            print("\nModified nodes:")
            for old_node, new_node in changes.modified_nodes:
                print(f"  ~ {old_node.id}: {old_node.label} → {new_node.label}")


def cmd_extract(args):
    """Extract a subgraph."""
    file_path = Path(args.input)
    if not file_path.exists():
        print(f"Error: File '{args.input}' not found", file=sys.stderr)
        sys.exit(1)

    # Parse
    format_name = detect_format(str(file_path))
    parser = get_parser_for_format(format_name)
    input_text = file_path.read_text()
    diagram = parser.parse(input_text)

    # Extract
    try:
        subgraph = DiagramTransforms.extract_subgraph(
            diagram, args.root, max_depth=args.depth
        )
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    # Render
    output_format = args.format or format_name
    renderer = get_renderer_for_format(output_format)
    output_text = renderer.render(subgraph)

    # Write
    if args.output:
        Path(args.output).write_text(output_text)
        print(f"✅ Subgraph extracted to {args.output}")
        print(f"   Extracted {len(subgraph.nodes)} nodes, {len(subgraph.edges)} edges")
    else:
        print(output_text)


def cmd_watch(args):
    """Watch files for changes and auto-convert."""
    import time

    print(f"👀 Watching {args.input} for changes...")
    print(f"   Output: {args.output}")
    print("   Press Ctrl+C to stop")

    input_path = Path(args.input)
    last_mtime = 0

    try:
        while True:
            if input_path.exists():
                current_mtime = input_path.stat().st_mtime
                if current_mtime > last_mtime:
                    last_mtime = current_mtime

                    # Convert
                    try:
                        input_format = detect_format(args.input)
                        output_format = (
                            detect_format(args.output) if args.output else "mermaid"
                        )

                        input_text = input_path.read_text()
                        parser = get_parser_for_format(input_format)
                        diagram = parser.parse(input_text)

                        renderer = get_renderer_for_format(output_format)
                        output_text = renderer.render(diagram)

                        if args.output:
                            Path(args.output).write_text(output_text)
                            print(f"🔄 Converted at {time.strftime('%H:%M:%S')}")
                        else:
                            print(output_text)
                    except Exception as e:
                        print(f"❌ Error: {e}")

            time.sleep(args.interval)
    except KeyboardInterrupt:
        print("\n👋 Stopped watching")


def main():
    """Enhanced CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Idea Junction - Bidirectional Diagramming System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Convert command
    convert_parser = subparsers.add_parser(
        "convert", help="Convert between diagram formats"
    )
    convert_parser.add_argument("input", help="Input file")
    convert_parser.add_argument("-o", "--output", help="Output file (default: stdout)")
    convert_parser.add_argument(
        "--from", dest="from_format", help="Input format (auto-detected if not specified)"
    )
    convert_parser.add_argument(
        "--to", dest="to_format", help="Output format (auto-detected from extension)"
    )
    convert_parser.add_argument(
        "-d",
        "--direction",
        choices=["TD", "LR", "BT", "RL"],
        help="Diagram direction",
    )

    # Validate command
    validate_parser = subparsers.add_parser("validate", help="Validate diagram files")
    validate_parser.add_argument("files", nargs="+", help="Files to validate")
    validate_parser.add_argument(
        "--no-orphans", action="store_true", help="Disallow orphaned nodes"
    )
    validate_parser.add_argument(
        "--no-cycles", action="store_true", help="Disallow cycles"
    )
    validate_parser.add_argument(
        "--require-start-end", action="store_true", help="Require START and END nodes"
    )
    validate_parser.add_argument("--max-nodes", type=int, help="Maximum node count")
    validate_parser.add_argument("--max-edges", type=int, help="Maximum edge count")

    # Stats command
    stats_parser = subparsers.add_parser("stats", help="Show diagram statistics")
    stats_parser.add_argument("file", help="Diagram file")

    # Simplify command
    simplify_parser = subparsers.add_parser("simplify", help="Simplify a diagram")
    simplify_parser.add_argument("input", help="Input file")
    simplify_parser.add_argument("-o", "--output", help="Output file")
    simplify_parser.add_argument("--format", help="Output format")
    simplify_parser.add_argument(
        "--keep-isolated", action="store_true", help="Keep isolated nodes"
    )

    # Diff command
    diff_parser = subparsers.add_parser("diff", help="Compare two diagrams")
    diff_parser.add_argument("file1", help="First diagram")
    diff_parser.add_argument("file2", help="Second diagram")
    diff_parser.add_argument("-v", "--verbose", action="store_true", help="Show details")

    # Extract command
    extract_parser = subparsers.add_parser("extract", help="Extract a subgraph")
    extract_parser.add_argument("input", help="Input file")
    extract_parser.add_argument("root", help="Root node ID")
    extract_parser.add_argument("-o", "--output", help="Output file")
    extract_parser.add_argument("--format", help="Output format")
    extract_parser.add_argument("--depth", type=int, help="Maximum depth")

    # Watch command
    watch_parser = subparsers.add_parser(
        "watch", help="Watch file for changes and auto-convert"
    )
    watch_parser.add_argument("input", help="Input file to watch")
    watch_parser.add_argument("-o", "--output", help="Output file")
    watch_parser.add_argument(
        "--interval", type=float, default=1.0, help="Check interval in seconds"
    )

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    # Dispatch to command handlers
    commands = {
        "convert": cmd_convert,
        "validate": cmd_validate,
        "stats": cmd_stats,
        "simplify": cmd_simplify,
        "diff": cmd_diff,
        "extract": cmd_extract,
        "watch": cmd_watch,
    }

    handler = commands.get(args.command)
    if handler:
        try:
            handler(args)
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            if "--debug" in sys.argv:
                raise
            sys.exit(1)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
