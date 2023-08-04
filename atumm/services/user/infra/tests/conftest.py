from typing import AsyncIterator

import httpx
import pytest

from thisapp.main import app


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.fixture
async def client() -> AsyncIterator[httpx.AsyncClient]:
    async with httpx.AsyncClient(app=app, base_url="http://testhost") as client:
        yield client
