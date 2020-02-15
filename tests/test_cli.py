import multiprocessing
import pathlib
import signal
import socket
import subprocess
import threading
import time


_PACKAGE_NAME = 'neuron'
_SERVER_ADDRESS = '127.0.0.1', 5000
_SERVER_BACKLOG = 1000
_ROOT = pathlib.Path(__file__).absolute().parent.parent


def test_client():
    server = multiprocessing.Process(target=run_server)
    server.start()
    try:
        time.sleep(0.1)
        host, port = _SERVER_ADDRESS
        process = subprocess.Popen(
            ['python', '-m', _PACKAGE_NAME, 'upload',
                f'{host}:{port}', f'1', f"I'm hungry"],
            stdout=subprocess.PIPE,
        )
        stdout, _ = process.communicate()
        assert b'done' in stdout.lower()
    finally:
        server.terminate()


def run_server():
    server = socket.socket()
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(_SERVER_ADDRESS)
    server.listen(_SERVER_BACKLOG)
    try:
        while True:
            connection, address = server.accept()
            connection.close()
    except KeyboardInterrupt:
        pass
    finally:
        server.close()


def test_server():
    host, port = _SERVER_ADDRESS
    process = subprocess.Popen(
        ['python', '-m', _PACKAGE_NAME, 'run',
            f'{host}:{port}', 'data/'],
        stdout=subprocess.PIPE,
    )
    thread = threading.Thread(target=process.communicate)
    thread.start()
    time.sleep(0.5)
    try:
        connection = socket.socket()
        connection.connect(_SERVER_ADDRESS)
        connection.close()
    finally:
        process.send_signal(signal.SIGINT)
        thread.join()
