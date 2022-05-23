import asynch
from aiochclient import ChClient
import aiohttp
from aiohttp import ClientSession

from api.clickhouse.create_cluster import create_cluster
from api.config import config
import logging

_logger = logging.getLogger(__name__)

class AsyncCHConnector:
    """Asyc connector for clichouse database."""

    def __init__(self):
        self.ahc_client = None
        self.pool = None
        self.shards = []
        self.shard_id = 0

    async def start_shards(self):
        for host in config.CH_SUBS + [config.CH_HOST]:
            shard_pool = await asynch.create_pool(minsize=10, maxsize=400, host=host, database=config.DB_NAME)
            self.shards.append((shard_pool, host))

    async def stop_shards(self):
        for _pool, host in self.shards:
            _pool.close()

    async def get_shard_pool(self):
        curr_pool, host = self.shards[self.shard_id]
        if self.shard_id < len(self.shards)-1:
            self.shard_id += 1
        else:
            self.shard_id = 0

        return curr_pool, host

    async def connect(self):
        self.pool = await asynch.create_pool(
            minsize=10,
            maxsize=400,
            host=config.CH_HOST,
            database=config.DB_NAME
        )

    async def disconnect(self):
        await self.pool.close()


def init_async_connector(app):
    async def start_app():
        create_cluster()
        await db.start_shards()
    return start_app


def close_async_connector(app):
    async def stop_app():
        await db.stop_shards()
    return stop_app


db = AsyncCHConnector()
