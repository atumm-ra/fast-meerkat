from unittest.mock import AsyncMock
from faker import Faker
import mock
import pytest
from atumm.app.infra.injector import injector
from atumm.user.core.models import UserModel
from atumm.user.dataproviders.beanie.repositories import UserRepo
from atumm.user.infra.auth.tokenizer import Tokenizer
from atumm.user.use_cases.login import LoginCommand, LoginUseCase



class TestTokensRouter:
    faker = Faker()

    @pytest.mark.anyio
    async def test_login(self):
        email = self.faker.email()
        password = self.faker.password()
        device_id = self.faker.uuid4()
        user = UserModel(email=email, password=password, device_id=device_id)
        user.encrypt_password()
        
        user_repo = AsyncMock()
        user_repo.find_by_email.return_value = user
        
        login_command = LoginCommand(email=email, password=password, device_id=device_id)
        login_use_case = LoginUseCase(user_repo, Tokenizer(self.faker.word(), 'HS256'))
        
        tokens = await login_use_case.execute(login_command)
        assert 'token' in tokens.keys()
        assert 'refresh_token' in tokens.keys()
