from unittest import TestCase
from unittest.mock import AsyncMock

import pytest
from hypothesis import HealthCheck, given, settings
from hypothesis.strategies import emails, uuids, text
from injector import Module, singleton
from starlette.testclient import TestClient

from atumm.app.infra.hypothesis.types import passwords
from atumm.app.infra.injector import injector
from atumm.user.entrypoints.common.schemas.jwt import RefreshTokenSchema
from atumm.user.entrypoints.common.services import UserService
from atumm.user.entrypoints.common.services.token import TokenService
from atumm.user.entrypoints.rest.tokens.request.auth import RefreshTokenRequest
from atumm.user.entrypoints.rest.users.request.user import LoginRequest
from atumm.user.infra.auth.tokenizer import Tokenizer


class TestAppModule(Module):
    def configure(self, binder):
        binder.bind(TokenService, to=AsyncMock(), scope=singleton)
        binder.bind(UserService, to=AsyncMock(), scope=singleton)


class TestTokensRouter(TestCase):
    @given(user_id=uuids(), email=emails())
    @settings(
        max_examples=1, suppress_health_check=[HealthCheck.function_scoped_fixture]
    )
    @pytest.mark.anyio
    async def test_refresh_token(self, client: TestClient, user_id: str, email: str):
        tokenizer = injector.get(Tokenizer)
        request = RefreshTokenRequest(
            token=tokenizer.encode(payload={"user_id": str(user_id), "sub": email}),
            refresh_token=tokenizer.encode(payload={"sub": "refresh"}),
        )

        refresh_token = RefreshTokenSchema(
            token=tokenizer.encode(payload={"user_id": str(user_id), "sub": email}),
            refresh_token=tokenizer.encode(payload={"sub": "refresh"}),
        )

        response = await client.post("/api/v1/tokens/refresh", json=request.dict())

        assert response.status_code == 200
        assert response.json() == refresh_token.dict()

    @given(email=emails(), password=passwords(), device_id=text())
    @settings(
        max_examples=1, suppress_health_check=[HealthCheck.function_scoped_fixture]
    )
    @pytest.mark.anyio
    async def test_login(self, client: TestClient, email: str, password: str, device_id: str):
        request = LoginRequest(email=email, password=password, device_id=device_id)

        response = await client.post("/api/v1/tokens/access", json=request.dict())

        assert response.status_code == 200
