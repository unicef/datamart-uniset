import os
import tempfile

import pytest


@pytest.fixture(autouse=True)
def conf():
    os.environ['DATABASE_URL'] = 'sqlite:///memory'
    from superset import security_manager
    security_manager.create_db()


@pytest.fixture
def app():
    db_fd, filename = tempfile.mkstemp(dir=os.curdir,
                                       prefix='TEST_',
                                       suffix='.DB')
    # os.environ['DATABASE_URL'] = 'sqlite:///%s' % filename
    from uniset.app import app
    app.config['TESTING'] = True
    app.config['WTF_CSRF_METHODS'] = []

    yield app

    os.close(db_fd)
    os.unlink(filename)


@pytest.fixture
def client(app):
    client = app.test_client()
    return client


# @pytest.fixture
# def tapp(app):
#     from superset import security_manager, db
#
#     security_manager.create_db()
#     db.session.merge(User(id=1, username='admin', first_name='F',
#                           last_name='L', email='e', password='123'))
#     db.session.commit()
#     tapp = TestApp(app, db=db, use_session_scopes=True)
#     tapp.set_authorization(('Basic', ('admin', '123')))
#     return tapp
