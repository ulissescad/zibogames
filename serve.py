#!/usr/bin/env python3
"""Local test server for the Godot Web export.

Serves ./build/web with the COOP/COEP headers needed for cross-origin isolation
(required only if you enabled Thread Support in the export) plus correct MIME
types for .wasm / .pck. You cannot just open index.html via file:// — the game
needs to be served over http.

Usage:
    python serve.py [port]        # default 8000
Then open http://localhost:8000
"""
import http.server
import socketserver
import sys
import os

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
DIRECTORY = os.path.join(os.path.dirname(__file__), "..", "build", "web")


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def end_headers(self):
        self.send_header("Cross-Origin-Opener-Policy", "same-origin")
        self.send_header("Cross-Origin-Embedder-Policy", "require-corp")
        super().end_headers()


Handler.extensions_map.update({
    ".wasm": "application/wasm",
    ".pck": "application/octet-stream",
    ".js": "text/javascript",
})

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("Servindo %s em http://localhost:%d" % (os.path.abspath(DIRECTORY), PORT))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nParado.")
