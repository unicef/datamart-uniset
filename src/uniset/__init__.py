import os

from .monkeypatch import patcher

VERSION = __version__ = '1.0'
NAME = 'uniset'

ROOT = os.path.dirname(__file__)


patcher.patch1()
