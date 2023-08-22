from typing import List

from classy_fastapi import Routable, get, post
from fastapi import Depends, Query
from fastapi_jwt_auth import AuthJWT
from injector import inject

from atumm.core.entrypoints.rest.responses import RuntimeExceptionResponse
from atumm.core.presenter import AbstractPresenter
from atumm.services.user.dataproviders.beanie.models import User
from atumm.services.user.domain.usecases.get_user import (
    GetUserInfoQuery,
    GetUserInfoUseCase,
)
from atumm.services.user.domain.usecases.register import (
    RegisterCommand,
    RegisterUseCase,
)
from atumm.services.user.domain.usecases.user_list import (
    GetUserListQuery,
    GetUserListUseCase,
)
from atumm.services.user.entrypoints.rest.users.response import (
    CreateUserResponseSchema,
    GetUserListResponseSchema,
)
from thisapp.fastapi.dependencies import IsAdmin, PermissionDependency


class UserController:
    def __init__(
        self,
        register_use_case: RegisterUseCase,
        get_user_info_use_case: GetUserInfoUseCase,
        get_user_list_use_case: GetUserListUseCase,
    ):
        self.register_use_case = register_use_case
        self.get_user_info_use_case = get_user_info_use_case
        self.get_user_list_use_case = get_user_list_use_case

    async def register(self, command: RegisterCommand) -> User:
        user = await self.register_use_case.execute(command)
        return user

    async def get_user_info(self, auth: AuthJWT) -> User:
        user = await self.get_user_info_use_case.execute(
            GetUserInfoQuery(auth=auth.data["sub"])
        )
        return user

    async def get_user_list(self, start: int, limit: int) -> List[User]:
        users = await self.get_user_list_use_case.execute(
            GetUserListQuery(limit=limit, start=start)
        )
        return users


class UserCollectionPresenter(AbstractPresenter[User, CreateUserResponseSchema]):
    @staticmethod
    def present(user: User) -> CreateUserResponseSchema:
        return CreateUserResponseSchema(**user.dict())


class UserRouter(Routable):
    @inject
    def __init__(
        self,
        register: RegisterUseCase,
        get_user_info: GetUserInfoUseCase,
        get_user_list: GetUserListUseCase,
    ):
        super().__init__(prefix="/users")
        self.controller = UserController(
            register,
            get_user_info,
            get_user_list,
        )
        self.presenter = UserCollectionPresenter()

    @post(
        "/",
        response_model=CreateUserResponseSchema,
        status_code=201,
        responses={
            "400": {"model": RuntimeExceptionResponse},
            "401": {"model": RuntimeExceptionResponse},
        },
    )
    async def create_user(self, command: RegisterCommand):
        user = await self.controller.register(command)
        return self.presenter.present(user)

    @get(
        "/",
        response_model=List[GetUserListResponseSchema],
        response_model_exclude={"id"},
        responses={
            "400": {"model": RuntimeExceptionResponse},
            "401": {"model": RuntimeExceptionResponse},
        },
        dependencies=[Depends(PermissionDependency([IsAdmin]))],
    )
    async def get_user_list(
        self,
        start: int = Query(None, description="Slice from"),
        limit: int = Query(10, description="Limit"),
    ):
        users = await self.controller.get_user_list(start=start, limit=limit)
        return self.presenter.present_list(users)
