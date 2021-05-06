from flask import current_app, request, jsonify
from .restful_auth_views import RestfulAuth__Views 
import jwt
from functools import wraps


def login_required(func):
    """Decorator used for checking if access token is valid or not,
        if access token is present but not valid, 
        it will generate a new access token using refresh token.
     Return:
        details of current user
    """
    @wraps(func)
    def checking(*args,**kwargs):
        restful_auth = current_app.restful_auth
        auth = RestfulAuth__Views()
        checking_token = auth.refresh()
        if checking_token:
            try:
            token = request.cookies.get(JWT_COOKIE_NAME)
            secret = current_app.config['SECRET']
            data = jwt.decode(token, current_app.config['SECRET_KEY'])
            verified_user = restful_auth.UserClass.query.filter_by(id = data['id']).first()
            except:
                return jsonify({'message': 'token is invalid'}),403
            return func(verified_user, *args, **kwargs)
        else:
            return func(verified_user=None, *args, **kwargs)         
    return checking