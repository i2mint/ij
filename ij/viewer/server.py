"""Web server for interactive diagram viewing."""

import http.server
import json
import socketserver
import threading
import webbrowser
from pathlib import Path
from typing import Optional

from ..core import DiagramIR
from ..renderers import MermaidRenderer


class ViewerHandler(http.server.BaseHTTPRequestHandler):
    """HTTP request handler for viewer."""

    diagram_data = None
    theme = "default"

    def do_GET(self):
        """Handle GET requests."""
        if self.path == "/":
            self.serve_html()
        elif self.path == "/api/diagram":
            self.serve_diagram()
        elif self.path.startswith("/api/"):
            self.serve_api()
        else:
            self.send_error(404)

    def serve_html(self):
        """Serve the main HTML page."""
        html = self.get_viewer_html()
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(html.encode())

    def serve_diagram(self):
        """Serve diagram data."""
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()

        data = {
            "diagram": self.diagram_data,
            "theme": self.theme,
        }
        self.wfile.write(json.dumps(data).encode())

    def serve_api(self):
        """Serve API endpoints."""
        # Could add more API endpoints here
        self.send_error(404)

    def get_viewer_html(self) -> str:
        """Generate viewer HTML."""
        return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>IJ Diagram Viewer</title>
    <script type="module">
        import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';

        async function loadDiagram() {
            try {
                const response = await fetch('/api/diagram');
                const data = await response.json();

                mermaid.initialize({
                    startOnLoad: true,
                    theme: data.theme || 'default',
                    securityLevel: 'loose',
                });

                const container = document.getElementById('diagram-container');
                container.innerHTML = '<div class="mermaid">' + data.diagram + '</div>';

                await mermaid.run({
                    querySelector: '.mermaid'
                });

            } catch (error) {
                console.error('Error loading diagram:', error);
                document.getElementById('diagram-container').innerHTML =
                    '<div class="error">Error loading diagram: ' + error.message + '</div>';
            }
        }

        window.addEventListener('DOMContentLoaded', loadDiagram);

        // Auto-refresh every 2 seconds
        setInterval(loadDiagram, 2000);
    </script>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
        }

        header {
            background: rgba(255, 255, 255, 0.95);
            padding: 1rem 2rem;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        }

        h1 {
            color: #333;
            font-size: 1.5rem;
            font-weight: 600;
        }

        .subtitle {
            color: #666;
            font-size: 0.875rem;
            margin-top: 0.25rem;
        }

        main {
            flex: 1;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 2rem;
        }

        #diagram-container {
            background: white;
            border-radius: 12px;
            padding: 2rem;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            max-width: 95%;
            max-height: 85vh;
            overflow: auto;
        }

        .mermaid {
            display: flex;
            justify-content: center;
            align-items: center;
        }

        .error {
            color: #e53e3e;
            padding: 2rem;
            text-align: center;
        }

        .controls {
            position: fixed;
            bottom: 2rem;
            right: 2rem;
            display: flex;
            gap: 0.5rem;
            z-index: 1000;
        }

        .control-btn {
            background: white;
            border: none;
            padding: 0.75rem 1.5rem;
            border-radius: 8px;
            cursor: pointer;
            font-size: 0.875rem;
            font-weight: 500;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
            transition: all 0.2s;
        }

        .control-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 16px rgba(0, 0, 0, 0.2);
        }

        footer {
            background: rgba(255, 255, 255, 0.1);
            color: white;
            text-align: center;
            padding: 1rem;
            font-size: 0.875rem;
        }
    </style>
</head>
<body>
    <header>
        <h1>🎨 IJ Diagram Viewer</h1>
        <div class="subtitle">Interactive diagram visualization • Live updates</div>
    </header>

    <main>
        <div id="diagram-container">
            <div class="mermaid">Loading diagram...</div>
        </div>
    </main>

    <div class="controls">
        <button class="control-btn" onclick="location.reload()">🔄 Refresh</button>
        <button class="control-btn" onclick="window.print()">🖨️ Print</button>
    </div>

    <footer>
        Powered by Idea Junction (ij) • Press Ctrl+C in terminal to stop server
    </footer>
</body>
</html>"""

    def log_message(self, format, *args):
        """Suppress default logging."""
        pass  # Silent mode


class ViewerServer:
    """Interactive web server for diagram viewing."""

    def __init__(self, port: int = 8080, theme: str = "default"):
        """Initialize viewer server.

        Args:
            port: Port to run server on
            theme: Mermaid theme ('default', 'dark', 'forest', 'neutral')
        """
        self.port = port
        self.theme = theme
        self.server: Optional[socketserver.TCPServer] = None
        self.thread: Optional[threading.Thread] = None

    def start(self, diagram: DiagramIR, open_browser: bool = True):
        """Start the viewer server.

        Args:
            diagram: DiagramIR to display
            open_browser: Whether to open browser automatically

        Example:
            >>> server = ViewerServer(port=8080)
            >>> server.start(diagram)
            Server running at http://localhost:8080
            Press Ctrl+C to stop
        """
        # Render diagram to Mermaid
        renderer = MermaidRenderer()
        mermaid_code = renderer.render(diagram)

        # Set class variables for handler
        ViewerHandler.diagram_data = mermaid_code
        ViewerHandler.theme = self.theme

        # Create server
        try:
            self.server = socketserver.TCPServer(("", self.port), ViewerHandler)
        except OSError as e:
            if "Address already in use" in str(e):
                print(f"⚠️  Port {self.port} is already in use. Try a different port.")
                return
            raise

        url = f"http://localhost:{self.port}"
        print(f"🚀 Server running at {url}")
        print(f"📊 Viewing diagram with {len(diagram.nodes)} nodes, {len(diagram.edges)} edges")
        print("🔄 Auto-refresh enabled (updates every 2 seconds)")
        print("⏹️  Press Ctrl+C to stop\n")

        # Open browser
        if open_browser:
            threading.Timer(0.5, lambda: webbrowser.open(url)).start()

        # Start server in thread
        self.thread = threading.Thread(target=self.server.serve_forever)
        self.thread.daemon = True
        self.thread.start()

        try:
            # Keep main thread alive
            self.thread.join()
        except KeyboardInterrupt:
            self.stop()

    def stop(self):
        """Stop the server."""
        if self.server:
            print("\n👋 Stopping server...")
            self.server.shutdown()
            self.server.server_close()
            print("✅ Server stopped")

    def update_diagram(self, diagram: DiagramIR):
        """Update the displayed diagram.

        Args:
            diagram: New DiagramIR to display
        """
        renderer = MermaidRenderer()
        mermaid_code = renderer.render(diagram)
        ViewerHandler.diagram_data = mermaid_code


def serve_diagram(
    diagram: DiagramIR,
    port: int = 8080,
    theme: str = "default",
    open_browser: bool = True,
):
    """Quickly serve a diagram in browser.

    Args:
        diagram: DiagramIR to display
        port: Port number
        theme: Mermaid theme
        open_browser: Whether to open browser

    Example:
        >>> from ij import DiagramIR, Node, Edge
        >>> diagram = DiagramIR()
        >>> # ... build diagram ...
        >>> serve_diagram(diagram)
    """
    server = ViewerServer(port=port, theme=theme)
    server.start(diagram, open_browser=open_browser)
