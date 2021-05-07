import base64
import json

valid_credentials = base64.b64encode(b"u1:password").decode("utf-8")

def add_mock_user(server, username, password):
    """
    Creates an unauthenticated user in the database for testing.
    """ 
    with server.application.test_request_context('/'):
        storage = server.application.restful_auth.storage
        user = storage.create_client(username, password)
        storage.save_client(user)
    return (user, username, password)

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

def test_index(server):
    response = server.get('/')
    assert response.data == b'Index page'
    return

def test_unauthorized_access(server):
    """

    Prerequisits. The client must exist in the database.

    """
    response = server.get('/text/user/u1.txt')
    assert response.status_code == 401
    assert response.data == b'not authorized'
    return

def test_basic_auth_login_and_token(server):
    """
    Blackbox test. Tests the login without knowing how the server internally
    works. Use basic auth and check the token is valid.
    """
    add_mock_user(server, 'u1', 'password')
    response = server.post(
        '/user/login',
        headers={"Authorization": "Basic " + valid_credentials}
    )
    assert response.status_code == 200

    cookies = get_cookies(response)
    assert 'token' in cookies
    # check the contents of the Token
    token = cookies['token']
    payload_segment = token.split('.')[1] # get the payload from the jwt
    payload_segment += '=='
    payload_str = base64.decodebytes(payload_segment.encode('ascii'))
    payload = json.loads(payload_str)
    assert 'exp' in payload
    assert 'id' in payload
    return

def test_login_and_authenticated(server):
    """
    Whitebox test. Check the internal client variables are being set on login.
    """
    add_mock_user(server, 'u1', 'password')
    # Before Login
    with server.application.test_request_context('/'):
        user = server.application.restful_auth.storage.get_client_by_username('u1')
        assert user.is_authenticated == False
        assert user.token == None
    response = server.post(
        '/user/login',
        headers={"Authorization": "Basic " + valid_credentials}
    )
    # If the assertion below fails, also check the test_basic_auth_login test.
    # After Login
    with server.application.test_request_context('/'):
        user = server.application.restful_auth.storage.get_client_by_username('u1')
        assert user.is_authenticated == True
        assert user.token is not None
    return

def test_logout_and_token(server):
    """
    Blackbox test. Tests the logout without knowing how the server internally
    works. Any cached token should be removed.
    """

    # TODO: this test works but does not check the edge cases for a user.

    server.set_cookie('localhost', 'token', 'some token value')
    response = server.post('/user/logout')
    cookies = get_cookies(response)
    assert 'token' in cookies
    assert cookies['token'] == ''
    return

def test_register_user(server):
    """
    Blackbox test. Create a new user with a token on creation.
    """
    response = server.post('/user/signup', data={'username': 'bob', 'password': 'test1234'})
    
    assert response.status_code == 200
    assert response.data == b'success'
    return

def test_register_adds_user_to_database(server):
    """
    Whitebox test. Check the databse contains the registered user.
    """
    # 1. Check there is no such user in the database
    with server.application.test_request_context('/'):
        user = server.application.restful_auth.storage.get_client_by_username('alice')
        assert user == None
    # 2. Register user
    response = server.post('/user/signup', data={'username': 'alice', 'password': 'test1234'})
    # 3. Check user is in the database
    with server.application.test_request_context('/'):
        user = server.application.restful_auth.storage.get_client_by_username('alice')
        assert user != None
        assert user.username == 'alice'
    return

def test_missing_global_txt(server):
    pass
