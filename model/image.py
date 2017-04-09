# -*- coding: utf-8 -*-
from model import mongo_db
from pymongo.collection import Collection
from pymongo.read_preferences import ReadPreference


class Image(object):
    """
    * `_id`
    * `url` (str)
    * `width` (int) - 宽
    * `height` (int) - 高

    ---
    """

    COL_NAME = 'image'
    p_col = Collection(mongo_db, COL_NAME,
                       read_preference=ReadPreference.PRIMARY_PREFERRED)
    s_col = Collection(mongo_db, COL_NAME,
                       read_preference=ReadPreference.SECONDARY_PREFERRED)

    class Field(object):
        _id = '_id'
        url = 'url'
        width = 'width'
        height = 'height'

    p_col.create_index(Field.url, unique=True)
