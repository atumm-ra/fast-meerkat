from typing import List

from injector import Module, provider, singleton
from motor.motor_asyncio import AsyncIOMotorClient
from atumm.services.user.infra.auth.tokenizer import Tokenizer

from thisapp.config import Config, get_config


class AsyncMotorClientProvider(Module):
    @provider
    @singleton
    def provide_async_motor(self) -> AsyncIOMotorClient:
        config: Config = get_config()
        return AsyncIOMotorClient(config.MONGO_URL)

class TokenizerProvider(Module):
    @singleton
    @provider
    def provide(self) -> Tokenizer:
        config: Config = get_config()
        return Tokenizer(config.JWT_SECRET_KEY, config.JWT_ALGORITHM)


app_providers: List = [AsyncMotorClientProvider, TokenizerProvider]
