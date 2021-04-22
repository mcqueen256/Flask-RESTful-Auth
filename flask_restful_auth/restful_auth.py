"""

"""

from flask import abort, Flask
from .restful_auth_views import RestfulAuth__Views
from . import default_config as conf
from flask_login import LoginManager

class RestfulAuth(RestfulAuth__Views):
    def __init__(self, app: Flask, UserClass):
        self.app: Flask = app
        self.init_app(app, UserClass)

    def init_app(self, app, UserClass):
        # bind Flask-RESTful-Auth to the app
        app.restful_auth = self

        self.UserClass = UserClass

        self._login_manager = LoginManager()
        self._login_manager.init_app(app)
        @self._login_manager.user_loader
        def load_user(id):
            return UserClass.query.filter_by(id=id).first()

        self._add_url_routes(app)

    def _add_url_routes(self, app: Flask):

        def login_stub():
            return self.login_view()

        def logout_stub():
            return self.logout_view()

        def register_stub():
            # if not self.USER_ENABLE_REGISTER: abort(404)
            return self.register_view()
        
        app.add_url_rule(conf.CLIENT_ENDPOINT_CREATE_URI, 'client.create', register_stub,
                        methods=conf.CLIENT_ENDPOINT_CREATE_METHODS)
        
        app.add_url_rule(conf.CLIENT_ENDPOINT_LOGIN_URI, 'client.login', login_stub,
                        methods=conf.CLIENT_ENDPOINT_LOGIN_METHODS)
        
        app.add_url_rule(conf.CLIENT_ENDPOINT_LOGOUT_URI, 'client.logout', logout_stub,
                        methods=conf.CLIENT_ENDPOINT_LOGOUT_METHODS)
        


        
