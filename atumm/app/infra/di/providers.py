from typing import List

from injector import Module, provider, singleton

from atumm.app.infra.config import Config, get_config
from motor.motor_asyncio import AsyncIOMotorClient


class AsyncMotorClientProvider(Module):
    @provider
    @singleton
    def provide_async_motor(self) -> AsyncIOMotorClient:
        config: Config = get_config()
        if config.STAGE == "test":
            from mongomock_motor import AsyncMongoMockClient

            beanie_client = AsyncMongoMockClient()
        else:
            beanie_client = AsyncIOMotorClient(config.MONGO_URL)
        return beanie_client


app_providers: List = [
    AsyncMotorClientProvider
]