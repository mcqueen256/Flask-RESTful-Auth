from flask import current_app, make_response, redirect, request, url_for
from passlib.hash import sha256_crypt as sc
import uuid
import jwt
import datetime

class RestfulAuth__Views(object):

    def login_view(self):
        User = current_app.restful_auth.UserClass
        db = current_app.db

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
                current_app.config['SECRET']
            )
            user.token = tokn
            db.session.commit()
            return redirect(url_for('home', token = tokn))

    def logout_view(self):
        # TODO: Dose not work
        if current_user.active == "True":
            try:
                jwt.verify(token,app.config['SECRET_KEY']) #checking if the token is still valid or not
            except:
                current_user.user.active = "False"
            curent_app.blacklist.append(token) #invalidating the token if not expired yet
        return redirect(url_for('/'))

    def register_view(self):
        User = current_app.restful_auth.UserClass
        db = current_app.db

        data = request.form

        #securing the password
        passw = encoding_password(data['password'])
    
        #create new user
        new_user = User(id=uuid.uuid4(), name = data['name'],active = "False",password = passw, email = data['email'],username = data['username'])
    
        #add to database
        db.session.add(new_user)
        db.session.commit()

def encoding_password(password):
    return sc.hash(password)