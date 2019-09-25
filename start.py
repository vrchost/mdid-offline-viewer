import logging
import webbrowser
from http.server import HTTPServer, SimpleHTTPRequestHandler

PORT = 28800
LOGFILE = 'start.log'


logging.basicConfig(filename=LOGFILE, filemode='w', level=logging.DEBUG)


class Server(HTTPServer):

    def __init__(self, server_address, RequestHandlerClass,
                 bind_and_activate=True):
        super().__init__(server_address, RequestHandlerClass,
                         bind_and_activate)
        self.browser_opened = False

    def service_actions(self):
        if not self.browser_opened:
            webbrowser.open_new(
                'http://%s:%s/presentation/index.html' % self.server_address)
            self.browser_opened = True


class RequestHandler(SimpleHTTPRequestHandler):

    def do_GET(self):
        if self.path == '/exit':
            raise KeyboardInterrupt
        super().do_GET()


def serve(port, server_class=Server, handler_class=RequestHandler):
    server_address = ('localhost', port)
    try:
        logging.debug('Trying to listen on port %s', port)
        httpd = server_class(server_address, handler_class)
    except OSError:
        logging.info('Could not listen on port %s', port)
        return False
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    return True


def start(port):
    print("starting")
    while not serve(port):
        port += 1


if __name__ == '__main__':
    start(PORT)
