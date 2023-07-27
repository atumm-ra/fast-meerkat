from typing import AsyncIterator
from hypothesis import settings

import httpx
import pytest

from atumm.app.infra.app.test import app


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.fixture
async def client() -> AsyncIterator[httpx.AsyncClient]:
    async with httpx.AsyncClient(app=app, base_url="http://testhost") as client:
        yield client

settings(max_examples=1)