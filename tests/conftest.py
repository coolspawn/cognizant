from random import randrange

import pytest
import pytest_asyncio
from aiohttp.test_utils import TestClient

from api.clickhouse.connector import ch_client
from api.clickhouse.create_cluster import create_cluster
from api.clickhouse.delete_cluster import delete_cluster
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
    delete_cluster()
    create_cluster()
    yield
    delete_cluster()


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
        "dt": 1653126543 + randrange(10, 3600),
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
