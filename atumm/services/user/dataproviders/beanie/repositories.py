from typing import List

import pymongo

from atumm.core.data_providers.datastore.exceptions import DuplicateKeyException
from atumm.services.user.core.models import UserModel
from atumm.services.user.core.repositories import AbstractUserRepo
from atumm.services.user.dataproviders.beanie.models import User


class UserRepo(AbstractUserRepo):
    async def create(self, username: str, password: str, email: str) -> UserModel:
        user = User(email=email, password=password, username=username)
        user.encrypt_password()

        try:
            await User.insert_one(user)
        except pymongo.errors.DuplicateKeyError as e:
            raise DuplicateKeyException(e.details["keyValue"])
        return user

    async def find_by_email(self, email: str) -> User:
        return await User.find_one(User.email == email)

    async def find_all(self, start: int = 0, limit: int = 12) -> List[UserModel]:
        user_list = await User.find().skip(start).to_list(limit)
        return user_list

    async def save(self, user: User) -> None:
        await user.save()
