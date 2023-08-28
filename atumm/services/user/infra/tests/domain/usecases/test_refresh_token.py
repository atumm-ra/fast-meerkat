import pytest
from faker import Faker
from mock import Mock

from atumm.services.user.domain.exceptions import InvalidRefreshSubject
from atumm.services.user.domain.usecases.refresh_token import (
    RefreshTokenCommand,
    RefreshTokenUseCase,
)
from atumm.services.user.infra.auth.tokenizer import Tokenizer


class TestRefreshTokenUseCase:
    faker = Faker()

    @pytest.mark.anyio
    async def test_refresh_token_valid(self):
        token = self.faker.sha256()
        refresh_token = self.faker.sha256()

        tokenizer = Tokenizer(self.faker.word(), "HS256")
        tokenizer.decode = Mock(
            return_value={"sub": "refresh"}
        )  # Mocking a valid refresh token subject

        refresh_token_command = RefreshTokenCommand(
            token=token, refresh_token=refresh_token
        )
        refresh_token_use_case = RefreshTokenUseCase(tokenizer)

        result = await refresh_token_use_case.execute(refresh_token_command)
        assert "token" in result.keys()
        assert "refresh_token" in result.keys()

    @pytest.mark.anyio
    async def test_refresh_token_invalid_subject(self):
        # Mocking a valid token and refresh token
        token = self.faker.sha256()
        refresh_token = self.faker.sha256()

        tokenizer = Tokenizer(self.faker.word(), "HS256")
        tokenizer.decode = Mock(
            return_value={"sub": "invalid"}
        )  # Mocking an invalid refresh token subject

        refresh_token_command = RefreshTokenCommand(
            token=token, refresh_token=refresh_token
        )
        refresh_token_use_case = RefreshTokenUseCase(tokenizer)

        with pytest.raises(InvalidRefreshSubject):
            await refresh_token_use_case.execute(refresh_token_command)
