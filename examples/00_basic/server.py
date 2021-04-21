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
# from flask_restful_auth import RestfulAuth, login_required, with_user
from flask import request

def create_app():
    """ Flask application factory. """

    app = Flask(__name__)

    # Initialise Flask-SQLAlchemy
    db = SQLAlchemy(app)
    db.create_all()

    # TODO: Define a User database ORM class and pass it to RestfulAuth

    # Initialise Flask-RESTful-Auth
    # auth = RestfulAuth(app, db)

    @app.route('/')
    def index():
        return "Index page"

    @app.route('/text/global.txt', methods=['GET', 'POST', 'PUT'])
    
    # @login_required 
    def resource_global():
        print(request.data)
        if request.method == 'GET':
            #read the contents of the file and return it
            with open('global.txt', 'rb') as fin:
                return fin.read()
        if request.method == 'PUT':
            #read the contents of the file and return it
            with open('global.txt', 'wb') as fout:
                #arguments for write
                fout.write(request.data)
                return "ok"
        if request.method == 'POST':
            #read the contents of the file and return it
            with open('global.txt', 'wb') as fout:
                
                fout.write(request.data)
                return "ok"
        return "TODO"

    @app.route('/text/user/<username>.txt')
    # @login_required
    def resouce_user(user):
        return "TODO"
    
    return app

# Start development web server
if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)