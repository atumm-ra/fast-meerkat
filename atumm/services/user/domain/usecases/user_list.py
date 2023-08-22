from typing import List

from injector import inject

from atumm.core.use_case import Query, QueryUseCase
from atumm.services.user.domain.models import UserModel
from atumm.services.user.domain.repositories import AbstractUserRepo


class GetUserListQuery(Query):
    start: int
    limit: int


class GetUserListUseCase(QueryUseCase[GetUserListQuery]):
    @inject
    def __init__(self, user_repo: AbstractUserRepo):
        self.user_repo = user_repo

    async def execute(self, query: GetUserListQuery) -> List[UserModel]:
        users = await self.user_repo.find_all(start=query.start, limit=query.limit)
        return users
