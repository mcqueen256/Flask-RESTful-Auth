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
        User = current_app.restful_auth.UserClass
        # Auqire the database adaptor
        # TODO: change to an adaptor class, don't use the database directly.
        db = current_app.db


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

        user = User.query.filter_by(username = user_identifier).first()
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

        user.is_authenticated = True

        # TODO: check the users active status

        response = make_response("ok", 200)

        if JWT_ENABLE:
            secret = current_app.config['SECRET']
            secret_1 = current_app.config['SECRET1']
            r_token: str = generate_refresh_token(user.id,secret_1)
            a_token: str = generate_access_token(user.id,secret)
            response.set_cookie(JWT_COOKIE_NAME, value=a_token)
            response.set_cookie(JWT_NEW_COOKIE_NAME, value=r_token)
            
            if JWT_STORE_AS_SESSION:
                user.token = a_token
                user.r_token = r_token
        
        else:
            # TODO: Workout what happens here (config error 500).
            pass

        db.session.add(user)
        db.session.commit()
        return response

    def logout_view(self):

        User = current_app.restful_auth.UserClass
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
                user = User.query.filter_by(id=id).first()
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
                user = self.UserClass.query.filter_by(id=id).first()
                if user is None:
                    return False
                if JWT_STORE_AS_SESSION:
                    if user.token != token:
                        return False
            except Exception as e: # TODO: make exceptions specific, if evaluated to be necessary.
                print('e', e)
                return False
        return True
        
    def refresh(self):
        if user.is_authenticated and JWT_ENABLE:
            token = request.cookies.get(JWT_COOKIE_NAME)
            secret = current_app.config['SECRET']
            if not self.validate_token(token,secret):
                r_token = request.cookies.get(JWT_NEW_COOKIE_NAME)
                secret_1 = current_app.config['SECRET1']
                if self.validate_token(r_token,secret_1):
                    data = jwt.decode(r_token, secret1, "HS256")
                    user = self.UserClass.query.filter_by(id=data['id']).first()
                    if user is none:
                        return False # or to logout page
                    if JWT_STORE_AS_SESSION:
                        if user.r_token != r_token:
                            return False #or to logout page
                    token = generate_access_token(data['id'],secret)
                    user.token = token
                    db.session.commit()
                    return True
                else:
                    return False#to logout page
            else:
                return # to the directed page
        else: 
            return #to login page

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

def generate_refresh_token(self,uid,key):
    payload = {
                'id': uid,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
            }    
    return jwt.encode(payload,key)

def generate_access_token(self,uid,key):
    payload = {
                'id': uid,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=2)
            }    
    return jwt.encode(payload,key)

def validate_token(self,token,secret):
    try:
        jwt.verify(token,secret)
        return True
    except:
        return False