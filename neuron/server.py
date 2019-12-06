from .cli import CommandLineInterface
from .utils.listener import Listener
from datetime import datetime
import pathlib
import struct
import threading


cli = CommandLineInterface()


@cli.command
def run(address, data):
    ip, port = address.split(':')
    address = ip, int(port)
    run_server(address, data)


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
            header = self.connection.receive(20)
            if len(header) == 0:
                return

            user_id, timestamp, thought_len = struct.unpack('<QQI', header)
            thought = receive_bytes(
                self.connection, thought_len).decode('utf-8')

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


def main(argv):
    cli.main()


def signal_handler(sig, frame):
    sys.exit(0)


if __name__ == '__main__':
    import signal
    import sys
    signal.signal(signal.SIGINT, signal_handler)
    sys.exit(main(sys.argv))
