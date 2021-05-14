"""
    **Example 0: Global and User Text Editor**


    This server demonstrates the access control of two endpoints:
     ``/text/global.txt``
     ``/text/user/<username>.txt``

    All registered users can read and write to the ``/text/global.txt``, however
    only a user can read and write to their own ``/text/user/<username>.txt`` file.

    The user management endpoints are implemented by the flask_restful_auth
    package. By default, they include:
        ``/user/signup``, ``/user/login``, ``/user/logout``


    **Usage of Curl**

    Curl is a universal tool that runs on Windows, Mac and Linux which helps in transferring data across the network

    Below are some example commands of curl

    - Curl usage help::

        curl -h

    - GET method::

         #used to gain access to resources from the URL specified
         curl -X GET https://www.gmail.com/

    - POST method::

         #posts information to the web server
         curl -X POST https://yourwebsite.com/

    - PUT method::

        #creates or replaces an existing server
        curl -X PUT https://yourwebsite.com/

"""

from flask import Flask
from flask import request
from flask_sqlalchemy import SQLAlchemy
from flask_restful_auth import RestfulAuth
from flask_restful_auth.storage_adaptors import SQLAlchemyStorageAdaptor

from pathlib import Path


def create_app():

    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'my little secret'
    app.config['SECRET'] = 'my little secret'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Initialise Flask-SQLAlchemy
    db = SQLAlchemy(app)
    # Create the user class.
    class User(db.Model):
        ''' Setting up User'''
        id = db.Column(db.String(36), primary_key=True)
        is_authenticated = db.Column(db.Boolean, nullable=False)
        is_active = db.Column(db.Boolean, nullable=False)
        # User vereification
        username = db.Column(db.String(60), nullable=False, unique=True)
        password = db.Column(db.String(300), nullable=False)
        token = db.Column(db.String(500), nullable=True)
        r_token = db.Column(db.String(500), nullable=True)

    app.db = db
    # Create tables
    db.create_all()

    # create database addaptor
    storage = SQLAlchemyStorageAdaptor(db, User)
    # Initialise Flask-RESTful-Auth
    auth = RestfulAuth(app, storage)

    # make application directories
    Path('testdata/text/').mkdir(parents=True, exist_ok=True)
    Path('testdata/text/user/').mkdir(parents=True, exist_ok=True)

    @app.route('/')
    def index():
        return "Index page"

    @app.route('/text/global.txt', methods=['GET', 'POST', 'PUT'])
    @auth.login_required 
    def resource_global():
        """
        """
        if request.method == 'GET':
            #read the contents of the file and return it
            return read_file_or_default('testdata/text/global.txt', default=b'authorized text file data')
        if request.method in ['POST', 'PUT']:
            #read the contents of the file and return it
            with open('testdata/text/global.txt', 'wb') as fout:
                #arguments for write
                fout.write(request.data)
                return "ok"
        # Unreachable
        return

    @app.route('/text/user/<username>.txt')
    @auth.login_required
    def resouce_user(username):
        """
        """
        # User constraint
        user = auth.current_user
        if not user:
            return 'unauthorized', 401
        if user.username != username:
            return 'unauthorized', 401
        # logged in must be the correct user. Process request
        if request.method == 'GET':
            #read the contents of the file and return it
            return read_file_or_default(f'testdata/text/user/{username}.txt')
        if request.method in ['POST', 'PUT']:
            #read the contents of the file and return it
            with open(f'testdata/text/user/{username}.txt', 'wb') as fout:
                #arguments for write
                fout.write(request.data)
                return "ok"
        # Unreachable
        return
    
    return app


def read_file_or_default(filepath, default=b''):
    """
    Helper function.

    Read the file from the server file system. If the file is not available,
    write a file with some default content and return that content.

    :param filepath: is the path to the file to read. If the file does not
        exist, the default value is written.
    :param default: is the byte string used if the file does not exist.
    """
    try:
        with open(filepath, 'rb') as fin:
            return fin.read()
    except FileNotFoundError:
        with open(filepath, 'wb') as fout:
            fout.write(default)
        # Try again
        try:
            with open(filepath, 'rb') as fin:
                return fin.read()
        except FileNotFoundError:
            # On the second fail, return an error
            return ('failed to read server file', 500)


# Start development web server
if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)