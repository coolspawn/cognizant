from clickhouse_driver import Client

from api.config import config


def delete_cluster():
    for sub in config.CH_SUBS:
        client = Client(sub, port=9000)
        client.execute("DROP DATABASE IF EXISTS db_weather")

    client = Client(config.CH_HOST, port=9000)
    client.execute("DROP DATABASE IF EXISTS db_weather")
