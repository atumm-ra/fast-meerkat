from typing import List

from classy_fastapi import Routable, get, post
from fastapi import Depends, Query
from fastapi_jwt_auth import AuthJWT
from injector import inject

from atumm.app.core.presenter import AbstractCollectionPresenter
from atumm.app.infra.exceptions.base import RuntimeExceptionResponse
from atumm.app.infra.fastapi.dependencies import IsAdmin, PermissionDependency
from atumm.user.core.exceptions import PasswordsDoNotMatchException
from atumm.user.dataproviders.beanie.models import User
from atumm.user.dataproviders.beanie.repositories import UserRepo
from atumm.user.entrypoints.rest.users.response import (
    CreateUserResponseSchema,
    GetUserListResponseSchema,
)
from atumm.user.use_cases.get_user import GetUserInfoQuery, GetUserInfoUseCase
from atumm.user.use_cases.register import RegisterCommand, RegisterUseCase
from atumm.user.use_cases.user_list import GetUserListQuery, GetUserListUseCase


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

    async def register(self, command: RegisterCommand):
        # todo refactor: move this exception class
        user = await self.register_use_case.execute(command)
        return user

    async def get_user_info(self, auth: AuthJWT):
        user = await self.get_user_info_use_case.execute(GetUserInfoQuery(auth=auth))
        return user

    async def get_user_list(self, limit: int, prev: int):
        users = await self.get_user_list_use_case.execute(
            GetUserListQuery(limit=limit, prev=prev)
        )
        return users


class UserCollectionPresenter(
    AbstractCollectionPresenter[User, CreateUserResponseSchema]
):
    @staticmethod
    def present(user: User) -> CreateUserResponseSchema:
        return CreateUserResponseSchema(**user.dict())

    @staticmethod
    def present_list(users: List[User]) -> List[CreateUserResponseSchema]:
        return [GetUserListResponseSchema(**user.dict()) for user in users]


class UserRouter(Routable):
    @inject
    def __init__(self, register: RegisterUseCase, get_user_info: GetUserInfoUseCase, get_user_list: GetUserListUseCase):
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
        limit: int = Query(10, description="Limit"),
        prev: int = Query(None, description="Prev ID"),
    ):
        users = await self.controller.get_user_list(limit=limit, prev=prev)
        return self.presenter.present_list(users)
