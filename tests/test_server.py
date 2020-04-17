from neuron.protobuf import neuron_pb2
from neuron.server import run_server
from neuron.server.server import app

import pytest
import requests
import subprocess
import time


_PACKAGE_NAME = 'neuron.server'
_SERVER_ADDRESS = '127.0.0.1', 8000


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_api_get_not_allowed(client):
    r = client.get('/users/42/snapshots')

    assert r.status_code == 405


def test_api_empty_post(client):
    r = client.post('/users/42/snapshots')

    assert r.status_code == 400


def test_api_post_snapshot(client, tmp_path):
    from neuron.server.server import config_raw_dir
    config_raw_dir(tmp_path)
    request = neuron_pb2.SnapshotInfo()

    user = request.user
    user.user_id = 42
    user.username = 'John'
    user.birthday = 100000
    user.gender = 2

    r = client.post('/users/42/snapshots', data=request.SerializeToString())

    assert r.status_code == 204


def test_cli_unsupported_queue():
    host, port = _SERVER_ADDRESS
    process = subprocess.Popen(
        ['python', '-m', _PACKAGE_NAME, 'run-server',
            '-H', host, '-p', str(port), 'kafka://127.0.0.1:9000'],
        stdout=subprocess.PIPE,
    )

    stdout, _ = process.communicate()

    assert process.returncode != 0
    assert b'Unsupported message queue type.' in stdout


def test_cli_bad_host():
    host, port = _SERVER_ADDRESS
    process = subprocess.Popen(
        ['python', '-m', _PACKAGE_NAME, 'run-server',
            '-H', str(2 ** 32), '-p', str(port), '--print'],
        stdout=subprocess.PIPE,
    )

    stdout, _ = process.communicate()

    assert process.returncode != 0
    assert b'Invalid host' in stdout


def test_cli():
    import signal
    host, port = _SERVER_ADDRESS
    process = subprocess.Popen(
        ['python', '-m', _PACKAGE_NAME, 'run-server',
            '-H', host, '-p', str(port), '--print'],
        stdout=subprocess.PIPE,
    )

    request = neuron_pb2.SnapshotInfo()

    user = request.user
    user.user_id = 42
    user.username = 'John'
    user.birthday = 100000
    user.gender = 2

    data = request.SerializeToString()
    headers = {'Content-Type': 'application/protobuf'}

    time.sleep(0.5)

    response = requests.post(
            f'http://{host}:{port}/users/{request.user.user_id}/snapshots', data=data,
            headers=headers)

    process.send_signal(signal.SIGINT)
    stdout, _ = process.communicate()

    assert process.returncode == 0
    assert b'John' in stdout
