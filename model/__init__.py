# -*- coding: utf-8 -*-
# ------------------------------------------------
# MongoDB Client
# ------------------------------------------------
from .configs import (
    MONGO_PWD,
    MONGO_HOST,
    MONGO_USER,
    MONGO_REPLICA,
    MONGO_DATABASE,
    IS_MONGO_AUTH,
    IS_MONGO_REPLICA,
)
from pymongo import MongoClient


if IS_MONGO_REPLICA:
    mongo_url = 'mongodb://%s/?replicaSet=%s' % (MONGO_HOST, MONGO_REPLICA)
else:
    mongo_url = MONGO_HOST

mongo_client = MongoClient(mongo_url, connect=False)
mongo_db = mongo_client[MONGO_DATABASE]

if IS_MONGO_AUTH:
    mongo_db.authenticate(MONGO_USER, MONGO_PWD)

