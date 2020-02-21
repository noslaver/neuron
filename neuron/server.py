from .utils.listener import Listener
from datetime import datetime
import pathlib
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

    def __init__(self, connection, data_dir):
        super().__init__()
        self.connection = connection
        self.data_dir = data_dir

    def run(self):
        self.handle_client()

    def handle_client(self):
        while True:
            msg = self.connection.receive()
            if len(msg) == 0:
                return

            user_id, timestamp = struct.unpack('<QQ', msg[:16])
            thought = msg[16:]

            timestamp = datetime.fromtimestamp(
                timestamp).strftime('%Y-%m-%d_%H-%M-%S')

            out_dir = pathlib.Path(self.data_dir) / str(user_id)
            out_dir.mkdir(parents=True, exist_ok=True)

            out_file = out_dir / f'{timestamp}.txt'
            out_file.touch(exist_ok=True)

            self.lock.acquire()
            all_messages = out_file.read_text()
            if len(all_messages) == 0:
                all_messages = thought
            else:
                all_messages += '\n' + thought
            out_file.write_text(all_messages)
            self.lock.release()


def signal_handler(sig, frame):
    sys.exit(0)


if __name__ == '__main__':
    import signal
    import sys
    signal.signal(signal.SIGINT, signal_handler)
