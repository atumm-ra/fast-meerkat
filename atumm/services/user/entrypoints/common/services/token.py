from injector import inject

from atumm.services.user.domain.exceptions import InvalidRefreshSubject
from atumm.services.user.entrypoints.common.schemas.jwt import RefreshTokenSchema
from atumm.services.user.infra.auth.tokenizer import Tokenizer


class TokenService:
    @inject
    def __init__(self, tokenizer: Tokenizer):
        self.tokenizer = tokenizer

    async def verify_token(self, token: str) -> None:
        self.tokenizer.decode(token=token)

    async def create_refresh_token(
        self,
        token: str,
        refresh_token: str,
    ) -> RefreshTokenSchema:
        token = self.tokenizer.decode(token=token)
        refresh_token = self.tokenizer.decode(token=refresh_token)
        if refresh_token.get("sub") != "refresh":
            raise InvalidRefreshSubject

        return RefreshTokenSchema(
            token=self.tokenizer.encode(
                payload={"user_id": token.get("user_id"), "sub": token.get("sub")}
            ),
            refresh_token=self.tokenizer.encode(payload={"sub": "refresh"}),
        )
