import os
import sys
import webbrowser
from http import HTTPStatus
from http.server import HTTPServer, SimpleHTTPRequestHandler
from socketserver import ThreadingMixIn

PORT = 28800

EXIT_PAGE = b"""
<html>
<head>
<title>Viewer</title>
</head>
<body>
<div style="text-align: center; font-size: x-large; margin-top: 5em;">
You may now close this browser window.
</div>
</body>
</html>
"""

INFO = """
Viewer started; a new browser window should have opened automatically.
If it has not, go to %s

Please do not close this window.
"""

INFO_END = """
Viewer exited; you may now close this window.
"""


application_path = None
if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)


class Server(ThreadingMixIn, HTTPServer):

    def __init__(self, server_address, handler_class, bind_and_activate=True):
        HTTPServer.__init__(self, server_address, handler_class, bind_and_activate)
        self.browser_opened = False
        self.daemon_threads = True

    def service_actions(self):
        if not self.browser_opened:
            url = 'http://%s:%s/presentation/index.html' % self.server_address
            webbrowser.open_new(url)
            self.browser_opened = True
            print(INFO % url)
            sys.stdout.flush()


class RequestHandler(SimpleHTTPRequestHandler):

    def __init__(self, *args, directory=None, **kwargs):
        if directory is None and application_path:
            directory = application_path
        super().__init__(*args, directory=directory, **kwargs)

    def exit_page(self):
        self.send_response(HTTPStatus.OK)
        self.end_headers()
        self.wfile.write(EXIT_PAGE)

    def do_GET(self):
        self.path = self.path.rstrip('/')
        if self.path == '/exit':
            self.exit_page()
            self.server.shutdown()
        else:
            super().do_GET()

    def send_head(self):
        if "If-Modified-Since" in self.headers:
            del self.headers["If-Modified-Since"]
        return super().send_head()

    def end_headers(self):
        self.send_header("Cache-Control", "no-cache")
        super().end_headers()

    def log_message(self, format, *args):
        pass


def serve(port, server_class=Server, handler_class=RequestHandler):
    server_address = ('127.0.0.1', port)
    try:
        httpd = server_class(server_address, handler_class)
    except OSError:
        return False
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print(INFO_END)
    return True

def start(port):
    while not serve(port):
        port += 1


if __name__ == '__main__':
    start(PORT)
