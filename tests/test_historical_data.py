from datetime import datetime, timedelta

import pytest

from api.clickhouse.connector import CHWriter
from api.weather_data.models import WeatherData

pytestmark = pytest.mark.asyncio
rows_qty = 5

template = {
    'city': 'Vienna',
    'measure_date': datetime.utcnow(),
    'temperature': 29,
    'pressure': 1029,
    'humidity': 89,
    'cloudiness': 39,
    'wind': 9,
}

@pytest.fixture()
def weather_lines():
    weather_list = []

    for i in range(rows_qty):
        vals = {
            'city': 'Vienna',
            'measure_date': datetime.utcnow() + timedelta(minutes=5*i),
            'temperature': template['temperature'] + i,
            'pressure': template['pressure'] + i,
            'humidity': template['humidity'] + i,
            'cloudiness': template['cloudiness'] + i,
            'wind': template['wind'] + i,
        }
        weather_list.append(WeatherData(**vals))
    return weather_list


async def test_simple_get(async_client, weather_lines):
    w = CHWriter('facts', 'db_weather')
    w.write_data(weather_data=weather_lines)
    url = '/api/v1/historical_data/Vienna'
    from_date = (datetime.utcnow() + timedelta(minutes=6)).strftime("%Y-%m-%d %H:%M:%S")
    till_date = (datetime.utcnow() + timedelta(minutes=12)).strftime("%Y-%m-%d %H:%M:%S")
    end_date = (datetime.utcnow() + timedelta(minutes=26)).strftime("%Y-%m-%d %H:%M:%S")
    # TODO take care of time zone in cursor
    cursor = (datetime.now() + timedelta(minutes=26)).timestamp()
    cases = [
        (f'{url}', lambda l: len(l['results']), rows_qty),
        (f'{url}?limit=2', lambda l: len(l['results']), 2),
        (f'{url}?from_date={from_date}', lambda l: len(l['results']), rows_qty-2),
        (f'{url}?till_date={till_date}', lambda l: len(l['results']), 3),
        (f'{url}?from_date={from_date}&till_date={till_date}', lambda l: len(l['results']), 1),
        (f'{url}?cursor={cursor}', lambda l: len(l['results']), 0),
        (f'{url}?aggregation=max&target=pressure', lambda l: l['results'][0]['pressure'], template['pressure'] + rows_qty - 1),
        (f'{url}?aggregation=min&target=temperature', lambda l: l['results'][0]['temperature'], template['temperature']),
        (f'{url}?aggregation=avg&target=humidity', lambda l: l['results'][0]['humidity'], 91),
        (f'{url}?from_date={from_date}&till_date={end_date}&limit=2&aggregation=max&target=wind', lambda l: l['results'][0]['wind'], 12),
    ]
    response = await async_client.get(url)
    json_resp = response.json()
    assert json_resp['results']

    for path, result, expected in cases:
        response = await async_client.get(path)
        assert response.status_code == 200
        assert result(response.json()) == expected
