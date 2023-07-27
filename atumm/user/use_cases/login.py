from typing import Optional

from atumm.app.core.use_case import Command, CommandUseCase
from atumm.user.core.exceptions import (
    AccountLockedException,
    PasswordsDoNotMatchException,
    UserNotFoundException,
)
from atumm.user.dataproviders.beanie.repositories import UserRepo
from atumm.user.infra.auth.tokenizer import Tokenizer


class LoginCommand(Command):
    email: str
    password: str
    device_id: Optional[str] = None


class LoginUseCase(CommandUseCase[LoginCommand]):
    def __init__(self, user_repo: UserRepo, tokenizer: Tokenizer):
        self.repo = user_repo
        self.tokenizer = tokenizer

    async def execute(self, command: LoginCommand):
        user = await self.repo.find_by_email(email=command.email)
        if not user:
            raise UserNotFoundException()

        if user.is_locked():
            raise AccountLockedException()

        if not user.is_password_valid(command.password):
            raise PasswordsDoNotMatchException

        if user.device_id is None:
            user.device_id = command.device_id
            await self.repo.save(user)

        token = self.tokenizer.encode(
            payload={"sub": str(user.email), "user_id": str(user.id), "type": "access"}
        )
        refresh_token = self.tokenizer.encode(
            payload={"sub": "refresh", "type": "refresh"}
        )
        return {"token": token, "refresh_token": refresh_token}
