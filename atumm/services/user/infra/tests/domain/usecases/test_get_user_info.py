from unittest.mock import AsyncMock, MagicMock

import pytest
from faker import Faker

from atumm.services.user.domain.models import UserModel
from atumm.services.user.domain.usecases.get_user import (
    GetUserInfoQuery,
    GetUserInfoUseCase,
)


class TestGetUserInfoUseCase:
    faker = Faker()

    @pytest.mark.anyio
    async def test_get_user_info(self):
        email = self.faker.email()
        password = self.faker.password()
        user = UserModel(email=email, password=password)
        user.encrypt_password()

        user_repo = AsyncMock()
        user_repo.find_by_email.return_value = user

        get_user_info_query = GetUserInfoQuery(email=email)
        get_user_info_use_case = GetUserInfoUseCase(user_repo)

        returned_user = await get_user_info_use_case.execute(get_user_info_query)

        user_repo.find_by_email.assert_called_once_with(email)
        assert returned_user.email == email
        assert returned_user.is_password_valid(password)
