# Endpoints

CLIENT_ENDPOINT_CREATE_URI = '/user/signup'
CLIENT_ENDPOINT_CREATE_METHODS = ['POST']
CLIENT_ENDPOINT_LOGIN_URI = '/user/login'
CLIENT_ENDPOINT_LOGIN_METHODS = ['POST']
CLIENT_ENDPOINT_LOGOUT_URI = '/user/logout'
CLIENT_ENDPOINT_LOGOUT_METHODS = ['GET', 'POST']

# Underlying Security mechanism.

JWT_ENABLE = True
""""""

JWT_COOKIE_NAME = 'Atoken' #Access tokens
JWT_REF_COOKIE_NAME = 'Rtoken' #Refresh tokens

JWT_STORE_AS_SESSION = True
"""
JWT_STORE_AS_SESSION
    If True, the JWT will be stored in the database and used secondary source
    to verify the validity of the token. Storing the JWT is useful in the case
    that a given token needs to be revoked.

    If False, a given JWT is valid until its expiry condition has occured.

    Dependencies
        JWT_ENABLE must be True to set this to True.
"""

JWT_VERIFY_TOKEN_WITH_AUTHENTICATION_SERVER = True # TODO
JWT_EXPIRATION_TIMEOUT = 3600 # 1 hour in seconds TODO

BASIC_HTTP_AUTH_ENABLE = False # TODO: Implement.
DIGEST_HTTP_AUTH_ENABLE = False # TODO: Implement.
SESSION_ENABLE = False # TODO: Implement.
OAUTH2_ENABLE = False # TODO: Implement.



AUTHENTICATION_CHANNEL_HTTP_BASIC_AUTH = True
"""
AUTHENTICATION_CHANNEL_HTTP_BASIC_AUTH
    Using the authentication header channel 

"""

AUTHENTICATION_BASIC_MESSAGE_MISSING = 'verfication failed - missing auth info'
AUTHENTICATION_FORM_MESSAGE_MISSING = 'verfication failed - missing auth info'
AUTHENTICATION_JSON_MESSAGE_MISSING = 'verfication failed - missing auth info'


AUTHENTICATION_CHANNEL_FORM = False
AUTHENTICATION_CHANNEL_JSON = False

AUTHENTICATION_USER_FIELD_NAME = 'username'
AUTHENTICATION_PASSWORD_FIELD_NAME = 'password'
AUTHENTICATION_PASSWORD_ENCRYPTION = None
AUTHENTICATION_PASSWORD_STORAGE_ENCRYPTION_SALT_SHA256 = True

LOGIN_USER_NOT_FOUND_MESSAGE = 'username or password is incorrect'
LOGIN_USER_WRONG_PASSWORD_MESSAGE = 'username or password is incorrect'