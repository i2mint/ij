# ij.viewer.server

Web server for interactive diagram viewing.

### Functions

| [`serve_diagram`](#ij.viewer.server.serve_diagram)(diagram[, port, theme, ...])   | Quickly serve a diagram in browser.   |
|-----------------------------------------------------------------------------------------------|---------------------------------------|

### Classes

| [`ViewerHandler`](#ij.viewer.server.ViewerHandler)(request, client_address, server)   | HTTP request handler for viewer.            |
|---------------------------------------------------------------------------------------------------|---------------------------------------------|
| [`ViewerServer`](#ij.viewer.server.ViewerServer)([port, theme])                      | Interactive web server for diagram viewing. |

### *class* ij.viewer.server.ViewerHandler(request, client_address, server)

Bases: [`BaseHTTPRequestHandler`](https://docs.python.org/3/library/http.server.html#http.server.BaseHTTPRequestHandler)

HTTP request handler for viewer.

#### do_GET()

Handle GET requests.

#### get_viewer_html()

Generate viewer HTML.

* **Return type:**
  [`str`](https://docs.python.org/3/builtins/stdtypes.html#str)

#### log_message(format, \*args)

Suppress default logging.

#### serve_api()

Serve API endpoints.

#### serve_diagram()

Serve diagram data.

#### serve_html()

Serve the main HTML page.

### *class* ij.viewer.server.ViewerServer(port=8080, theme='default')

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

Interactive web server for diagram viewing.

#### start(diagram, open_browser=True)

Start the viewer server.

* **Parameters:**
  * **diagram** ([`DiagramIR`](ij.core.md#ij.core.DiagramIR)) – DiagramIR to display
  * **open_browser** ([`bool`](https://docs.python.org/3/builtins/functions.html#bool)) – Whether to open browser automatically

### Example

```pycon
>>> server = ViewerServer(port=8080)
>>> server.start(diagram)
Server running at http://localhost:8080
Press Ctrl+C to stop
```

#### stop()

Stop the server.

#### update_diagram(diagram)

Update the displayed diagram.

* **Parameters:**
  **diagram** ([`DiagramIR`](ij.core.md#ij.core.DiagramIR)) – New DiagramIR to display

### ij.viewer.server.serve_diagram(diagram, port=8080, theme='default', open_browser=True)

Quickly serve a diagram in browser.

* **Parameters:**
  * **diagram** ([`DiagramIR`](ij.core.md#ij.core.DiagramIR)) – DiagramIR to display
  * **port** ([`int`](https://docs.python.org/3/builtins/functions.html#int)) – Port number
  * **theme** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Mermaid theme
  * **open_browser** ([`bool`](https://docs.python.org/3/builtins/functions.html#bool)) – Whether to open browser

### Example

```pycon
>>> from ij import DiagramIR, Node, Edge
>>> diagram = DiagramIR()
>>> # ... build diagram ...
>>> serve_diagram(diagram)
```
