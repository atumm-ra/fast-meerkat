from injector import Binder, Module, provider, singleton
from motor.motor_asyncio import AsyncIOMotorClient

from atumm.app.infra.config import Config, get_config
from atumm.user.core.repositories import AbstractUserRepo
from atumm.user.dataproviders.beanie.repositories import UserRepo
from atumm.user.infra.auth.tokenizer import Tokenizer


class TokenizerProvider(Module):
    @singleton
    @provider
    def provide(self) -> Tokenizer:
        config: Config = get_config()
        return Tokenizer(config.JWT_SECRET_KEY, config.JWT_ALGORITHM)


class UserRepoProvider(Module):
    def configure(self, binder: Binder):
        motor_client = self.__injector__.get(AsyncIOMotorClient)
        binder.bind(AbstractUserRepo, to=UserRepo(motor_client), scope=singleton)


user_providers = [TokenizerProvider, UserRepoProvider]
