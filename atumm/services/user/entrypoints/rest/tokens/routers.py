from classy_fastapi import Routable, post
from injector import inject

from atumm.core.entrypoints.rest.responses import RuntimeExceptionResponse
from atumm.services.user.entrypoints.rest.tokens.controllers import TokensController
from atumm.services.user.entrypoints.rest.tokens.requests import (
    LoginRequest,
    RefreshTokenRequest,
)
from atumm.services.user.entrypoints.rest.tokens.responses import (
    AuthenticatedTokensResponse,
)


class TokensRouter(Routable):
    @inject
    def __init__(self, controller: TokensController):
        super().__init__(prefix="/tokens")
        self.controller = controller

    @post(
        "/refresh",
        responses={
            "200": {"model": AuthenticatedTokensResponse},
            "400": {"model": RuntimeExceptionResponse},
            "401": {"model": RuntimeExceptionResponse},
        },
    )
    async def refresh_token(
        self, request: RefreshTokenRequest
    ) -> AuthenticatedTokensResponse:
        return await self.controller.refresh_token(request)

    @post(
        "/access",
        responses={
            "200": {"model": AuthenticatedTokensResponse},
            "401": {"model": RuntimeExceptionResponse},
            "404": {"model": RuntimeExceptionResponse},
        },
    )
    async def login(self, request: LoginRequest) -> AuthenticatedTokensResponse:
        return await self.controller.login(request)
