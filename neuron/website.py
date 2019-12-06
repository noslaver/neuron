import http.server
from functools import wraps
import re

def HandlerFactory(handlers):
    class Handler(http.server.BaseHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            self.handlers = handlers
            super(Handler, self).__init__(*args, **kwargs)

        def do_GET(self):
            for path in self.handlers.keys():
                match = re.search(f'^{path}$', self.path)
                if match:
                    f = self.handlers[path]
                    return_code, body = f(*match.groups())

                    self.send_response(return_code)
                    self.send_header('Content-Type', 'text/html')
                    self.send_header('Content-Length', len(body))
                    self.end_headers()
                    self.wfile.write(body.encode('utf-8'))
                    return

            self.send_response(404)
            self.end_headers()


    return Handler

class Website:
    def __init__(self):
        self.handlers = {}
        pass

    def route(self, path):
        def decorator(f):
            self.handlers[path] = f

            @wraps(f)
            def wrapper(*args, **kwargs):
                return f(*args, **kwargs)
            return wrapper
        return decorator

    def run(self, address):
        HandlerClass = HandlerFactory(self.handlers)
        server = http.server.HTTPServer(address, HandlerClass)
        server.serve_forever()
