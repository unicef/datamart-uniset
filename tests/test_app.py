def test_home(client):
    resp = client.post('/login/', data=dict(username='admin', password='123'))
    assert 'User confirmation needed' not in str(resp)
    res = client.get('/')
    assert res.location == 'http://localhost/superset/welcome'
    res = client.get(res.location)
    res = client.get('/users')


def test_welcome(tapp):
    with tapp.session_transaction() as sess:
        sess['user_id'] = 1
        res = tapp.get('/')
        res = res.follow().follow()
        assert res
