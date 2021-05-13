from flask import current_app, request, jsonify
from .default_config import *
import jwt
from functools import wraps
"""
    **Create Teacher Record**
    This function allows user to create(post) a teacher record.
    :return: teacher's information added by the user in json and http status code
    - Example::
        curl -X POST http://localhost:5000/ -H 'cache-control: no-cache' -H 'content-type: application/json' \
        -d '{
            "name": "Mary Rose",
            "subject": "Biology"
        }'
    - Expected Success Response::
        HTTP Status Code: 201
        {
            "name": "Mary Rose",
            "subject": "Biology"
        }
    - Expected Fail Response::
        HTTP Status Code: 400
        {'error': 'Duplicate teacher name'}
"""


# def refresh_tokens(func):
#     """This decorator is used for checking if the access token has expired or not

#     Return:
#         bool : True if refreshed, flase if Access/Refresh Token does not exist/Refresh token is not verified 
#     """
#     @wraps(func)
#     def token_checking(*args,**kwargs):
#         status = self.refresh()
#         if status:
#             token = request.cookies.get(JWT_COOKIE_NAME)
#             secret = current_app.config['SECRET']
#             try:
#                 data = jwt.decode(token,secret)
#                 verified_user = restful_auth.UserClass.query.filter_by(id = data['id']).first()
#                 return func(verified_user, *args, **kwargs)
#             except:
#                 return jsonify({'message': 'token is invalid'}),403
#         else:
#             return jsonify({'message':  'Missing token,User Not Authorised'}),403
#     return token_checking