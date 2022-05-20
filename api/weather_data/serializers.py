import datetime
import pandas as pd

from aiochclient import ChClient
from aiohttp import ClientSession
from api.weather_data.models import WeatherData

tokens = {
    'capital': """city = '%s'""",
    'from_date': """measure_date >= '%s'""",
    'till_date': """measure_date <= '%s'""",
    'cursor': """measure_date > '%s'""",
}


async def get_conditions(**kwargs):
    res = ''
    params = []
    for k, v in kwargs.items():
        tok = tokens.get(k)
        if tok and v:
            params.append(tok % v)

    cond = ' AND '.join(params)
    if cond:
        res = f' WHERE {cond}'
    return res


async def get_query(**kwargs):
    select = 'SELECT *'
    table_name = kwargs.get('table_name', 'db_weather.facts')
    conditions = await get_conditions(**kwargs)
    order_by = kwargs.get('order_by', 'ORDER BY measure_date')
    limit = kwargs.get('limit', 100)

    params = {
        'select': select,
        'table_name': table_name,
        'conditions': conditions,
        'order_by': order_by,
        'limit': f'LIMIT {limit}',
    }
    query = '%(select)s FROM %(table_name)s %(conditions)s %(order_by)s %(limit)s'
    query = query % params
    return query


async def aggregate_rows(rows, column, func_name):
    df = pd.DataFrame(rows)
    aggs = {
        'max': df[df[column] == df[column].max()],
        'min': df[df[column] == df[column].min()],
        'avg': df[df[column] == df[column].median()],
    }

    agg_rows = aggs.get(func_name).to_dict('records')
    return agg_rows


class WeatherDataSerializer:

    def serialize(self, raw_data):
        main = raw_data['main']
        wd_vals = {
            'city': raw_data['name'],
            'measure_date': datetime.datetime.fromtimestamp(raw_data['dt']),
            'temperature': main['temp'],
            'pressure': main['pressure'],
            'humidity': main['humidity'],
            'cloudiness': raw_data['clouds']['all'],
            'wind': raw_data['wind']['speed']
        }
        wd = WeatherData(**wd_vals)
        return wd


class AsyncWeatherDataSerializer:
    def __init__(self):
        self.ahc_client = None

    async def connect(self):
        s = ClientSession()
        self.ahc_client = ChClient(s, database='db_weather')
        await self.ahc_client.is_alive()

    async def disconnect(self):
        await self.ahc_client.close()

    async def get_queryset(self, **kwargs):
        agg_query = await get_query(**kwargs)
        all_rows = await self.ahc_client.fetch(agg_query)
        agg_func = kwargs.get('aggregation')
        if agg_func:
            target = kwargs.get('target')
            all_rows = await aggregate_rows(all_rows, target, agg_func)

        return all_rows
