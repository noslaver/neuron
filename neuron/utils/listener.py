from .connection import Connection
import socket


class Listener:
    def __init__(self, port, host='0.0.0.0', backlog=1000, reuseaddr=True):
        self.port = port
        self.host = host
        self.backlog = backlog
        self.reuseaddr = reuseaddr

    def __repr__(self):
        return f'{self.__class__.__name__}' + \
            '(port={self.port}, ' + \
            'host={self.host!r}, ' + \
            'backlog={self.backlog}, ' + \
            'reuseaddr={self.reuseaddr})'

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exception, error, traceback):
        self.stop()

    def start(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if self.reuseaddr:
            server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((self.host, self.port))
        server.listen(self.backlog)

        self.server = server

    def stop(self):
        self.server.close()

    def accept(self):
        client, _ = self.server.accept()
        return Connection(client)
