from unittest.mock import AsyncMock

import pytest
from faker import Faker

from atumm.user.use_cases.register import RegisterCommand, RegisterUseCase
from atumm.user.core.models import UserModel



class TestRegisterUseCase:
    faker = Faker()

    @pytest.mark.anyio
    async def test_register(self):
        email = self.faker.email()
        password = self.faker.password()
        username = self.faker.user_name()

        user = UserModel(email=email, password=password, username=username)
        user.encrypt_password()

        user_repo = AsyncMock()
        user_repo.find_by_email.return_value = None
        user_repo.create.return_value = user

        register_command = RegisterCommand(
            email=email, password1=password, password2=password, username=username
        )
        register_use_case = RegisterUseCase(user_repo)

        created_user = await register_use_case.execute(register_command)

        user_repo.create.assert_called_once_with(username, password, email)
        assert created_user.email == email
        assert created_user.username == username
        assert created_user.is_password_valid(password)
