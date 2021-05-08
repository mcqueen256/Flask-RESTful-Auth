from flask import current_app, request, jsonify

import jwt
from functools import wraps

def login_required(func):
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
    @wraps(func)
    def checking(*args,**kwargs):
        restful_auth = current_app.restful_auth
        token = request.args.get('token')
        if not token or token in current_app.blacklist:
            return jsonify({'message':  'Missing token'}),403
        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'])
            verified_user = restful_auth.UserClass.query.filter_by(id = data['id']).first()
        except:
            return jsonify({'message': 'token is invalid'}),403
        return func(verified_user, *args, **kwargs)
    return checking