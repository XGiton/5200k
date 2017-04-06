import subprocess

from base64 import b64encode
from datetime import datetime
from uuid import uuid4

from flask import (
    Flask,
    jsonify,
)
from flask.sessions import SecureCookieSessionInterface, SessionMixin
from flask_login import LoginManager
from configs import (
    DEBUG,
    SECRET_KEY,
    ROOT_PATH,
)
from model.user import User
from model.user_session import UserSession
from werkzeug.datastructures import CallbackDict


# Init Flask app
app = Flask(__name__)
app.debug = DEBUG

# Set session configs
app.session_cookie_name = 'sessionId'
app.secret_key = SECRET_KEY


class MongoSession(CallbackDict, SessionMixin):
    def __init__(self, initial=None, sid=None):
        CallbackDict.__init__(self, initial)
        self.sid = sid
        self.modified = False


class MongoSessionInterface(SecureCookieSessionInterface):
    """Extend default session interface to store and get session from mongodb.
    We just override open_session and save_session functions.
    See: pymongo.sessions.SecureCookieSessionInterface
    """
    session_class = MongoSession

    def open_session(self, app, request):
        # get session id
        sid = None
        # try to get from request params
        if request.method in ('POST', 'PUT'):
            sid = request.form.get(app.session_cookie_name)
        elif request.method in ('GET', 'DELETE'):
            sid = request.args.get(app.session_cookie_name)

        if sid is None:
            sid = b64encode(str(uuid4()))
            return self.session_class(sid=sid)

        # try to loads data from mongodb
        query = {'_id': sid}
        user_session = UserSession.p_col.find_one(
            query,
            [UserSession.Field.session]
        )
        if user_session is None:
            sid = b64encode(str(uuid4()))
            return self.session_class(sid=sid)

        return self.session_class(
            initial=user_session.get(UserSession.Field.session, None),
            sid=sid
        )

    def save_session(self, app, session, response):
        domain = self.get_cookie_domain(app)
        path = self.get_cookie_path(app)
        if not session:
            response.delete_cookie(app.session_cookie_name,
                                   domain=domain, path=path)
            return

        httponly = self.get_cookie_httponly(app)
        secure = self.get_cookie_secure(app)
        expires = self.get_expiration_time(app, session)
        sid = session.sid
        update_dic = {
            UserSession.Field.session: dict(session)
        }
        user_id = session.get('user_id')
        if user_id is not None:
            update_dic[UserSession.Field.user_id] = user_id

        # update mongodb
        now = datetime.utcnow()
        if sid is not None:
            UserSession.p_col.update(
                {
                    '_id': sid
                },
                {
                    '$set': update_dic,
                    '$setOnInsert': {
                        '_id': sid,
                        UserSession.Field.update_time: now
                    }
                },
                upsert=True
            )
        else:
            # insert new session record
            update_dic['_id'] = b64encode(str(uuid4()))
            update_dic[UserSession.Field.update_time] = now
            sid = UserSession.p_col.insert_one(update_dic)

        # set cookies
        response.set_cookie(app.session_cookie_name, sid,
                            expires=expires,
                            httponly=httponly,
                            domain=domain,
                            path=path,
                            secure=secure)


# Init login manager
login_manager = LoginManager()
login_manager.init_app(app)
app.session_interface = MongoSessionInterface()


@login_manager.user_loader
def load_user(user_id):
    user = User.p_col.find_one({'_id': user_id})
    if user is None:
        return None
    return User(**user)


@login_manager.request_loader
def request_callback(request):
    """
    Will call this each time need to verify login status
    Args:
        request: Flask Request object

    Returns:
        user: User object or None

    """
    # check if there is `session_id` in request params
    if request.method in ('POST', 'PUT'):
        session_id = request.form.get('sessionId')
    elif request.method in ('GET', 'DELETE'):
        session_id = request.args.get('sessionId')
    else:
        session_id = None

    if session_id is not None:
        # get user
        query = {'_id': session_id}
        user_session = UserSession.p_col.find_one(
            query,
            [UserSession.Field.user_id]
        )
        if user_session is None or \
                UserSession.Field.user_id not in user_session:
            return None
        user = User.s_col.find_one(
            {
                '_id': user_session[UserSession.Field.user_id]
            }
        )
        if user is None:
            return None
        return User(**user)

    return None


@app.route('/git/hook', methods=['POST'])
def git_hook():
    """Accept git hook push, and pull the latest code."""
    subprocess.Popen(
        'git pull && git submodule update', cwd=ROOT_PATH, shell=True
    )
    return 'ok'


@app.errorhandler(400)
def handle_400(e):
    err = {'err': 0, 'msg': 'Bad Request'}
    return jsonify(stat=0, **err), 400


@app.errorhandler(401)
def handle_401(e):
    err = {'err': 1, 'msg': 'Unauthorized'}
    return jsonify(stat=0, **err), 401


@app.errorhandler(403)
def handle_403(e):
    err = {'err': 2, 'msg': 'Forbidden'}
    return jsonify(stat=0, **err), 403


@app.errorhandler(404)
def handle_404(e):
    err = {'err': 3, 'msg': 'Not Found'}
    return jsonify(stat=0, **err), 404
