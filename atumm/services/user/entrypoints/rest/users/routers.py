from typing import List

from classy_fastapi import Routable, get, post
from fastapi import Depends, Query
from injector import inject

from atumm.core.entrypoints.rest.responses import RuntimeExceptionResponse
from atumm.services.user.domain.usecases.register import RegisterCommand
from atumm.services.user.entrypoints.rest.users.controllers import UserController
from atumm.services.user.entrypoints.rest.users.presenters import UserPresenter
from atumm.services.user.entrypoints.rest.users.responses import (
    GetUsersResponse,
    RegisterResponse,
)
from thisapp.fastapi.dependencies.permission import IsAdmin, PermissionDependency


class UserRouter(Routable):
    @inject
    def __init__(
        self,
        controller: UserController,
        presenter: UserPresenter,
    ):
        super().__init__(prefix="/users")
        self.controller = controller
        self.presenter = presenter

    @post(
        "/",
        response_model=RegisterResponse,
        status_code=201,
        responses={
            "400": {"model": RuntimeExceptionResponse},
            "401": {"model": RuntimeExceptionResponse},
        },
    )
    async def create_user(self, command: RegisterCommand):
        user = await self.controller.register_action(command)
        return self.presenter.present(user)

    @get(
        "/",
        response_model=List[GetUsersResponse],
        response_model_exclude={"id"},
        responses={
            "400": {"model": RuntimeExceptionResponse},
            "401": {"model": RuntimeExceptionResponse},
        },
        dependencies=[Depends(PermissionDependency([IsAdmin]))],
    )
    async def get_user_list(
        self,
        start_from: int = Query(0, description="Slice from"),
        num_items: int = Query(10, description="Number of items to return"),
    ):
        users = await self.controller.get_user_list_action(start=start_from, limit=num_items)
        return self.presenter.present_list(users)
