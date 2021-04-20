"""

Server

Example 0: Global and User Text Editor
======================================

This server demonstrates the access control of two endpoints:
 - /text/global.txt
 - /text/user/<username>.txt

All registered users can read and write to the /text/global.txt, however
only a user can read and write to their own /text/user/<username>.txt file.

The user management endpoints are implemented by the flask_restful_auth
package. By default, they include:
- /user/signup
- /user/login
- /user/logout
"""

import os
from flask import Flask, jsonify, request, make_response
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
from passlib.hash import sha256_crypt as sc
import uuid
import secrets
import jwt
import datetime

from flask_restful_auth.restful_auth import RestfulAuth
from flask_restful_auth import login_required

def create_app():
    """ Flask application factory. """

    app = Flask(__name__)

    # Configure flask app
    app.config['SECRET_KEY'] = os.environ.get('Secret')
    app.config['SQLALCHEMY _DATABASE_URI'] = 'something'

    # Initialise Flask-SQLAlchemy
    db = SQLAlchemy(app)

    app.blacklist = [] # TODO: Cannot have this in application memory. See issue #5
    class User(db.Model):
        ''' Setting up User'''
        id = db.Column(db.Integer, primary_key=True)
        # User vereification
        username = db.Column(db.String(60), nullable=False, unique=True)
        password = db.Column(db.String(300), nullable=False)
        active = db.Column(db.String(50),nullable=False)
        token = db.Column(db.String(500),nullable = True)
        # User details
        name = db.Column(db.String(50), nullable=False)


    def encoding_password(password):
        return sc.hash(password)

    # Initialise Flask-RESTful-Auth
    auth = RestfulAuth(app, User)

    #creating decorator
    #can be used for email auth
    def require_login(func):
        @wraps(func)
        def checking(*args,**kwargs):
            token = request.args.get('token')
            if not token or token in blacklist:
                return jsonify({'message':  'Missing token'}),403
            try:
                data = jwt.decode(token, app.config['SECRET_KEY'])
                verified_user = User.query.filter_by(id = data['id']).first()
            except:
                return jsonify({'message': 'token is invalid'}),403
            return func(verified_user,*args, **kwargs)
        return checking

    @app.route('/',methods=['GET','POST'])
    def index():
        return 'Welcome to chatbox'

    #create/register a user
    @app.route('/register',methods=['GET','POST'])
    def sign_up():
        data = request.form

        #securing the password
        passw = encoding_password(data['password'])
    
        #create new user
        new_user = User(id=uuid.uuid4(), name = data['name'],active = "False",password = passw, email = data['email'],username = data['username'])
    
        #add to database
        db.session.add(new_user)
        db.session.commit()
        
        return '<h1>New User Created</h1>'

    #login to user section
    @app.route('/login',methods=['GET','POST','PUT'])
    def login():
        auth = request.authorization

        if not auth or not auth.username or not auth.password:
            return make_response('verfication failed',401)

        user = User.query.filter_by(username = auth.username).first()

        if not user:
            return make_response('Either username or Password is incorrect. Please try Again!!!',401)

        if sc.verify(auth.password,user.password):
            user.active = "True"
            tokn= jwt.encode(
                {
                    'id':user.id,
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
                },
                app.config['SECRET']
            )
            user.token = tokn
            db.session.commit()
            return redirect(url_for('home', token = tokn))

    #logout of user section
    @app.route('/logout/<token>',methods=['GET','POST','PUT'])
    @login_required
    def logout(current_user):
        if current_user.active == "True":
            try:
                jwt.verify(token,app.config['SECRET_KEY']) #checking if the token is still valid or not
            except:
                current_user.user.active = "False"
            blacklist.append(token) #invalidating the token if not expired yet
        return redirect(url_for('/'))

    #check if the invalid token has expired or not
    def invalidate_token():
        for invalid in blacklist:
            try:
                jwt.verify(invalid,app.config['SECRET_KEY'])
            except:
                blacklist.remove(invalid)
    return app
        
    
# Start development web server
if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
