"""

"""

from flask import Flask, abort, current_app, request
from .restful_auth_routes import RestfulAuth__Routes
from .restful_auth_decorators import RestfulAuth__Decorators
from .default_config import *
from functools import wraps
import jwt

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
        


        
