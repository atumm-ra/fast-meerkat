from injector import Binder, Module, singleton

from atumm.core.infra.config import Config
from atumm.services.user.dataproviders.beanie.repositories import UserRepo
from atumm.services.user.domain.repositories import AbstractUserRepo
from atumm.services.user.domain.services import PasswordHasher


class UserRepoProvider(Module):
    def configure(self, binder: Binder):
        binder.bind(
            AbstractUserRepo,
            to=UserRepo(PasswordHasher(self.__injector__.get(Config).PASSWORD_KEY)),
            scope=singleton,
        )


user_providers = [UserRepoProvider]
