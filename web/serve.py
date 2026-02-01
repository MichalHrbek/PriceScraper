import http.server
import socketserver
import os
import webbrowser

os.chdir(os.path.dirname(__file__))

PORT = 8000

class AliasHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def translate_path(self, path):
        # serve /data/* from ../out/*
        # Unsafe - don't expose on public networks
        if path.startswith('/data/'):
            relative_path = path.removeprefix('/data/')
            out_dir = os.path.abspath(os.path.join(os.getcwd(), '..', 'out'))
            return os.path.join(out_dir, relative_path)
        
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
