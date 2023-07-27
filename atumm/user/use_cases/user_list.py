from atumm.app.core.use_case import Query, QueryUseCase
from atumm.user.dataproviders.beanie.repositories import UserRepo


class GetUserListQuery(Query):
    limit: int
    prev: int


class GetUserListUseCase(QueryUseCase[GetUserListQuery]):
    def __init__(self, user_repo: UserRepo):
        self.user_repo = user_repo

    async def execute(self, query: GetUserListQuery):
        users = await self.user_repo.find_all(limit=query.limit)
        return users
