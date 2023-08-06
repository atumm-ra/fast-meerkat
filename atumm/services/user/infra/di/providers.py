from injector import Binder, Module, singleton
from motor.motor_asyncio import AsyncIOMotorClient

from atumm.services.user.dataproviders.beanie.repositories import UserRepo
from atumm.services.user.domain.repositories import AbstractUserRepo


class UserRepoProvider(Module):
    def configure(self, binder: Binder):
        binder.bind(AbstractUserRepo, to=UserRepo(), scope=singleton)


user_providers = [UserRepoProvider]
