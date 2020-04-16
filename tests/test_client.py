from neuron.client import upload_sample
from neuron.client.reader import Reader

import pytest
import requests
import subprocess
import time

_PACKAGE_NAME = 'neuron.client'
_SERVER_ADDRESS = '127.0.0.1', 8000
_SAMPLE_PATH = 'tests/sample.mind.gz'

def test_reader():
    reader = Reader(_SAMPLE_PATH, 'protobuf')

    snapshots = list(reader.read())

    assert reader.user.username == 'John Smith'
    assert reader.user.user_id == 42

    assert len(snapshots) == 1


@pytest.fixture
def mock_response(monkeypatch):
    def mock_post(url, data, headers):
        return MockResponse()
    monkeypatch.setattr(requests, 'post', mock_post)


class MockResponse:
    def __init__(self):
        self.status_code = 204


def test_api(mock_response):
    host, port = _SERVER_ADDRESS
    upload_sample(host, port, _SAMPLE_PATH)


def test_cli():
    host, port = _SERVER_ADDRESS
    server = subprocess.Popen(
        ['python', '-m', 'http.server', str(port), '--bind', host],
        stdout=subprocess.PIPE,
    )
    try:
        time.sleep(0.1)
        process = subprocess.Popen(
            ['python', '-m', _PACKAGE_NAME, 'upload-sample',
                '-H', host, '-p', str(port), _SAMPLE_PATH],
            stdout=subprocess.PIPE,
        )
        time.sleep(0.5)

        stdout, stderr = process.communicate()

        assert b'Uploading snapshot #1' in stdout
        assert not stderr
    finally:
        server.terminate()

def test_cli_error():
    host, port = _SERVER_ADDRESS
    process = subprocess.Popen(
        ['python', '-m', _PACKAGE_NAME, 'upload-sample',
            '-H', host, '-p', str(port), _SAMPLE_PATH],
        stdout=subprocess.PIPE,
    )
    time.sleep(0.2)

    stdout, stderr = process.communicate()

    assert b'Failed to connect to server' in stdout
    assert process.returncode != 0
