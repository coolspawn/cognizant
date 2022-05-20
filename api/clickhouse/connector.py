from clickhouse_driver import Client

ch_client = Client('localhost')
quote = '"{0}"'.format


class CHWriter(object):
    def __init__(self, table, db):
        self.table = table
        self.db = db

    def write_data(self, data):
        if not data:
            return
        column_list = ', '.join(data[0].dict().keys())
        for obj in data:
            query = 'insert into {}.{} ({}) values'.format(self.db, self.table, column_list)
            ch_client.execute(query, params=[obj.dict()])
