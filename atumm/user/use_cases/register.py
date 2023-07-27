from pydantic import EmailStr, Field, validator

from atumm.app.core.use_case import Command, CommandUseCase
from atumm.user.core.exceptions import (
    DuplicateEmailOrUsernameException,
    PasswordsDoNotMatchException,
)
from atumm.user.core.repositories import AbstractUserRepo


class RegisterCommand(Command):
    email: EmailStr = Field(..., description="Email")
    password1: str = Field(..., description="Password1")
    password2: str = Field(..., description="Password2")
    username: str = Field(..., description="username")

    @validator("password2")
    def passwords_match(cls, v, values, **kwargs):
        if "password1" in values and v != values["password1"]:
            raise PasswordsDoNotMatchException
        return v


class RegisterUseCase(CommandUseCase[RegisterCommand]):
    def __init__(self, user_repo: AbstractUserRepo):
        self.user_repo = user_repo

    async def execute(self, command: RegisterCommand):
        # todo refactor: exceptions separation
        does_exist = await self.user_repo.find_by_email(command.email)
        print(does_exist, flush=True)
        if does_exist:
            raise DuplicateEmailOrUsernameException

        user = await self.user_repo.create(
            command.username, command.password1, command.email
        )
        return user
