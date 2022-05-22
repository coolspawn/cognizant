from aiochclient import ChClient
from aiohttp import ClientSession
from api.config import config


class AsyncCHConnector:
    """Asyc connector for clichouse database."""

    def __init__(self):
        self.ahc_client = None

    async def connect(self):
        session = ClientSession()
        self.ahc_client = ChClient(
            session,
            url=config.CH_URL,
            database=config.DB_NAME,
        )
        await self.ahc_client.is_alive()

    async def disconnect(self):
        await self.ahc_client.close()


def init_async_connector(app):
    async def start_app():
        await db.connect()

    return start_app


def close_async_connector(app):
    async def stop_app():
        await db.disconnect()

    return stop_app


db = AsyncCHConnector()
