# coding=utf-8
from unittest import mock
from unittest.mock import Mock

import pytest
import vcr

from uniset.azure.synchronizer import SyncResult
from uniset.synchronizer import UnisetSynchronizer

# from uniset.azure.synchronizer import Synchronizer, SyncResult


@pytest.fixture()
def synchronizer():
    with mock.patch('uniset.azure.synchronizer.Synchronizer.get_token'):
        with mock.patch('uniset.synchronizer.UnisetSynchronizer._store'):
            return UnisetSynchronizer(extra={'role': None})


@pytest.fixture()
def unicef_user():
    from flask_appbuilder.security.sqla.models import User
    return User(email='sapostolico@unicef.org',
                username='sapostolico@unicef.org')


@pytest.fixture()
def user():
    from flask_appbuilder.security.sqla.models import User
    return User(email='sapostolico@gmail.org',
                username='sapostolico@unicef.org')
    # azure_id='21d2ecba-83e4-4e81-a93c-d44f55dd222e')


def test_syncresult():
    result = SyncResult()
    result.log("error")
    result.log(("created", True))
    result.log(("updated", False))

    assert result.created == ["created"]
    assert result.skipped == ["error"]
    assert result.updated == ["updated"]


def test_syncresult_add():
    result1 = SyncResult()
    result2 = SyncResult()
    result1.log("error")
    result2.log(("created", True))

    result = result1 + result2
    assert result.created == ["created"]
    assert result.skipped == ["error"]
    assert result1.created == []

    with pytest.raises(ValueError):
        result = result1 + {}  # noqa

    result1 += result2
    assert result1.created == ["created"]
    assert result1.skipped == ["error"]


def test_syncresult_eq():
    assert SyncResult() == SyncResult([])
    assert not SyncResult([0]) == SyncResult([])
    assert not SyncResult([0]) == []


@vcr.use_cassette('tests/vcr_cassettes/fetch_users.yaml')
def test_fetch_users(synchronizer):
    result = synchronizer.fetch_users("startswith(mail,'sapostolico')")
    assert result.created


# @vcr.use_cassette('tests/vcr_cassettes/sync_unicef_user.yaml')
# def test_sync_unicef_user(synchronizer, unicef_user):
#     result = synchronizer.sync_user(unicef_user)
#     assert result == unicef_user


# @vcr.use_cassette('tests/vcr_cassettes/sync_user.yaml')
# def test_sync_user(synchronizer, user):
#     with pytest.raises(ValueError):
#         synchronizer.sync_user(user)


@vcr.use_cassette('tests/vcr_cassettes/syncronize.yaml')
def test_syncronize(synchronizer):
    result = synchronizer.syncronize(10)
    assert len(result.created) == 5
    assert len(result.updated) == 0
    assert len(result.skipped) == 7


@vcr.use_cassette('tests/vcr_cassettes/resume.yaml')
def test_resume(synchronizer):
    result = synchronizer.resume(max_records=10)
    assert len(result.created) == 5
    assert len(result.updated) == 0
    assert len(result.skipped) == 7


@vcr.use_cassette('tests/vcr_cassettes/get_token.yaml')
def test_get_token():
    synchronizer = UnisetSynchronizer()
    token = synchronizer.get_token()
    assert token


@vcr.use_cassette('tests/vcr_cassettes/exception.yaml')
def test_exception():
    with mock.patch('requests.get', side_effect=ConnectionError()):
        synchronizer = UnisetSynchronizer()
        with pytest.raises(ConnectionError):
            synchronizer.get_page("http://page")

    with mock.patch('requests.get', Mock(status_code=500)):
        synchronizer = UnisetSynchronizer()
        with pytest.raises(ConnectionError):
            synchronizer.get_page("http://page")

    with mock.patch('requests.get', return_value=Mock(status_code=400,
                                                      content="",
                                                      json=lambda: {"error": {"message": "--"}})):
        synchronizer = UnisetSynchronizer()
        with pytest.raises(ConnectionError):
            synchronizer.get_page("http://page")


def test_token_expired():
    content = {"error": {
        "code": "InvalidAuthenticationToken",
        "message": "Access token has expired.",
        "innerError": {"request-id": "a4acb36b-7e25-4a90-b754-9f032218888a",
                       "date": "2018-09-26T18:46:23"}
    }}

    def get_responses():
        yield Mock(status_code=401, json=lambda: content)
        yield Mock(status_code=200, json=lambda: {})

    responses = get_responses()

    with mock.patch('uniset.azure.synchronizer.Synchronizer.get_token') as get_token:
        with mock.patch('requests.get', lambda *k, **kw: next(responses)):
            synchronizer = UnisetSynchronizer()
            synchronizer.get_page("http://page")
            assert get_token.call_count == 3
