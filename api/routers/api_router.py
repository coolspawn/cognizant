from datetime import datetime
from typing import Optional

from api.clickhouse.create_cluster import create_cluster
from api.weather_data.models import ApiV1HistoricalDataCapitalGetResponse, WeatherData
from api.weather_data.serializers import AsyncWeatherDataSerializer
from fastapi import APIRouter

ach_connector = AsyncWeatherDataSerializer()
api_router = APIRouter()


@api_router.get('/ping')
async def pong():
    return 'pong'


@api_router.post('/init_db')
async def initialize_db():
    create_cluster()
    return 'done!'


@api_router.get('/api/v1/historical-data/{capital}')
async def get_apiv1_historical_data_capital(
        capital: str,
        from_date: Optional[datetime] = None,
        till_date: Optional[datetime] = None,
        aggregation: Optional[str] = None,
        target: Optional[str] = None,
        cursor: Optional[float] = None,
        limit: Optional[int] = 100,
):
    params = {
        'capital': capital,
        'from_date': from_date,
        'till_date': till_date,
        'cursor': cursor,
        'limit': limit,
        'aggregation': aggregation,
        'target': target,
    }
    query_set = await ach_connector.get_queryset(**params)
    results = [WeatherData(**row) for row in query_set]
    if results:
        cursor = query_set[-1]['measure_date'].timestamp()
        params.update({'cursor': cursor})

    return ApiV1HistoricalDataCapitalGetResponse(results=results, **params)


@api_router.get('/api/v1/get_temperature/{capital}')
async def get_temperature_capital(
        capital: str,
        from_date: Optional[datetime] = None,
        till_date: Optional[datetime] = None,
        aggregation: Optional[str] = None,
):
    # just check request via shard poll without pandas

    params = {
        'capital': capital,
        'from_date': from_date,
        'till_date': till_date,
        'aggregation': aggregation,
    }
    query_set, host = await ach_connector.get_aggregated_queryset(**params)
    results = [WeatherData(**row) for row in query_set]
    if results:
        cursor = query_set[-1]['measure_date'].timestamp()
        params.update({'cursor': cursor})
        params.update({'target': host})

    return ApiV1HistoricalDataCapitalGetResponse(results=results, **params)
