from datetime import datetime
from typing import Optional

from api.clickhouse.connector import ch_client
from api.weather_data.models import ApiV1HistoricalDataCapitalGetResponse, WeatherData
from api.weather_data.serializers import AsyncWeatherDataSerializer
from fastapi import APIRouter

ach_connector = AsyncWeatherDataSerializer()
api_router = APIRouter()

@api_router.get('/ping')
async def pong():
    return pong

@api_router.get('/init_db')
async def initialize_db():
    # client does not suport multiple statement
    # TODO make async put into config or make via os
    with open('api/clickhouse/db_struct.ddl', 'r') as f:
        ddl = f.read()
        for command in ddl.split(';'):
            if command:
                ch_client.execute(command)
    return 'done!'


@api_router.get('/api/v1/historical_data/{capital}')
async def get_api_v1_historical_data_capital(
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
