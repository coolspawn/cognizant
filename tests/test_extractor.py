from api.celery_app.tasks import collect_weather_data_from_source
from api.weather_data.models import Cities


def test_extractor(mocker, ext_api_json_resp, clickhouse_client):
    mocker.patch('api.weather_data.extractor.WeatherProducer.get_weather_data', return_value=ext_api_json_resp)
    collect_weather_data_from_source()
    res = clickhouse_client.execute('SELECT * from db_weather.facts')
    assert res, 'No data in database'
    assert len(res) == len(Cities)
