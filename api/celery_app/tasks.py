from api.celery_app.celery import celery_instance
from celery.utils.log import get_task_logger

from api.weather_data.extractor import WeatherProducer
from api.weather_data.serializers import WeatherDataSerializer
from api.clickhouse.connector import CHWriter
from api.weather_data.models import Cities

celery_log = get_task_logger(__name__)
feeder = WeatherProducer()
loader = CHWriter('facts', 'db_weather')
serializer = WeatherDataSerializer()


@celery_instance.task
def collect_weather_data_from_source():
    ts_data = []
    for city in Cities:
        data = feeder.get_weather_data(city=city.value)
        pd_obj = serializer.serialize(data)
        ts_data.append(pd_obj)
    loader.write_data(ts_data)
