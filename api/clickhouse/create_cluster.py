from clickhouse_driver import Client

from api.config import config


def create_cluster():
    for sub in config.CH_SUBS:
        client = Client(sub, port=9000)
        with open('api/clickhouse/db_struct.ddl', 'r') as f:
            ddl = f.read()
            for command in ddl.split(';'):
                if command:
                    client.execute(command)

    client = Client(config.CH_HOST, port=9000)
    with open('api/clickhouse/db_struct_master.ddl', 'r') as f:
        ddl = f.read()
        for command in ddl.split(';'):
            if command:
                client.execute(command)
