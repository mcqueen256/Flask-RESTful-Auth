from passlib.hash import sha256_crypt
import uuid
from functools import wraps

from .default_config import *

# TODO: setup a default getter that always returns None

class RestfulAuth__Decorators(object):
    def client_getter(self, func):
        self._client_getter = func
        return func