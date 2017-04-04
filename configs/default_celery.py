# -*- coding: utf-8 -*-
from config.celery_config import DefaultCeleryConfig, create_celery_instance


celery_app = create_celery_instance('base_project',
                                    DefaultCeleryConfig,
                                    'redis://localhost:6379/0')
