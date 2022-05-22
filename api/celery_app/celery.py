import os

from celery import Celery
from api.config import config


celery_instance = Celery(
    'tasks',
    backend=f'redis://{config.CELERY_BACKEND}:6379/0',
    broker=f'amqp://test:test@{config.CELERY_BROKER}:5672//',
    include=[f'{config.CELERY_PATH}.tasks'],
)

celery_instance.conf.beat_schedule = {
    'Collecting weather data': {
        'task': f'{config.CELERY_PATH}.tasks.collect_weather_data_from_source',
        'schedule': config.CELERY_TASK_INTERVAL,
    },
}
