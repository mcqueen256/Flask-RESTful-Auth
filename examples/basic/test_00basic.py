import base64
from .server.create_app import User

valid_credentials = base64.b64encode(b"u1:password").decode("utf-8")

def action_login(server, username, password):
    pass

def action_signup(username, password):
    pass

def add_mock_user(server):
    db = server.db


def test_index(client):
    response = client.get('/')
    assert response.data == b'Index page'
    return

def test_unauthorized_access(client):
    """

    Prerequisits. The client must exist in the database.

    """
    response = client.get('/text/user/u1.txt')
    assert response.status_code == 401
    assert response.data == b'not authorized'
    return

def test_authenticate_and_aquire_token(client):
    response = client.post(
        '/user/login',
        headers={"Authorization": "Basic " + valid_credentials}
    )
    assert response.status_code == 200

    cookie_string = response.headers.get('Set-Cookie')
    cookies = {
        w.split('=')[0]:w.split('=')[1]
        for w in cookie_string.split('; ')
    }
    assert 'token' in cookies

    # maybe test the token content?
    return


def test_missing_global_txt(client):
    pass
