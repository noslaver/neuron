from neuron.parsers import parse
from collections import namedtuple
import json
import pytest
import subprocess


_PACKAGE_NAME = 'neuron.parsers'
_SNAPSHOT_PATH = 'tests/snapshot_info.json'


@pytest.fixture
def raw_snapshot():
    with open(_SNAPSHOT_PATH, 'r') as reader:
        yield json.loads(reader.read(), object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))


def test_pose_parser(raw_snapshot):
    result = parse('pose', raw_snapshot)

    user = result['metadata']['user']

    assert user['id'] == '42'
    assert user['name'] == 'John Smith'
    assert user['gender'] == 'Male'

    translation = result['data']['translation']

    assert translation['x'] == 0.487
    assert translation['y'] == 0.007
    assert translation['z'] == -1.13

    rotation = result['data']['rotation']

    assert rotation['x'] == -0.108
    assert rotation['y'] == -0.267
    assert rotation['z'] == -0.021
    assert rotation['w'] == 0.957


def test_feelings_parser(raw_snapshot):
    result = parse('feelings', raw_snapshot)

    user = result['metadata']['user']

    assert user['id'] == '42'
    assert user['name'] == 'John Smith'
    assert user['gender'] == 'Male'

    feelings = result['data']

    assert feelings['hunger'] == 0.5
    assert feelings['thirst'] == 0.6
    assert feelings['exhaustion'] == 0.7
    assert feelings['happiness'] == 0.8


def test_color_image_parser(raw_snapshot):
    result = parse('color_image', raw_snapshot)

    user = result['metadata']['user']

    assert user['id'] == '42'
    assert user['name'] == 'John Smith'
    assert user['gender'] == 'Male'

    assert result['data']['parsed_image_path'] == 'data/42/2019-12-04_08-08-07-339000/color_image.jpg'


def test_depth_image_parser(raw_snapshot):
    result = parse('depth_image', raw_snapshot)

    user = result['metadata']['user']

    assert user['id'] == '42'
    assert user['name'] == 'John Smith'
    assert user['gender'] == 'Male'

    assert result['data']['parsed_image_path'] == 'data/42/2019-12-04_08-08-07-339000/depth_image.png'


def test_cli_unsupprted_queue(tmp_path):
    bad_sample = tmp_path / 'snapshot.json'
    bad_sample.write_text('not json')

    process = subprocess.Popen(
            ['python', '-m', _PACKAGE_NAME, 'run-parser', 'pose', 'kafka://127.0.0.1:90'],
        stdout=subprocess.PIPE,
    )

    stdout, stderr = process.communicate()

    assert b'Unsupported message queue type.' in stdout
    assert process.returncode != 0


def test_cli_bad_json(tmp_path):
    bad_sample = tmp_path / 'snapshot.json'
    bad_sample.write_text('not json')

    process = subprocess.Popen(
        ['python', '-m', _PACKAGE_NAME, 'parse', 'pose', bad_sample],
        stdout=subprocess.PIPE,
    )

    stdout, stderr = process.communicate()

    assert b'An error occurred' in stdout
    assert b'Bad JSON' in stdout
    assert process.returncode != 0


def test_cli_bad_snapshot(tmp_path):
    bad_sample = tmp_path / 'snapshot.json'
    bad_sample.write_text('{}')

    process = subprocess.Popen(
        ['python', '-m', _PACKAGE_NAME, 'parse', 'pose', bad_sample],
        stdout=subprocess.PIPE,
    )

    stdout, stderr = process.communicate()

    assert b'An error occurred' in stdout
    assert b'Failed to parse' in stdout
    assert process.returncode != 0


def test_cli():
    process = subprocess.Popen(
        ['python', '-m', _PACKAGE_NAME, 'parse', 'pose', _SNAPSHOT_PATH],
        stdout=subprocess.PIPE,
    )

    stdout, stderr = process.communicate()

    assert process.returncode == 0
    assert not stderr

    result = json.loads(stdout)

    user = result['metadata']['user']

    assert user['id'] == '42'
    assert user['name'] == 'John Smith'
    assert user['gender'] == 'Male'

    translation = result['data']['translation']

    assert translation['x'] == 0.487
    assert translation['y'] == 0.007
    assert translation['z'] == -1.13

    rotation = result['data']['rotation']

    assert rotation['x'] == -0.108
    assert rotation['y'] == -0.267
    assert rotation['z'] == -0.021
    assert rotation['w'] == 0.957
