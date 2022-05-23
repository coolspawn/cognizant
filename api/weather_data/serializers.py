import datetime

import pandas as pd
from asynch.cursors import DictCursor

from api.clickhouse.async_connector import db
from api.weather_data.models import WeatherData

tokens = {
    'capital': """city = '%s'""",
    'from_date': """measure_date >= '%s'""",
    'till_date': """measure_date <= '%s'""",
    'cursor': """measure_date > %s""",
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

    return query % params


async def get_aggregated_query(**kwargs):
    select = 'SELECT *'
    table_name = kwargs.get('table_name', 'db_weather.facts')
    conditions = await get_conditions(**kwargs)
    order_by = kwargs.get('order_by', 'ORDER BY measure_date')
    limit = kwargs.get('limit', 100)
    aggregation = kwargs.get('aggregation')
    params = {
        'select': select,
        'table_name': table_name,
        'conditions': conditions,
        'order_by': order_by,
        'limit': f'LIMIT {limit}',
    }
    query = f"""
            select 
            temp_agg.val as temperature,
            temp_agg.city as city,
            facts.measure_date
            From
            (SELECT {aggregation}(temperature) as val, city
            FROM {table_name}
            {conditions}
            group by city) as temp_agg
            left join 
            (select * from {table_name} {conditions}) as facts 
            on temp_agg.val = facts.temperature
        """

    return query


async def aggregate_rows(rows, column, func_name):
    df = pd.DataFrame(rows)
    aggs = {
        'max': df[df[column] == df[column].max()],
        'min': df[df[column] == df[column].min()],
        'avg': df[df[column] == df[column].median()],
    }

    return aggs.get(func_name).to_dict('records')


class WeatherDataSerializer:
    """Serializer for extracting data."""

    def serialize(self, raw_data):
        main = raw_data['main']
        wd_vals = {
            'city': raw_data['name'],
            'measure_date': datetime.datetime.fromtimestamp(raw_data['dt']),
            'temperature': main['temp'],
            'pressure': main['pressure'],
            'humidity': main['humidity'],
            'cloudiness': raw_data['clouds']['all'],
            'wind': raw_data['wind']['speed'],
        }
        return WeatherData(**wd_vals)


class AsyncWeatherDataSerializer:
    """Serializer for response."""

    async def get_queryset(self, **kwargs):
        agg_query = await get_query(**kwargs)
        shard_pool, host = await db.get_shard_pool()
        async with shard_pool.acquire() as conn:
            async with conn.cursor(cursor=DictCursor) as cursor:
                await cursor.execute(agg_query)
                all_rows = cursor.fetchall()
        agg_func = kwargs.get('aggregation')
        if agg_func and all_rows:
            target = kwargs.get('target')
            all_rows = await aggregate_rows(all_rows, target, agg_func)

        return all_rows

    async def get_aggregated_queryset(self, **kwargs):
        agg_query = await get_aggregated_query(**kwargs)
        shard_pool, host = await db.get_shard_pool()
        async with shard_pool.acquire() as conn:
            async with conn.cursor(cursor=DictCursor) as cursor:
                await cursor.execute(agg_query)
                all_rows = cursor.fetchall()

        return all_rows, host
