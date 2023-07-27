from typing import AsyncIterator
from hypothesis import settings
from atumm.app.infra.app.server import app
import httpx
import pytest


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.fixture
async def client() -> AsyncIterator[httpx.AsyncClient]:
    async with httpx.AsyncClient(app=app, base_url="http://testhost") as client:
        yield client

settings(max_examples=1)