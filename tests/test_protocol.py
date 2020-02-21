import datetime as dt

import pytest

from neuron.protocol import Hello


user_id = 1
datetime = dt.datetime(2000, 1, 1, 12, 0)
username = "Allen"
gender = 'm'
serialized = b"\x01\x00\x00\x00\x00\x00\x00\x00\x05\x00\x00\x00Allen@\xecm8m"


@pytest.fixture
def hello():
    return Hello(user_id=user_id, username=username, birthdate=datetime, gender=gender)


def test_attributes(hello):
    assert hello.user_id == user_id
    assert hello.birthdate == datetime
    assert hello.username == username


def test_repr(hello):
    assert repr(hello) == f'Hello(user_id={user_id!r}, username={username!r}, birthdate={datetime!r}, gender={gender!r})'


def test_str(hello):
    assert str(hello) == f'user {user_id}: {username}, born {datetime:%B %d, %Y} ({gender})'


def test_eq(hello):
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


def test_serialize(hello):
    assert hello.serialize() == serialized


def test_deserialize():
    h = Hello.deserialize(serialized)
    assert h.user_id == user_id
    assert h.birthdate == datetime
    assert h.username == username
    assert h.gender == gender


def test_symmetry(hello):
    assert Hello.deserialize(hello.serialize()) == hello
