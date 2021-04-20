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
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
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

    # Create the user class.
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

    # Initialise Flask-RESTful-Auth
    auth = RestfulAuth(app, User)

    # Define some routes
    @app.route('/',methods=['GET','POST'])
    def index():
        return 'Welcome to chatbox'

    # Print the url list in the console.
    print(app.url_map)

    return app
        
    
# Start development web server
if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
