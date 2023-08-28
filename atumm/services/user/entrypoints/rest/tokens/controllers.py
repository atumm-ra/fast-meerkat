from injector import inject

from atumm.services.user.domain.usecases.login import LoginCommand, LoginUseCase
from atumm.services.user.domain.usecases.refresh_token import (
    RefreshTokenCommand,
    RefreshTokenUseCase,
)
from atumm.services.user.entrypoints.rest.tokens.presenters import TokenPresenter
from atumm.services.user.entrypoints.rest.tokens.requests import (
    LoginRequest,
    RefreshTokenRequest,
)
from atumm.services.user.entrypoints.rest.tokens.responses import (
    AuthenticatedTokensResponse,
)


class TokensController:
    @inject
    def __init__(
        self,
        presenter: TokenPresenter,
        refresh_token_use_case: RefreshTokenUseCase,
        login_use_case: LoginUseCase,
    ):
        self.presenter = presenter
        self.refresh_token_use_case = refresh_token_use_case
        self.login_use_case = login_use_case

    async def refresh_token(
        self, request: RefreshTokenRequest
    ) -> AuthenticatedTokensResponse:
        tokens = await self.refresh_token_use_case.execute(
            RefreshTokenCommand(
                token=request.token, refresh_token=request.refresh_token
            )
        )
        return self.presenter.present(tokens)

    async def login(self, request: LoginRequest) -> AuthenticatedTokensResponse:
        tokens = await self.login_use_case.execute(
            LoginCommand(
                email=request.email,
                password=request.password,
                device_id=request.device_id,
            )
        )
        return self.presenter.present(tokens)
