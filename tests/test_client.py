from neuron.client import upload_sample
from neuron.client.reader import Reader

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

def test_api():
    host, port = _SERVER_ADDRESS
    upload_sample(host, port, _SAMPLE_PATH)

def test_cli():
    time.sleep(0.1)
    host, port = _SERVER_ADDRESS
    process = subprocess.Popen(
        ['python', '-m', _PACKAGE_NAME, 'upload-sample',
            '-H', host, '-p', str(port), _SAMPLE_PATH],
        stdout=subprocess.PIPE,
    )

    stdout, stderr = process.communicate()

    assert not stdout
    assert not stderr
