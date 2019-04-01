import os


from uniset.settings import env
from .monkeypatch import patcher

VERSION = __version__ = '0.3'
NAME = 'uniset'

ROOT = os.path.dirname(__file__)

if env('SENTRY_DSN'):
    import sentry_sdk
    from sentry_sdk.integrations.flask import FlaskIntegration

    sentry_sdk.init(env('SENTRY_DSN'),
                    integrations=[FlaskIntegration()]
                    )
patcher.patch1()
