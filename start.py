import webbrowser
from http.server import HTTPServer, SimpleHTTPRequestHandler


PORT = 28800


class Server(HTTPServer):

    def __init__(self, server_address, handler_class, bind_and_activate=True):
        super().__init__(server_address, handler_class, bind_and_activate)
        self.browser_opened = False

    def service_actions(self):
        if not self.browser_opened:
            url = 'http://%s:%s/presentation/index.html' % self.server_address
            webbrowser.open_new(url)
            self.browser_opened = True


class RequestHandler(SimpleHTTPRequestHandler):

    def do_GET(self):
        if self.path == '/exit':
            raise KeyboardInterrupt
        super().do_GET()


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
    return True


def start(port):
    while not serve(port):
        port += 1


if __name__ == '__main__':
    start(PORT)
