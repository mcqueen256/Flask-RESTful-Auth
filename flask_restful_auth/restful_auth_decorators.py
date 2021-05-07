from flask import current_app, make_response
import uuid
from functools import wraps

from .default_config import *

class RestfulAuth__Decorators(object):
    def login_required(self, func):
        @wraps(func)
        def decorated_view(*args, **kwargs):
            # TODO: add a global disable?
            if current_app.config.get('LOGIN_DISABLED'):
                return func(*args, **kwargs)
            elif not self.is_authorized():
                return make_response('not authorized', 401)
            return func(*args, **kwargs)
        return decorated_view