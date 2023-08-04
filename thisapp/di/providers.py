from typing import List

from injector import Module, provider, singleton
from motor.motor_asyncio import AsyncIOMotorClient

from thisapp.config import Config, get_config


class AsyncMotorClientProvider(Module):
    @provider
    @singleton
    def provide_async_motor(self) -> AsyncIOMotorClient:
        config: Config = get_config()
        return AsyncIOMotorClient(config.MONGO_URL)


app_providers: List = [AsyncMotorClientProvider]
