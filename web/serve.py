import http.server
import socketserver
import os
import webbrowser

os.chdir(os.path.dirname(__file__))

PORT = 8000

class AliasHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def translate_path(self, path):
        # serve /data/* from ../out/*
        if path.startswith("/data"):
            path = path.replace("data", "../out", 1)
        return super().translate_path(path)

with socketserver.TCPServer(("", PORT), AliasHTTPRequestHandler) as httpd:
    url = f"http://localhost:{PORT}"
    print(f"Serving at {url}")
    # TODO only when not already open
    webbrowser.open(url)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt as e:
        print('Keyboard interrupt received, exiting.')
