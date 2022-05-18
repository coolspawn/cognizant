import os

from celery import Celery

celery_instance = None

# running without docker
if not bool(os.getenv('DOCKER')):
    celery_instance = Celery(
        "worker",
        backend="redis://test:test@localhost:6379/0",
        broker="amqp://test:test@localhost:5672//"
    )
    celery_instance.conf.task_routes = {
        "celery_app.worker.get_weather_data": "test"}
else:
    # running with docker
    celery_instance = Celery(
        "worker",
        backend="redis://test:test@redis:6379/0",
        broker="amqp://test:test@rabbit_mq:5672//"
    )
    celery_instance.conf.task_routes = {
        "app.api.celery_app.worker.get_weather_data": "test"}

celery_instance.conf.update(task_track_started=True)
