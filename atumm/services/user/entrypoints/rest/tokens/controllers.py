from classy_fastapi import Routable, post
from injector import inject

from atumm.core.entrypoints.rest.responses import RuntimeExceptionResponse
from atumm.services.user.domain.usecases.login import LoginCommand, LoginUseCase
from atumm.services.user.entrypoints.common.services.token import TokenService
from atumm.services.user.entrypoints.rest.tokens.presenters import TokenPresenter
from atumm.services.user.entrypoints.rest.tokens.requests import (
    LoginRequest,
    RefreshTokenRequest,
    VerifyTokenRequest,
)
from atumm.services.user.entrypoints.rest.tokens.responses import (
    AuthenticatedTokensResponse,
)


class TokensRouter(Routable):
    @inject
    def __init__(
        self,
        presenter: TokenPresenter,
        jwt_service: TokenService,
        login_use_case: LoginUseCase,
    ):
        super().__init__(prefix="/tokens")
        self.presenter = presenter
        self.jwt_service = jwt_service
        self.login_use_case = login_use_case

    @post(
        "/refresh",
        response_model=AuthenticatedTokensResponse,
        responses={
            "400": {"model": RuntimeExceptionResponse},
            "401": {"model": RuntimeExceptionResponse},
        },
    )
    async def refresh_token(self, request: RefreshTokenRequest):
        token = await self.jwt_service.create_refresh_token(
            token=request.token, refresh_token=request.refresh_token
        )
        return AuthenticatedTokensResponse(
            **{"token": token.token, "refresh_token": token.refresh_token}
        )

    @post(
        "/verify",
        status_code=200,
        responses={"401": {"model": RuntimeExceptionResponse}},
    )
    async def verify_token(self, request: VerifyTokenRequest):
        # todo revisit
        await self.jwt_service.verify_token(token=request.token)
        return {}

    @post(
        "/access",
        response_model=AuthenticatedTokensResponse,
        responses={
            "404": {"model": RuntimeExceptionResponse},
            "401": {"model": RuntimeExceptionResponse},
        },
    )
    async def login(self, request: LoginRequest):
        tokens = await self.login_use_case.execute(
            LoginCommand(
                email=request.email,
                password=request.password,
                device_id=request.device_id,
            )
        )
        return self.presenter.present(tokens)
