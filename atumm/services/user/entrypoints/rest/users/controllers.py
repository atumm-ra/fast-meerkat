from typing import List

from fastapi_jwt_auth import AuthJWT
from injector import inject

from atumm.services.user.dataproviders.beanie.models import User
from atumm.services.user.domain.usecases.get_user import (
    GetUserInfoQuery,
    GetUserInfoUseCase,
)
from atumm.services.user.domain.usecases.get_users import GetUsersQuery, GetUsersUsecase
from atumm.services.user.domain.usecases.register import (
    RegisterCommand,
    RegisterUseCase,
)


class UserController:
    @inject
    def __init__(
        self,
        register_usecase: RegisterUseCase,
        get_user_info_usecase: GetUserInfoUseCase,
        get_users_usecase: GetUsersUsecase,
    ):
        self.register_usecase = register_usecase
        self.get_user_info_usecase = get_user_info_usecase
        self.get_users_usecase = get_users_usecase

    async def register_action(self, command: RegisterCommand) -> User:
        return await self.register_usecase.execute(command)

    async def get_user_info_action(self, auth: AuthJWT) -> User:
        return await self.get_user_info_usecase.execute(GetUserInfoQuery(auth=auth.data["sub"]))

    async def get_user_action(self, start: int, limit: int) -> List[User]:
        return await self.get_users_usecase.execute(GetUsersQuery(limit=limit, start=start))
