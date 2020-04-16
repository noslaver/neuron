from neuron.client import upload_sample
from neuron.client.reader import Reader

import pytest
import subprocess
import time

_PACKAGE_NAME = 'neuron.client'
_SERVER_ADDRESS = '127.0.0.1', 8000
_SAMPLE_PATH = 'tests/sample.mind.gz'
_SAMPLE_PATH_BINARY = 'tests/sample.mind'

def test_reader_protobuf():
    reader = Reader(_SAMPLE_PATH, 'protobuf')

    snapshots = list(reader.read())

    assert reader.user.username == 'John Smith'
    assert reader.user.user_id == 42

    assert len(snapshots) == 1


def test_reader_binary():
    reader = Reader(_SAMPLE_PATH_BINARY, 'binary')

    snapshots = list(reader.read())

    assert reader.user.username == 'John Smith'
    assert reader.user.user_id == 42

    assert len(snapshots) == 1


@pytest.fixture
def mock_response(monkeypatch):
    def mock_post(url, data, headers):
        return MockResponse()
    import requests
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

        stdout, stderr = process.communicate()

        assert b'Uploading snapshot #1' in stdout
        assert not stderr
    finally:
        server.terminate()


def test_cli_server_error():
    host, port = _SERVER_ADDRESS
    process = subprocess.Popen(
        ['python', '-m', _PACKAGE_NAME, 'upload-sample',
            '-H', host, '-p', str(port), _SAMPLE_PATH],
        stdout=subprocess.PIPE,
    )

    stdout, stderr = process.communicate()

    assert b'Failed to connect to server' in stdout
    assert process.returncode != 0


def test_cli_bad_sample(tmp_path):
    bad_sample = tmp_path / 'sample.mind.gz'
    bad_sample.write_text('content')

    host, port = _SERVER_ADDRESS
    process = subprocess.Popen(
        ['python', '-m', _PACKAGE_NAME, 'upload-sample',
            '-H', host, '-p', str(port), bad_sample],
        stdout=subprocess.PIPE,
    )

    stdout, stderr = process.communicate()

    assert b'An error occurred' in stdout
    assert process.returncode != 0
