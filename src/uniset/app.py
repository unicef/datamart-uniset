def setup():
    from superset import app, appbuilder
    from .monkeypatch import patcher
    from .models import UserProfile  # noqa
    patcher.patch2(appbuilder)
    return app


app = setup()
