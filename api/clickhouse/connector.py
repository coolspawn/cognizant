from clickhouse_driver import Client
from api.config import config

ch_client = Client(config.CH_HOST)
quote = '"{0}"'.format


class CHWriter(object):
    """Write weather data into clickhouse database."""
    def __init__(self, table, db_name):
        self.table = table
        self.db_name = db_name

    def write_data(self, weather_data):
        if not weather_data:
            return
        column_list = ', '.join(weather_data[0].dict().keys())
        for weather_obj in weather_data:
            query = 'insert into {}.{} ({}) values'.format(self.db_name, self.table, column_list)
            ch_client.execute(query, params=[weather_obj.dict()])
