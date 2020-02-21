import datetime as dt

import pytest

from neuron.protocol import Hello, Config


user_id = 1
datetime = dt.datetime(2000, 1, 1, 12, 0)
username = "Allen"
gender = 'm'
serialized = b"\x01\x00\x00\x00\x00\x00\x00\x00\x05\x00\x00\x00Allen@\xecm8m"


@pytest.fixture
def hello():
    return Hello(user_id=user_id, username=username, birthdate=datetime, gender=gender)


def test_hello_attributes(hello):
    assert hello.user_id == user_id
    assert hello.birthdate == datetime
    assert hello.username == username


def test_hello_repr(hello):
    assert repr(hello) == f'Hello(user_id={user_id!r}, username={username!r}, birthdate={datetime!r}, gender={gender!r})'


def test_hello_str(hello):
    assert str(hello) == f'user {user_id}: {username}, born {datetime:%B %d, %Y} ({gender})'


def test_hello_eq(hello):
    h1 = Hello(user_id, username, datetime, gender)
    assert h1 == hello
    h2 = Hello(user_id + 1, username, datetime, gender)
    assert h2 != hello
    h3 = Hello(user_id + 1, username, datetime + dt.timedelta(minutes=1), gender)
    assert h3 != hello
    h4 = Hello(user_id + 1, username + '!', datetime + dt.timedelta(minutes=1), gender)
    assert h4 != hello
    h5 = 1
    assert h5 != hello
    h6 = lambda: None
    h6.user_id = user_id
    h6.birthdate = datetime
    h6.username = username
    h6.gender = gender
    assert h6 != hello


def test_hello_serialize(hello):
    assert hello.serialize() == serialized


def test_hello_deserialize():
    h = Hello.deserialize(serialized)
    assert h.user_id == user_id
    assert h.birthdate == datetime
    assert h.username == username
    assert h.gender == gender


def test_hello_symmetry(hello):
    assert Hello.deserialize(hello.serialize()) == hello


fields = ['a', 'bb', 'ccc']
serialized_config = b"\x03\x00\x00\x00\x01\x00\x00\x00a\x02\x00\x00\x00bb\x03\x00\x00\x00ccc"


@pytest.fixture
def config():
    return Config(fields)


def test_config_attributes(config):
    assert config.fields == fields


def test_config_repr(config):
    assert repr(config) == f'Config(fields={fields!r})'


def test_config_str(config):
    assert str(config) == f'Supported fields: {fields!r}'


def test_config_eq(config):
    c1 = Config(fields)
    assert c1 == config
    c2 = Config(['bla'])
    assert c2 != config
    c3 = lambda: None
    c3.fields = fields
    assert c3 != config


def test_config_serialize(config):
    assert config.serialize() == serialized_config


def test_config_deserialize():
    c = Config.deserialize(serialized_config)
    assert set(c.fields) == set(fields)


def test_config_symmetry(config):
    assert Config.deserialize(config.serialize()) == config
