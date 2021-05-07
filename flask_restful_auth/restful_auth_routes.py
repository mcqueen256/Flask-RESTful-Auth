from flask import current_app, make_response, request, Response
from passlib.hash import sha256_crypt
import uuid
import jwt
import datetime

from flask_login import login_user, current_user

from .default_config import *

def reject_login_attempt(message: str) -> Response:
    response = make_response(message, 401)
    clear_auth_cookie(response)
    return response


def clear_auth_cookie(response: Response) -> Response:
    if JWT_ENABLE:
        response.set_cookie(JWT_COOKIE_NAME)
    return response

class RestfulAuth__Routes(object):

    def login_route(self):

        # Construct empty credentials
        user_identifier = None
        password = None
        credentials = (user_identifier, password)

        # Extract the credentials
        if AUTHENTICATION_CHANNEL_HTTP_BASIC_AUTH:

            auth = request.authorization
            if not auth or not auth.username or not auth.password:
                return reject_login_attempt(AUTHENTICATION_BASIC_MESSAGE_MISSING)
            user_identifier = auth.username
            password = auth.password

        elif AUTHENTICATION_CHANNEL_FORM:

            # TODO: Untested.
            user_identifier = request.form[AUTHENTICATION_USER_FIELD_NAME]
            password = request.form[AUTHENTICATION_PASSWORD_FIELD_NAME]
            if not user_identifier or not password:
                return reject_login_attempt(AUTHENTICATION_FORM_MESSAGE_MISSING)
        
        elif AUTHENTICATION_CHANNEL_JSON:

            # TODO: Untested
            user_identifier = request.json()[AUTHENTICATION_USER_FIELD_NAME]
            password = request.json()[AUTHENTICATION_PASSWORD_FIELD_NAME]
            if not user_identifier or not password:
                return reject_login_attempt(AUTHENTICATION_JSON_MESSAGE_MISSING)
            
        else:
            # TODO: Workout what happens here (config error 500).
            pass

        # Query datastore for the user.

        user = self.storage.get_client_by_username(user_identifier)
        if not user:
            return reject_login_attempt(LOGIN_USER_NOT_FOUND_MESSAGE)

        # Check the password.

        password_verified = False
        if AUTHENTICATION_PASSWORD_STORAGE_ENCRYPTION_SALT_SHA256:
            password_verified = sha256_crypt.verify(password, user.password)
        else:
            # TODO: Workout what happens here (config error 500).
            pass
        
        if not password_verified:
            return reject_login_attempt(LOGIN_USER_WRONG_PASSWORD_MESSAGE)

        # At this point, the user is considered authenticated. Build the response.

        self.storage.set_client_authenticated_status(user, True)

        # TODO: check the users active status

        response = make_response("ok", 200)

        if JWT_ENABLE:
            payload = {
                'id': user.id,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
            }
            secret = current_app.config['SECRET']
            token: str = jwt.encode(payload, secret)
            response.set_cookie(JWT_COOKIE_NAME, value=token)
            if JWT_STORE_AS_SESSION:
                user.token = token
                self.storage.set_client_token(user, token)
        else:
            # TODO: Workout what happens here (config error 500).
            pass

        self.storage.save_client(user)
        
        return response

    def logout_route(self):

        # Auqire the database adaptor
        # TODO: change to an adaptor class, don't use the database directly.
        response = make_response("logout")
        clear_auth_cookie(response)

        user = None
        if JWT_ENABLE:
            token = request.cookies.get(JWT_COOKIE_NAME)
            if token is None:
                return response
            try:
                secret = current_app.config['SECRET']
                data = jwt.decode(token, secret, "HS256")
                id = data['id']
                user = self.storage.get_client_by_id(id)
                # TODO: check if the client is None
                if JWT_STORE_AS_SESSION:
                    user.token = None
            except Exception as e: # TODO: make exceptions specific, if evaluated to be necessary.
                print('e', e)
                return response
        
        if user is not None:
            self.storage.set_client_authenticated_status(user, False)
            self.storage.save_client(user)
            
        return response

    def register_route(self):

        response = make_response('success')

        username = None
        password = None
        if request.form['username'] is not None and request.form['password'] is not None:
            username = request.form['username']
            password = request.form['password']
        else:
            return reject_login_attempt('missing username or password')

        #securing the password
        password = encoding_password(password)
    
        # Check the user does not already exist
        client = self.storage.get_client_by_username(username)
        if client is not None:
            return 'already registered', 401 # TODO: is this the correct error code?

        #create new user
        #add to database
        new_user = self.storage.create_client(username, password)
        self.storage.save_client(new_user)

        return response

def encoding_password(password):
    return sha256_crypt.hash(password)