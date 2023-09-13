from typing import List

from atumm.core.infra.config import Config, configure
from atumm.extensions.di.fastapi import AuthBackendProvider
from atumm.services.user.infra.auth.tokenizer import Tokenizer
from injector import Binder, Module, provider, singleton
from motor.motor_asyncio import AsyncIOMotorClient

from thisapp.config import ConfigProvider


class AsyncMotorClientProvider(Module):
    @provider
    @singleton
    def provide_async_motor(self) -> AsyncIOMotorClient:
        config: Config = self.__injector__.get(Config)
        return AsyncIOMotorClient(config.MONGO_URL)


class TokenizerProvider(Module):
    @singleton
    @provider
    def provide(self) -> Tokenizer:
        config: Config = self.__injector__.get(Config)
        return Tokenizer(config.JWT_SECRET_KEY, config.JWT_ALGORITHM)


app_providers: List = [
    ConfigProvider,
    AsyncMotorClientProvider,
    TokenizerProvider,
    AuthBackendProvider,
]
