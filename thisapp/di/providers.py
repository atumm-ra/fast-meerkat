from typing import List

from injector import Binder, Module, provider, singleton
from motor.motor_asyncio import AsyncIOMotorClient
from atumm.core.infra.config import Config
from atumm.services.user.infra.auth.tokenizer import Tokenizer

from thisapp.config import get_config


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


class ConfigProvider(Module):
    def configure(self, binder: Binder):
        binder.bind(Config, to=get_config(), scope=singleton)


app_providers: List = [ConfigProvider, AsyncMotorClientProvider, TokenizerProvider]
