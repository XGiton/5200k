# -*- coding: utf-8 -*-
from model import mongo_db
from pymongo.collection import Collection
from pymongo.read_preferences import ReadPreference


class Setting(object):
    """
    * `_id`

    ---
    """

    COL_NAME = 'setting'
    p_col = Collection(mongo_db, COL_NAME,
                       read_preference=ReadPreference.PRIMARY_PREFERRED)
    s_col = Collection(mongo_db, COL_NAME,
                       read_preference=ReadPreference.SECONDARY_PREFERRED)

    class Field(object):
        _id = '_id'
