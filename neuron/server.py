from .parsers import Parsers
from .protocol import Config, Hello, Snapshot
from .utils.listener import Listener
from datetime import datetime
from pathlib import Path
import struct
import threading


def run_server(address, data_dir):
    listener = Listener(address[1], address[0], 1, True)
    listener.start()

    while True:
        client = listener.accept()
        handler = Handler(client, data_dir)
        handler.start()


class Handler(threading.Thread):
    lock = threading.Lock()

    config = Config(Parsers.parsers.keys())

    def __init__(self, connection, data_dir):
        super().__init__()
        self.connection = connection
        self.data_dir = data_dir

    def run(self):
        self.handle_client()

    def handle_client(self):
        msg = self.connection.receive_message()
        if len(msg) == 0:
            return

        hello = Hello.deserialize(msg)

        self.connection.send_message(self.config.serialize())

        msg = self.connection.receive_message()
        snapshot = Snapshot.deserialize(msg)
        print(snapshot)

        directory = Path(self.data_dir) / str(hello.user_id) / snapshot.timestamp.strftime('%Y-%m-%d_%H-%M-%S-%f')
        directory.mkdir(parents=True, exist_ok=True)

        for parser in Parsers.parsers.values():
            parser(Parsers.parse_context(directory), snapshot)

        Parsers


def signal_handler(sig, frame):
    sys.exit(0)


if __name__ == '__main__':
    import signal
    import sys
    signal.signal(signal.SIGINT, signal_handler)
