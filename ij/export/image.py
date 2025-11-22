"""Image export functionality for diagrams.

Supports exporting diagrams to SVG and PNG formats.
"""

import subprocess
import tempfile
from pathlib import Path
from typing import Literal, Optional

from ..core import DiagramIR
from ..renderers import GraphvizRenderer, MermaidRenderer


class ImageExporter:
    """Export diagrams to image formats."""

    def __init__(
        self,
        format: Literal["svg", "png", "pdf"] = "svg",
        engine: Literal["mermaid-cli", "playwright", "graphviz"] = "mermaid-cli",
    ):
        """Initialize image exporter.

        Args:
            format: Output format ('svg', 'png', 'pdf')
            engine: Rendering engine to use

        Note:
            Requires external tools:
            - mermaid-cli: npm install -g @mermaid-js/mermaid-cli
            - playwright: pip install playwright && playwright install
            - graphviz: System package (apt install graphviz, brew install graphviz)
        """
        self.format = format
        self.engine = engine

    def render(
        self,
        diagram: DiagramIR,
        output_path: str,
        width: Optional[int] = None,
        height: Optional[int] = None,
        background: str = "white",
        theme: str = "default",
    ) -> bool:
        """Render diagram to image file.

        Args:
            diagram: DiagramIR to render
            output_path: Output file path
            width: Image width in pixels (optional)
            height: Image height in pixels (optional)
            background: Background color
            theme: Diagram theme ('default', 'dark', 'forest', 'neutral')

        Returns:
            True if successful, False otherwise

        Example:
            >>> exporter = ImageExporter(format='png', engine='mermaid-cli')
            >>> success = exporter.render(diagram, 'output.png', width=800)
        """
        if self.engine == "graphviz":
            return self._render_graphviz(diagram, output_path)
        elif self.engine == "mermaid-cli":
            return self._render_mermaid_cli(
                diagram, output_path, width, height, background, theme
            )
        elif self.engine == "playwright":
            return self._render_playwright(
                diagram, output_path, width, height, background, theme
            )
        else:
            raise ValueError(f"Unknown rendering engine: {self.engine}")

    def _render_graphviz(self, diagram: DiagramIR, output_path: str) -> bool:
        """Render using Graphviz."""
        try:
            # Render to DOT format
            renderer = GraphvizRenderer()
            dot_code = renderer.render(diagram)

            # Determine format
            format_map = {"svg": "svg", "png": "png", "pdf": "pdf"}
            output_format = format_map.get(self.format, "svg")

            # Create temporary DOT file
            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".dot", delete=False
            ) as f:
                f.write(dot_code)
                dot_file = f.name

            # Run Graphviz
            result = subprocess.run(
                ["dot", f"-T{output_format}", dot_file, "-o", output_path],
                capture_output=True,
                text=True,
            )

            # Clean up
            Path(dot_file).unlink()

            if result.returncode == 0:
                return True
            else:
                print(f"Graphviz error: {result.stderr}")
                return False

        except FileNotFoundError:
            print(
                "Error: Graphviz not found. Install with: apt install graphviz or brew install graphviz"
            )
            return False
        except Exception as e:
            print(f"Error rendering with Graphviz: {e}")
            return False

    def _render_mermaid_cli(
        self,
        diagram: DiagramIR,
        output_path: str,
        width: Optional[int],
        height: Optional[int],
        background: str,
        theme: str,
    ) -> bool:
        """Render using Mermaid CLI (mmdc)."""
        try:
            # Render to Mermaid format
            renderer = MermaidRenderer()
            mermaid_code = renderer.render(diagram)

            # Create temporary Mermaid file
            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".mmd", delete=False
            ) as f:
                f.write(mermaid_code)
                mmd_file = f.name

            # Build mmdc command
            cmd = ["mmdc", "-i", mmd_file, "-o", output_path]

            if theme != "default":
                cmd.extend(["-t", theme])

            if background:
                cmd.extend(["-b", background])

            if width:
                cmd.extend(["-w", str(width)])

            if height:
                cmd.extend(["-H", str(height)])

            # Run Mermaid CLI
            result = subprocess.run(cmd, capture_output=True, text=True)

            # Clean up
            Path(mmd_file).unlink()

            if result.returncode == 0:
                return True
            else:
                print(f"Mermaid CLI error: {result.stderr}")
                return False

        except FileNotFoundError:
            print(
                "Error: Mermaid CLI not found. Install with: npm install -g @mermaid-js/mermaid-cli"
            )
            return False
        except Exception as e:
            print(f"Error rendering with Mermaid CLI: {e}")
            return False

    def _render_playwright(
        self,
        diagram: DiagramIR,
        output_path: str,
        width: Optional[int],
        height: Optional[int],
        background: str,
        theme: str,
    ) -> bool:
        """Render using Playwright (headless browser)."""
        try:
            from playwright.sync_api import sync_playwright
        except ImportError:
            print(
                "Error: Playwright not installed. Install with: pip install playwright && playwright install"
            )
            return False

        try:
            # Render to Mermaid format
            renderer = MermaidRenderer()
            mermaid_code = renderer.render(diagram)

            # Create HTML with Mermaid
            html_content = self._create_mermaid_html(mermaid_code, theme, background)

            # Use Playwright to render
            with sync_playwright() as p:
                browser = p.chromium.launch()
                page = browser.new_page()

                if width and height:
                    page.set_viewport_size({"width": width, "height": height})

                # Load HTML
                page.set_content(html_content)

                # Wait for Mermaid to render
                page.wait_for_selector(".mermaid svg", timeout=5000)

                # Take screenshot
                if self.format == "png":
                    page.screenshot(path=output_path, full_page=True)
                elif self.format == "pdf":
                    page.pdf(path=output_path)
                else:  # SVG - extract the rendered SVG
                    svg_content = page.eval_on_selector(".mermaid svg", "el => el.outerHTML")
                    Path(output_path).write_text(svg_content)

                browser.close()

            return True

        except Exception as e:
            print(f"Error rendering with Playwright: {e}")
            return False

    def _create_mermaid_html(
        self, mermaid_code: str, theme: str, background: str
    ) -> str:
        """Create HTML page with Mermaid diagram."""
        return f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <script type="module">
        import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
        mermaid.initialize({{
            startOnLoad: true,
            theme: '{theme}',
            themeCSS: 'background-color: {background};'
        }});
    </script>
    <style>
        body {{
            margin: 0;
            padding: 20px;
            background-color: {background};
        }}
        .mermaid {{
            text-align: center;
        }}
    </style>
</head>
<body>
    <div class="mermaid">
{mermaid_code}
    </div>
</body>
</html>"""

    def check_dependencies(self) -> dict:
        """Check which rendering engines are available.

        Returns:
            Dictionary of engine availability

        Example:
            >>> exporter = ImageExporter()
            >>> available = exporter.check_dependencies()
            >>> if available['graphviz']:
            ...     print("Graphviz is installed")
        """
        available = {}

        # Check Graphviz
        try:
            result = subprocess.run(
                ["dot", "-V"], capture_output=True, text=True, timeout=5
            )
            available["graphviz"] = result.returncode == 0
        except (FileNotFoundError, subprocess.TimeoutExpired):
            available["graphviz"] = False

        # Check Mermaid CLI
        try:
            result = subprocess.run(
                ["mmdc", "--version"], capture_output=True, text=True, timeout=5
            )
            available["mermaid-cli"] = result.returncode == 0
        except (FileNotFoundError, subprocess.TimeoutExpired):
            available["mermaid-cli"] = False

        # Check Playwright
        try:
            import playwright

            available["playwright"] = True
        except ImportError:
            available["playwright"] = False

        return available


def quick_export(
    diagram: DiagramIR,
    output_path: str,
    format: str = "svg",
    engine: Optional[str] = None,
) -> bool:
    """Quick export diagram to image.

    Args:
        diagram: DiagramIR to export
        output_path: Output file path
        format: Image format ('svg', 'png', 'pdf')
        engine: Rendering engine (auto-detected if None)

    Returns:
        True if successful

    Example:
        >>> from ij import DiagramIR, Node, Edge
        >>> diagram = DiagramIR()
        >>> # ... build diagram ...
        >>> quick_export(diagram, 'diagram.png', format='png')
    """
    # Auto-detect engine if not specified
    if engine is None:
        exporter = ImageExporter(format=format)
        available = exporter.check_dependencies()

        if available.get("graphviz"):
            engine = "graphviz"
        elif available.get("mermaid-cli"):
            engine = "mermaid-cli"
        elif available.get("playwright"):
            engine = "playwright"
        else:
            print("Error: No rendering engines available")
            print("Install one of:")
            print("  - Graphviz: apt install graphviz / brew install graphviz")
            print("  - Mermaid CLI: npm install -g @mermaid-js/mermaid-cli")
            print("  - Playwright: pip install playwright && playwright install")
            return False

    exporter = ImageExporter(format=format, engine=engine)
    return exporter.render(diagram, output_path)
