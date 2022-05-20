
from celery import Celery

celery_instance = Celery(
    "tasks",
    backend="redis://127.0.0.1:6379/0",
    broker="amqp://test:test@localhost:5672//",
    include=['api.celery_app.tasks'],
)

celery_instance.conf.beat_schedule = {
    'Collecting weather data': {
        'task': 'api.celery_app.tasks.collect_weather_data_from_source',
        'schedule': 300.0,
    },
}
