# -*- coding: utf-8 -*-
import requests
from bson import ObjectId
from datetime import datetime
from pymongo.errors import DuplicateKeyError

from flask import request, jsonify, session, abort
from flask_login import current_user, login_required, login_user, logout_user

from . import api, USER_ERROR
from configs import WX_APP_ID, WX_APP_SECRET
from model.user import User


class Error(object):
    USER_ERROR = 1000
    GET_SESSION_FROM_WX_FAILED = {
        'err': USER_ERROR + 1,
        'msg': 'Get session key from wx failed'
    }


@api.route('/user/login', methods=['POST'])
def login():
    """
    ## 登录

        POST '/api/user/login'

    Params:
    * `code` (str) - 微信登录code
    * `nick_name` (str) - 从微信获取
    * `avatar_url` (str) - 从微信获取
    * `gender` (int) - 从微信获取
        * `0` - 未知
        * `1` - 男
        * `2` - 女
    * `union_id` (str) - 从微信获取

    Returns:
    * `nick_name` (str) - 昵称
    * `avatar_url` (str) - 头像
    * `description` (str) - 介绍

    * `sessionId` (str)

    Errors: `1001`

    ---
    """
    code = request.form['code']
    # 从微信服务器获取session_key
    url = (
        'https://api.weixin.qq.com/sns/jscode2session?'
        'appid=%s&secret=%s&js_code=%s&grant_type=authorization_code'
    ) % (WX_APP_ID, WX_APP_SECRET, code)

    rsp = requests.get(url)
    if rsp.status_code / 100 != 2:
        return jsonify(stat=0, **Error.GET_SESSION_FROM_WX_FAILED), 400
    if 'openid' not in rsp.json():
        return jsonify(stat=0, **Error.GET_SESSION_FROM_WX_FAILED), 400
    openid = rsp.json()['openid']
    session_key = rsp.json()['session_key']

    user = User.p_col.find_one(
        {
            User.Field.openid: openid
        },
        [
            User.Field.nick_name,
            User.Field.avatar_url,
            User.Field.description,
            User.Field.gender
        ]
    )
    if user is None:
        # 注册用户
        user = {
            '_id': str(ObjectId()),
            User.Field.nick_name: request.form['nick_name'],
            User.Field.avatar_url: request.form['avatar_url'],
            User.Field.description: '',
            User.Field.gender: request.form.get('gender', 0, type=int),
            User.Field.openid: openid,
            User.Field.session_key: session_key
        }
        try:
            User.p_col.insert_one(user)
        except DuplicateKeyError:
            abort(400)

    # get sessionId
    session_id = session.sid
    # login user
    login_user(User(**user))

    return jsonify(stat=1, user_id=user['_id'], session_id=session_id)


@api.route('/user/profile', methods=['GET'])
@login_required
def get_current_user_profile():
    """
    ## 获取当前用户个人信息

        GET '/api/user/profile'

    Params:
    * `session_id` (str)

    Returns:
    * `nick_name` (str) - 昵称
    * `avatar_url` (str) - 头像
    * `description` (str) - 描述
    * `gender` (int) - 性别
        * `0` - 未知
        * `1` - 男
        * `2` - 女

    Errors:

    ---
    """
    user = User.s_col.find_one(
        {
            '_id': current_user['_id']
        },
        [
            User.Field.nick_name,
            User.Field.avatar_url,
            User.Field.description,
            User.Field.gender
        ]
    )

    return jsonify(stat=1, **user), 200
