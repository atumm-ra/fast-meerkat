from typing import List

from atumm.extensions.beanie.di import AsyncMotorClientProvider
from atumm.extensions.config import Config
from atumm.extensions.fastapi.di import AuthenticationBackendProvider
from atumm.extensions.services.tokenizer.base import BaseTokenizer
from atumm.extensions.services.tokenizer.jwt_tokenizer import JWTTokenizer
from injector import Module, provider, singleton

from thisapp.config import ConfigProvider


class TokenizerProvider(Module):
    @singleton
    @provider
    def provide(self, config: Config) -> BaseTokenizer:
        return JWTTokenizer(config.JWT_SECRET_KEY, 3600)


app_providers: List = [
    ConfigProvider,
    AsyncMotorClientProvider,
    TokenizerProvider,
    AuthenticationBackendProvider,
]
