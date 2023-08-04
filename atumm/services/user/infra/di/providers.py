from injector import Binder, Module, provider, singleton
from motor.motor_asyncio import AsyncIOMotorClient

from thisapp.config import Config, get_config
from atumm.services.user.core.repositories import AbstractUserRepo
from atumm.services.user.dataproviders.beanie.repositories import UserRepo
from atumm.services.user.infra.auth.tokenizer import Tokenizer


class TokenizerProvider(Module):
    @singleton
    @provider
    def provide(self) -> Tokenizer:
        config: Config = get_config()
        return Tokenizer(config.JWT_SECRET_KEY, config.JWT_ALGORITHM)


class UserRepoProvider(Module):
    def configure(self, binder: Binder):
        binder.bind(AbstractUserRepo, to=UserRepo(), scope=singleton)


user_providers = [TokenizerProvider, UserRepoProvider]
