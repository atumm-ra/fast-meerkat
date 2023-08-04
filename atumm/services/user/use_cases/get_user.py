from injector import inject
from pydantic import EmailStr
from atumm.core.use_case import Query, QueryUseCase
from atumm.services.user.core.repositories import AbstractUserRepo
from atumm.services.user.dataproviders.beanie.models import User


class GetUserInfoQuery(Query):
    email: EmailStr


class GetUserInfoUseCase(QueryUseCase[GetUserInfoQuery]):
    @inject
    def __init__(self, user_repo: AbstractUserRepo):
        self.user_repo = user_repo

    async def execute(self, command: GetUserInfoQuery) -> User:
        user = await self.user_repo.find_by_email(command.email)
        return user
