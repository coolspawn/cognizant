import pytest
import pytest_asyncio
from aiohttp.test_utils import TestClient

from api.clickhouse.async_connector import db
from api.clickhouse.connector import ch_client
from api.main import app
from httpx import AsyncClient


@pytest_asyncio.fixture()
def clickhouse_client():
    yield ch_client

@pytest.fixture()
def ord_client():
    yield TestClient(app)

@pytest_asyncio.fixture(autouse=True)
async def database():
    ch_client.execute('DROP DATABASE IF EXISTS db_weather')
    with open('api/clickhouse/db_struct.ddl', 'r') as f:
        ddl = f.read()
        for command in ddl.split(';'):
            if command:
                ch_client.execute(command)
    await db.connect()
    yield
    ch_client.execute('DROP DATABASE IF EXISTS db_weather')
    await db.disconnect()


@pytest_asyncio.fixture()
async def async_client():
    async with AsyncClient(app=app, base_url='http://test') as ac:
        yield ac


@pytest.fixture()
def ext_api_json_resp():
    resp = {
        "coord": {
            "lon": 16.3721,
            "lat": 48.2085
        },
        "weather": [
            {
                "id": 802,
                "main": "Clouds",
                "description": "scattered clouds",
                "icon": "03d"
            }
        ],
        "base": "stations",
        "main": {
            "temp": 23.7,
            "feels_like": 23.48,
            "temp_min": 21.73,
            "temp_max": 25.26,
            "pressure": 1018,
            "humidity": 52
        },
        "visibility": 10000,
        "wind": {
            "speed": 12.52,
            "deg": 325,
            "gust": 21.01
        },
        "clouds": {
            "all": 40
        },
        "dt": 1653126543,
        "sys": {
            "type": 2,
            "id": 2037452,
            "country": "AT",
            "sunrise": 1653102500,
            "sunset": 1653158048
        },
        "timezone": 7200,
        "id": 2761369,
        "name": "Vienna",
        "cod": 200
    }
    yield resp


@pytest.fixture()
def request_cases():
    url = '/api/v1/historical_data'
    cases = [
        (f'{url}/Vienna'),
        (f'{url}/Vienna?limit=2', lambda l: len(l)),
        (f'{url}/Vienna?from_date=2022-05-19'),
        (f'{url}/Vienna?till_date=2022-05-21'),
        (f'{url}/Vienna?from_date=2022-05-19&till_date=2022-05-21'),
        (f'{url}/Vienna?cursor=1652995527.0'),
        (f'{url}/Vienna?aggregation=max&target=pressure'),
        (f'{url}/Vienna?aggregation=min&target=temperature'),
        (f'{url}/Vienna?aggregation=avg&target=humidity'),
        (f'{url}/Vienna?from_date=2022-05-19&till_date=2022-05-21&limit=1&aggregation=max&target=wind'),
    ]
    yield cases
