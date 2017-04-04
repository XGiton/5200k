# -*- coding: utf-8 -*-
# --- Redis Cache ---
from configs import (
    REDIS_NAME,
    REDIS_DB,
    REDIS_PWD,
    REDIS_0_HOST,
    REDIS_0_PORT,
    REDIS_1_HOST,
    REDIS_1_PORT,
    IS_REPLICA,
)


if IS_REPLICA:
    from redis.sentinel import Sentinel
    redis_sentinel = Sentinel(
        [(REDIS_0_HOST, REDIS_0_PORT), (REDIS_1_HOST, REDIS_1_PORT)],
        password=REDIS_PWD,
        db=REDIS_DB
    )
    r = redis_sentinel.master_for(REDIS_NAME)
else:
    import redis
    r = redis.StrictRedis(host=REDIS_0_HOST, port=REDIS_0_PORT, db=REDIS_DB)
