# 
# Server
# 
# Example 0: Global and User Text Editor
# ======================================
#
# This server demonstrates the access control of two endpoints:
#  - /text/global.txt
#  - /text/user/<username>.txt
#
# All registered users can read and write to the /text/global.txt, however
# only a user can read and write to their own /text/user/<username>.txt file.
#
# The user management endpoints are implemented by the flask_restful_auth
# package. By default, they include:
# - /user/signup
# - /user/login
# - /user/logout

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful_auth import RestfulAuth, login_required
from flask import request
from flask_login import UserMixin, login_required

def create_app():
    """ Flask application factory. """

    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'my little secret'
    app.config['SECRET'] = 'my little secret'

    # Initialise Flask-SQLAlchemy
    db = SQLAlchemy(app)

    app.db = db

    # Create the user class.
    class User(db.Model, UserMixin):
        ''' Setting up User'''
        id = db.Column(db.String(36), primary_key=True)
        is_authenticated = db.Column(db.Boolean, nullable=False)
        is_active = db.Column(db.Boolean, nullable=False)
        # User vereification
        username = db.Column(db.String(60), nullable=False, unique=True)
        password = db.Column(db.String(300), nullable=False)
        token = db.Column(db.String(500), nullable=True)

    # Create tables
    db.create_all()

    import uuid
    from passlib.hash import sha256_crypt
    new_user = User(
        id=str(uuid.uuid4()),
        is_active=True,
        is_authenticated=False,
        password=sha256_crypt.hash('password'),
        username='u1',
    )
    #add to database
    db.session.add(new_user)
    db.session.commit()

    # Initialise Flask-RESTful-Auth
    auth = RestfulAuth(app, User)

    @app.route('/')
    def index():
        return "Index page"

    @app.route('/text/global.txt', methods=['GET', 'POST', 'PUT'])
    # @login_required 
    def resource_global():
        print(request.data)
        if request.method == 'GET':
            #read the contents of the file and return it
            try:
                with open('global.txt', 'rb') as fin:
                    return fin.read()
            except ValueError:
                print('File Not Found')
        if request.method in ['POST', 'PUT']:
            #read the contents of the file and return it
            with open('global.txt', 'wb') as fout:
                #arguments for write
                fout.write(request.data)
                return "ok"
        return "TODO"

    @app.route('/text/user/<username>.txt')
    @auth.login_required
    def resouce_user(username):
        return "TODO"
    
    # Print the url list in the console.
    if app.config['DEBUG'] is not None:
        print(app.url_map)
    
    return app

# Start development web server
if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)