from typing import List

from atumm.app.core.data_providers.datastore import beanie
from atumm.app.core.data_providers.datastore.exceptions import (
    DataProviderException,
    DuplicateKeyException,
)
from atumm.user.core.models import UserModel
from atumm.user.core.repositories import AbstractUserRepo
from atumm.user.dataproviders.beanie.models import User


class UserRepo(AbstractUserRepo):
    async def create(self, username: str, password: str, email: str) -> User:
        user = User(email=email, password=password, username=username)
        user.encrypt_password()
        try:
            await User.insert_one(user)
        except beanie.exceptions.DuplicateKeyException as e:
            raise DuplicateKeyException(e.key)
        except beanie.exceptions.BeanieException as e:
            raise DataProviderException(str(e))
        return user

    async def find_by_email(self, email: str) -> User:
        return await User.find_one(User.email == email)

    async def find_all(self, limit: int = 12) -> List[User]:
        user_list = await User.find().to_list(limit)
        return user_list

    async def save(self, user: User) -> None:
        await user.save()
