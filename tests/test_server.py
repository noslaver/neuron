from neuron.protobuf import neuron_pb2
from neuron.server import run_server
from neuron.server.server import app

import pytest
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


def test_api_post_snapshot(client):
    request = neuron_pb2.SnapshotInfo()

    user = request.user
    user.user_id = 42
    user.username = 'John'
    user.birthday = 100000
    user.gender = 2

    r = client.post('/users/42/snapshots', data=request.SerializeToString())

    assert r.status_code == 204


def test_cli():
    pass


def test_cli_server_error():
    pass


def test_cli_bad_sample(tmp_path):
    pass
