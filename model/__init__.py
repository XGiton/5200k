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


# ------------------------------------------------
# MySQL Client
# ------------------------------------------------
from model.config import (
    MYSQL_USER,
    MYSQL_PWD,
    MYSQL_HOST,
    MYSQL_DATABASE,
    MYSQL_HA_PWD,
    MYSQL_HA_HOST,
    MYSQL_HA_PORT,
    MYSQL_HA_USER,
)
from mysql.connector.connection import MySQLConnection


class MySQLConnectionWrap(MySQLConnection):

    """A wrap of MySQLConnection class. Add with statement support."""

    def __init__(self, **kwargs):
        """Init a new connection instance """
        MySQLConnection.__init__(self)
        self.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PWD,
            database=MYSQL_DATABASE,
            **kwargs
        )

    def __enter__(self):
        return self

    def __exit__(self, type, value, trace):
        self.close()


class MySQLSlaveConnectionWrap(MySQLConnection):

    """A wrap of MySQLConnection class.

    This class iwll connect to haproxy which load balancing for mysql slaves

    **Note:** This class can only be used for query, not for update, insert
    or delete
    """

    def __init__(self, **kwargs):
        """Init a new connection instance """
        MySQLConnection.__init__(self)
        self.connect(
            host=MYSQL_HA_HOST,
            port=MYSQL_HA_PORT,
            user=MYSQL_HA_USER,
            password=MYSQL_HA_PWD,
            database=MYSQL_DATABASE,
            **kwargs
        )

    def __enter__(self):
        return self

    def __exit__(self, type, value, trace):
        self.close()


from . import setting
