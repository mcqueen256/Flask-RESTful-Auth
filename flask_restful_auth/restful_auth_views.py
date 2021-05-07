from flask import current_app, make_response, redirect, request, url_for, Response
from passlib.hash import sha256_crypt
import uuid
import jwt
import datetime
from functools import wraps

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

class RestfulAuth__Views(object):

    def login_view(self):

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

    def logout_view(self):

        # Auqire the database adaptor
        # TODO: change to an adaptor class, don't use the database directly.
        db = current_app.db
        response = redirect(url_for('/'))
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
            user.is_authenticated = False
            db.session.add(user)
            db.session.commit()
            
        return response

    def is_authorized(self) -> bool:
        # TODO: Below is slightly duplicated code
        if JWT_ENABLE:
            token = request.cookies.get(JWT_COOKIE_NAME)
            print(token)
            if token is None:
                return False # No token 
            try:
                secret = current_app.config['SECRET']
                data = jwt.decode(token, secret, "HS256")
                id = data['id']
                user = self.storage.get_client_by_id(id)
                if user is None:
                    return False
                if JWT_STORE_AS_SESSION:
                    if user.token != token:
                        return False
            except Exception as e: # TODO: make exceptions specific, if evaluated to be necessary.
                print('e', e)
                return False
        return True
        


    def login_required(self, func):
        @wraps(func)
        def decorated_view(*args, **kwargs):
            # TODO: add a global disable?
            if current_app.config.get('LOGIN_DISABLED'):
                return func(*args, **kwargs)
            elif not self.is_authorized():
                # return some_unauthorized_response_builder()
                return make_response('not authorized', 401)
            return func(*args, **kwargs)
        return decorated_view

    def register_view(self):
        User = current_app.restful_auth.UserClass
        db = current_app.db

        data = request.form

        #securing the password
        password = encoding_password(data['password'])
    
        #create new user
        new_user = User(
            id=uuid.uuid4(),
            is_active=True,
            password=password,
            username=data['username']
        )
    
        #add to database
        db.session.add(new_user)
        db.session.commit()

def encoding_password(password):
    return sc.hash(password)