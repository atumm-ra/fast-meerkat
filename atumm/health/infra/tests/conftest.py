import asyncio
from typing import AsyncIterator
from beanie import init_beanie
from mock import Mock
from mongomock_motor import AsyncMongoMockClient
import httpx
import pytest
from hypothesis import settings
from atumm.app.infra.injector import injector

from atumm.app.infra.app.server import app
from atumm.user.dataproviders.beanie.models import User


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.fixture
async def client() -> AsyncIterator[httpx.AsyncClient]:
    async with httpx.AsyncClient(
        app=app, base_url="http://testhost"
    ) as client:
        yield client


