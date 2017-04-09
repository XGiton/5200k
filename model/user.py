# -*- coding: utf-8 -*-
from flask_login import UserMixin
from model import mongo_db
from pymongo.collection import Collection
from pymongo.read_preferences import ReadPreference


class User(UserMixin):
    """
    * `_id`
    * `nick_name` (str) - 用户名
    * `avatar_url` (str) - 头像
    * `description` (str) - 个人介绍
    * `gender` (int) - 性别
        * `0` - 未知
        * `1` - 男
        * `2` - 女
    * `openid` (str) - 微信openid(该数据不能返回前端，用作用户的唯一标识)
    * `session_key` (str) - 微信session key(该数据不能返回前端)
    * `create_time` (datetime utcnow) - 创建时间

    ---
    """

    COL_NAME = 'user'
    p_col = Collection(mongo_db, COL_NAME,
                       read_preference=ReadPreference.PRIMARY_PREFERRED)
    s_col = Collection(mongo_db, COL_NAME,
                       read_preference=ReadPreference.SECONDARY_PREFERRED)

    class Field(object):
        _id = '_id'
        nick_name = 'nick_name'
        avatar_url = 'avatar_url'
        description = 'description'
        gender = 'gender'
        openid = 'openid'
        session_key = 'session_key'
        create_time = 'create_time'

    class Gender(object):
        """ 性别"""
        unknown = 0
        male = 1
        female = 2

    def __init__(self, **kwargs):
        UserMixin.__init__(self)
        for k, v in kwargs.items():
            self.__setattr__(k, v)

    def get_id(self):
        return self._id

    p_col.create_index(Field.openid, unique=True, sparse=True)
