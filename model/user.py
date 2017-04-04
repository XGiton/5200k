# -*- coding: utf-8 -*-
from flask.ext.login import UserMixin
from model import mongo_db
from pymongo.collection import Collection
from pymongo.read_preferences import ReadPreference


class User(UserMixin):
    """
    * `_id`
    * `username` (string)
    * `pwdMd5` (string)

    ---
    """

    COL_NAME = 'user'
    p_col = Collection(mongo_db, COL_NAME,
                       read_preference=ReadPreference.PRIMARY_PREFERRED)
    s_col = Collection(mongo_db, COL_NAME,
                       read_preference=ReadPreference.SECONDARY_PREFERRED)

    class Field(object):
        _id = '_id'
        username = 'username'
        pwdMd5 = 'pwdMd5'

    def __init__(self, **kwargs):
        UserMixin.__init__(self)
        for k, v in kwargs.items():
            self.__setattr__(k, v)

    def get_id(self):
        return self._id
