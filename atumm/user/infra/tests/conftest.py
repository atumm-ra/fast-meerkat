from typing import AsyncIterator

import httpx
import pytest
from asgi_lifespan import LifespanManager
from hypothesis import settings

from atumm.app.infra.app.server import app


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.fixture
async def client() -> AsyncIterator[httpx.AsyncClient]:
    async with httpx.AsyncClient(
        app=app, base_url="http://testhost"
    ) as client, LifespanManager(app):
        yield client


settings(max_examples=1)
