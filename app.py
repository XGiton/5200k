# -*- coding: utf-8 -*-
from flask import Flask
from flask.ext import login as flask_login
from uuid import uuid4
from base64 import b64encode
from config import DEBUG
from model.user import User
from model.token import Token


app = Flask(__name__, static_folder='public')

app.secret_key = b64encode(uuid4().hex)
app.debug = DEBUG

# login manager
login_manager = flask_login.LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    """: Override load_user method, and return User object or None as user not
    found, and if return None, user will be regard as unauthorized
    """
    user = User.p_col.find_one({User.Field._id: user_id}, [])
    if user is None:
        return None

    return User(**user)


@login_manager.request_loader
def request_loader(request):
    """: Authorize
    """
    user_id = request.args.get('userId') or request.form.get('userId')
    token = request.args.get('token') or request.form.get('token')

    if not (user_id and token):
        return None

    token = Token.p_col.find_one({
        Token.Field.userId: user_id,
        Token.Field.token: token
    })
    if token is None:
        return None

    user = User.p_col.find_one({User.Field._id: user_id})
    if user is None:
        return None

    return User(**user)
