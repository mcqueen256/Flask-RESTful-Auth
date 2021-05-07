import base64

valid_credentials = base64.b64encode(b"u1:password").decode("utf-8")

def action_login(server, username, password):
    pass

def action_signup(username, password):
    pass

def add_mock_user(server, username, password):
    return

def get_cookies(response):
    """
    Helper function to retreive the cookies from a response.
    """
    cookie_string = response.headers.get('Set-Cookie')
    cookies = {
        w.split('=')[0]:w.split('=')[1]
        for w in cookie_string.split('; ')
    }
    return cookies

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

def test_basic_auth_login_and_token(client):
    """
    Blackbox test. Tests the login without knowing how the server internally
    works. Use basic auth and check the token is valid.
    """
    response = client.post(
        '/user/login',
        headers={"Authorization": "Basic " + valid_credentials}
    )
    assert response.status_code == 200

    cookies = get_cookies(response)
    assert 'token' in cookies
    # check the contents of the Token
    token = cookies['token']
    payload_segment = token.split('.')[1] # get the payload from the jwt
    import json, base64
    payload_segment += '=='
    payload_str = base64.decodestring(payload_segment.encode('ascii'))
    payload = json.loads(payload_str)
    assert 'exp' in payload
    assert 'id' in payload
    return

def test_login_and_authenticated(client):
    """
    Whitebox test. Check the internal client variables are being set on login.
    """
    # Before Login
    with client.application.test_request_context('/'):
        user = client.application.restful_auth.storage.get_client_by_username('u1')
        assert user.is_authenticated == False
        assert user.token == None
    response = client.post(
        '/user/login',
        headers={"Authorization": "Basic " + valid_credentials}
    )
    # If the assertion below fails, also check the test_basic_auth_login test.
    # After Login
    with client.application.test_request_context('/'):
        user = client.application.restful_auth.storage.get_client_by_username('u1')
        assert user.is_authenticated == True
        assert user.token is not None
    return



def test_missing_global_txt(client):
    pass
