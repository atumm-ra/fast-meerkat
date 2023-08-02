from typing import List

import pymongo
from injector import inject
from motor.motor_asyncio import AsyncIOMotorClient

from atumm.app.core.data_providers.datastore.exceptions import DuplicateKeyException
from atumm.user.core.repositories import AbstractUserRepo
from atumm.user.dataproviders.beanie.models import User


class UserRepo(AbstractUserRepo):
    @inject
    def __init__(self, client: AsyncIOMotorClient) -> None:
        super().__init__()
        self.client = client

    async def create(self, username: str, password: str, email: str) -> User:
        user = User(email=email, password=password, username=username)
        user.encrypt_password()

        try:
            await User.insert_one(user)
        except pymongo.errors.DuplicateKeyError as e:
            raise DuplicateKeyException(e.details["keyValue"])
        return user

    async def find_by_email(self, email: str) -> User:
        document = await self.client.db.users.find_one({"email": {"$eq": email}})
        return await self.client.User.find_one(User.email == email)

    async def find_all(self, limit: int = 12) -> List[User]:
        user_list = await User.find().to_list(limit)
        return user_list

    async def save(self, user: User) -> None:
        await user.save()
