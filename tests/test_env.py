import os
from contextlib import contextmanager
from io import StringIO

import pytest

from uniset.environ import Env

NOTSET = object()


@contextmanager
def setenv(**values):
    old = {}
    for k, v in values.items():
        old[k] = os.environ.get(k, NOTSET)
        if v == NOTSET:
            os.unsetenv(k)
        else:
            os.environ[k] = v
    yield
    for k, v in old.items():
        if v == NOTSET:
            del os.environ[k]
        else:
            os.environ[k] = v


def test_simple():
    with setenv(BASE=NOTSET):
        env = Env(defaults=dict(BASE=1))

        assert env.BASE == 1
        assert env('BASE') == 1
        assert os.environ['BASE'] == '1'


# def test_cast():
#     with setenv(BASE=NOTSET):
#         env = Env(defaults=dict(BASE=(str, 1)))
#         assert env.BASE == '1'
#         assert env('BASE') == '1'
#         assert os.environ['BASE'] == '1'


def test_environ():
    with setenv(BASE='22'):
        env = Env(defaults=dict(BASE=(int, 1)))
        assert env.BASE == 22
        assert env('BASE') == 22


def test_read_env():
    with setenv(BASE=NOTSET):
        env = Env(StringIO(u'BASE=33'), defaults=dict(BASE=(int, 1)))

        assert env.BASE == 33
        assert env('BASE') == 33
        os.environ['BASE'] = '33'


def test_lazy():
    with setenv(BASE=NOTSET):
        env = Env(StringIO(u'BASE=33'),
                  lazy=True,
                  defaults=dict(BASE=(int, 1)))

        assert env.BASE == 1
        assert env('BASE') == 1
        os.environ['BASE'] = '1'


@pytest.mark.parametrize("vartype,value", [(int, 1),
                                           (str, 'a'),
                                           (bool, 't'),
                                           (float, 1.1)])
def test_cast(vartype, value):
    with setenv(BASE=NOTSET):
        env = Env(defaults=dict(BASE=(vartype, value)))
        caster = getattr(env, vartype.__name__)
        assert caster('BASE') == value
        assert env.BASE == value
        assert env('BASE') == value
        os.environ['BASE'] = str(value)


def test_bytes():
    with setenv(BASE=NOTSET):
        env = Env(defaults=dict(BASE=(bytes, 'aa')))
        assert env.BASE == 'aa'
        assert env.bytes('BASE') == b'aa'
        os.environ['BASE'] = 'aa'
