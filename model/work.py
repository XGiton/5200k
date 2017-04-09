# -*- encoding: utf-8 -*-
from model import mongo_db
from pymongo.collection import Collection
from pymongo.read_preferences import ReadPreference


class Work(object):
    """
    * `_id`
    * `user_id` (str) - 用户id
    * `image_ids` (list of str) - 图片id列表
    * `description` (str) - 描述
    * `create_time` (datetime utcnow) - 创建时间
    * `like_no` (int) - 点赞数

    ---
    """

    COL_NAME = 'work'
    p_col = Collection(mongo_db, COL_NAME,
                       read_preference=ReadPreference.PRIMARY_PREFERRED)
    s_col = Collection(mongo_db, COL_NAME,
                       read_preference=ReadPreference.SECONDARY_PREFERRED)

    class Field(object):
        _id = '_id'
        user_id = 'user_id'
        image_ids = 'image_ids'
        description = 'description'
        create_time = 'create_time'
        like_no = 'like_no'

    p_col.create_index(Field.user_id, unique=False, sparse=False)
