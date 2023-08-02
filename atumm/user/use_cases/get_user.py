from fastapi_jwt_auth import AuthJWT
from injector import inject

from atumm.app.core.use_case import Query, QueryUseCase
from atumm.user.dataproviders.beanie.models import User
from atumm.user.dataproviders.beanie.repositories import UserRepo


class GetUserInfoQuery(Query):
    class Config:
        arbitrary_types_allowed = True

    auth: AuthJWT


class GetUserInfoUseCase(QueryUseCase[GetUserInfoQuery]):
    @inject
    def __init__(self, user_repo: UserRepo):
        self.user_repo = user_repo

    async def execute(self, command: GetUserInfoQuery) -> User:
        data = command.auth.get_raw_jwt()
        user = await self.user_repo.find_by_email(data["sub"])
        return user
