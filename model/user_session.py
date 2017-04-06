#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pymongo import ASCENDING
from pymongo.collection import Collection
from pymongo.read_preferences import ReadPreference

from . import mongo_db


class UserSession(object):
    """
    * `_id` (str) - Session id
    * `user_id` (str)
    * `session` (str) *optional* - Serialized session dict data
    * `s_type` (int) - Session type
    * `update_time` (datetime)
    * `openid` (str) - 微信openid
    * `session_key` (str) - 微信session_key

    ---
    """
    COL_NAME = 'user_session'
    p_col = Collection(
        mongo_db, COL_NAME, read_preference=ReadPreference.PRIMARY_PREFERRED
    )
    s_col = Collection(
        mongo_db, COL_NAME, read_preference=ReadPreference.SECONDARY_PREFERRED
    )

    class Field(object):
        _id = '_id'
        user_id = 'user_id'
        session = 'session'
        s_type = 's_type'
        update_time = 'update_time'
        openid = 'openid'
        session_key = 'session_key'

    p_col.create_index(Field.update_time, expireAfterSeconds=60*60*24*30)
