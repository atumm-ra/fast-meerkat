from atumm.core.presenters import AbstractPresenter
from atumm.services.user.entrypoints.rest.tokens.responses import (
    AuthenticatedTokensResponse,
)


class TokenPresenter(AbstractPresenter[dict, AuthenticatedTokensResponse]):
    def present(self, tokens: dict) -> AuthenticatedTokensResponse:
        return AuthenticatedTokensResponse(
            token=tokens["token"], refresh_token=tokens["refresh_token"]
        )
