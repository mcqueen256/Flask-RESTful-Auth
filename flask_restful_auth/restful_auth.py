"""

"""

from flask import Flask, abort, current_app, request
from .restful_auth_routes import RestfulAuth__Routes
from .restful_auth_decorators import RestfulAuth__Decorators
from .default_config import *
from functools import wraps
from passlib.hash import sha256_crypt
import jwt
import datetime

from .storage_adaptors import StorageAdaptorInterface

class RestfulAuth(RestfulAuth__Routes, RestfulAuth__Decorators):
    def __init__(self, app: Flask, storage: StorageAdaptorInterface):
        self.app: Flask = app
        self.init_app(app, storage)

    def init_app(self, app: Flask, storage: StorageAdaptorInterface):
        # bind Flask-RESTful-Auth to the app
        app.restful_auth = self
        self._add_url_routes(app)
        # bind the data storage adaptor
        self.storage: StorageAdaptorInterface = storage
    
    def is_authorized(self) -> bool:
        # TODO: Below is slightly duplicated code
        if JWT_ENABLE:
            token = request.cookies.get(JWT_COOKIE_NAME)
            if token is None:
                return False # No token 
            secret = current_app.config['SECRET']
            try:                   
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
    
    def refresh(self) -> bool:
        """
            **Refresh Tokens**
            After every refresh of webpage or when logging on to a new webpage
            This function, first confirms that  Access token has expired or not
            if it has,Then using a refresh token, it generates a new access token
            
            :Returns:
                bool: True if access/refresh key is still valid otherwise false 
        """
        
        if JWT_ENABLE:
            token = request.cookies.get(JWT_COOKIE_NAME)
            secret = current_app.config['SECRET']
            
            if token is None: #if no token exist
                return False #unauthorised access
            if self.validate_token(token=token,secret=secret):
                return True #to Directed Page
            else:
                r_token = request.cookies.get(JWT_REF_COOKIE_NAME)
                secret_1 = current_app.config['SECRET1']
                if self.validate_token(r_token,secret_1):
                    data = jwt.decode(r_token, secret_1, "HS256")
                    id = data['id']
                    user = self.storage.get_client_by_id(id).first()
                    if user is None:
                        return False # to logout/login page
                    if JWT_STORE_AS_SESSION:
                        if user.r_token != r_token:
                            return False #to logout/login page
                    a_token = self.generate_jwt_token(data['id'],secret,time=2)
                    user.token = a_token
                    self.storage.set_client_token(user, a_token)
                    self.storage.save_client(user)
                    return True #To directed Page
                else:
                    return False #to logout/login page
        else:
            return False #to logout/login page

    
    def encoding_password(self, password):
        """
            **Hashing Password**
            Encoding password for security purposes

            :Args:
                password (string): User password

            :Returns:
                String: Hash Password
        """
        return sha256_crypt.hash(password)

    def generate_jwt_token(self, uid, key, time:int):
        """
            **Create Jwt Tokens**
            Generate tokens for authentication purposes
            :Args:
                uid (string): User Id
                key (string): Secret key for encoding 
                time (int): valid time period in minutes

            :Returns:
                string: Encoded Token
        """
        payload = {
                    'id': uid,
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=time)
                }    
        return jwt.encode(payload,key)


    def validate_token(self, token,secret):
        """
            **Token Status Checkup**
            The function checks if token has expired or not
            :Args:
                token (string): token used for authentication
                secret (string): secret key

            :Returns:
                bool: true if token is still valid otherwise false
        """
        try:
            jwt.verify(token,secret) # TODO: This function does not exist
            return True
        except:
            return False

    @property
    def current_user(self):
        """Get the current user object."""
        # TODO: Below is slightly duplicated code
        if JWT_ENABLE:
            token = request.cookies.get(JWT_COOKIE_NAME)
            if token is None:
                return None # No token 
            try:
                secret = current_app.config['SECRET']
                data = jwt.decode(token, secret, "HS256")
                id = data['id']
                user = self.storage.get_client_by_id(id)
                if user is None:
                    return None
                if JWT_STORE_AS_SESSION:
                    if user.token != token:
                        return None
            except Exception as e: # TODO: make exceptions specific, if evaluated to be necessary.
                print('e', e)
                return None
        else:
            raise "Placeholder error: "
        return user

    def _add_url_routes(self, app: Flask):

        def login_stub():
            return self.login_route()

        def logout_stub():
            return self.logout_route()

        def register_stub():
            # if not self.USER_ENABLE_REGISTER: abort(404)
            return self.register_route()
        
        app.add_url_rule(CLIENT_ENDPOINT_CREATE_URI, 'client.create', register_stub,
                        methods=CLIENT_ENDPOINT_CREATE_METHODS)
        
        app.add_url_rule(CLIENT_ENDPOINT_LOGIN_URI, 'client.login', login_stub,
                        methods=CLIENT_ENDPOINT_LOGIN_METHODS)
        
        app.add_url_rule(CLIENT_ENDPOINT_LOGOUT_URI, 'client.logout', logout_stub,
                        methods=CLIENT_ENDPOINT_LOGOUT_METHODS)
        


        
