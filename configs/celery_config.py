# -*- coding: utf-8 -*-
import datetime
from celery import Celery
from celery.schedules import crontab


class BaseCeleryConfig(object):
    """Celery配置的基类.
    其他的Celery配置类都继承该基类
    """
    CELERY_TASK_SERIALIZER = 'json'
    CELERY_RESULT_SERIALIZER = 'json'
    CELERYD_CONCURRENCY = 4
    CELERY_ACKS_LATE = True
    CELERY_IGNORE_RESULT = True
    CELERY_STORE_ERRORS_EVEN_IF_IGNORED = True
    CELERYD_PREFETCH_MULTIPLIER = 1
    CELERY_EVENT_QUEUE_EXPIRES = 7200
    CELERY_TIMEZONE = 'UTC'


class DefaultCeleryConfig(BaseCeleryConfig):
    """App Celery 配置类"""
    CELERY_IMPORTS = (
        'lib.send_email',
    )

    CELERY_ROUTES = {
        'send_error_email': {
            'queue': 'send.error.email',
            'routing_key': 'send.error.email',
        },
    }
    CELERY_QUEUES = {
        'send.error.email': {
            'exchange': 'send.error.email',
            'exchange_type': 'direct',
            'routing_key': 'send.error.email',
        },
    }


def create_celery_instance(name, config, broker_url):
    """创建celery 实例
    :name - celery 实例名
    :configs - celery 配置
    :return - celery 实例
    """
    inst = Celery(name, broker=broker_url)
    inst.config_from_object(config)

    return inst
