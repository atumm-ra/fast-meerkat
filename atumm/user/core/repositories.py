from abc import abstractmethod
from typing import List

from atumm.app.core.data_providers.datastore.beanie import BeanieDataProvider
from atumm.user.dataproviders.beanie.models import User


class AbstractUserRepo(BeanieDataProvider[User]):
    @abstractmethod
    async def create(self, username: str, password: str, email: str) -> User:
        pass

    @abstractmethod
    async def find_by_email(self, email: str) -> User:
        pass

    @abstractmethod
    async def find_all(self, limit: int = 12) -> List[User]:
        pass

    @abstractmethod
    async def save(self, user: User) -> None:
        pass
