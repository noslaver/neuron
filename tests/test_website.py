import multiprocessing
import pathlib
import time
import requests

from neuron import run_webserver


_ADDRESS = '127.0.0.1', 8000
_URL = f'http://{_ADDRESS[0]}:{_ADDRESS[1]}'
_ROOT = pathlib.Path(__file__).absolute().parent.parent
_WEBSERVER_PATH = _ROOT / 'web.py'
_DATA_DIR = _ROOT / 'data'


def test_web():
    process = multiprocessing.Process(target=run)
    process.start()
    time.sleep(1)
    try:
        response = requests.get(_URL)
        for user_dir in _DATA_DIR.iterdir():
            assert f'user {user_dir.name}' in response.text
        for user_dir in _DATA_DIR.iterdir():
            response = requests.get(f'{_URL}/users/{user_dir.name}')
            assert f'User {user_dir.name}' in response.text
            for thought_file in user_dir.iterdir():
                assert thought_file.read_text() in response.text
    finally:
        process.terminate()


def run():
    run_webserver(_ADDRESS, _DATA_DIR)
