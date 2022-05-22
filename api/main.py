import os

from api.clickhouse.async_connector import (close_async_connector,
                                            init_async_connector)
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routers.api_router import api_router
from api.config import config


def get_application():
    application = FastAPI(
        title=config.DESCRIPTION,
        version=config.VERSION,
        servers=config.SERVERS,
        debug=config.DEBUG,
    )
    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
        allow_credentials=True,
    )

    application.add_event_handler("startup", init_async_connector(application))
    application.add_event_handler("shutdown", close_async_connector(application))

    application.include_router(api_router)

    return application


app = get_application()
