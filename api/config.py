import os

from pydantic import BaseSettings


class GlobalConfig(BaseSettings):
    DEBUG = False
    TIMEZONE = "UTC"
    SERVICE_NAME = "Weather API"
    DESCRIPTION = "production"
    ENVIRONMENT = os.environ.get("ENVIRONMENT", "LOCAL")
    VERSION = '1.0'
    SERVERS = [{'url': 'http://0.0.0.0:8000'}]
    DB_NAME = 'db_weather'

    CH_HOST = 'ch_server'
    CH_PORT = 8123
    CH_PROT = 'http'

    CH_URL = f'{CH_PROT}://{CH_HOST}:{CH_PORT}/'
    CH_SUBS = ['ch-sub-1', 'ch-sub-2']

    CELERY_BACKEND = 'redis'
    CELERY_BROKER = 'rabbit_mq'
    CELERY_PATH = 'api.celery_app'
    CELERY_TASK_INTERVAL = 300


class DevConfig(GlobalConfig):
    DESCRIPTION = "dev"
    DEBUG = True


class LocalConfig(GlobalConfig):
    DESCRIPTION = "local"
    DEBUG = True
    TESTING = True
    CH_HOST = 'localhost'
    CH_URL = 'http://localhost:8123'
    CELERY_BACKEND = 'localhost'
    CELERY_BROKER = 'localhost'

class CurrentConfig:

    def __init__(self, environment):
        self.environment = environment

    def __call__(self):
        if self.environment == "LOCAL":
            return LocalConfig()
        return DevConfig()


config = CurrentConfig(GlobalConfig().ENVIRONMENT)()
