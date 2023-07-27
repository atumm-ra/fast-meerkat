from typing import List

from fastapi import FastAPI, Request
from injector import inject
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware

from atumm.app.infra.config import Config, get_config
from atumm.app.infra.fastapi.middlewares import (
    AuthBackend,
    AuthenticationMiddleware,
    ResponseLogMiddleware,
)


class BaseWebApp:
    @inject
    def __init__(self, config: Config):
        self.config = config
        self.app = FastAPI(
            title="Savvee",
            description="Savvee API",
            version="1.0.0",
            docs_url=None if self.config.STAGE == "production" else "/docs",
            redoc_url=None if self.config.STAGE == "production" else "/redoc",
            # middleware=self.make_middleware(),
        )

    def make_middleware(self) -> List[Middleware]:
        middleware = [
            Middleware(
                CORSMiddleware,
                allow_origins=["*"],
                allow_credentials=True,
                allow_methods=["*"],
                allow_headers=["*"],
            ),
            Middleware(AuthenticationMiddleware, backend=AuthBackend()),
            Middleware(ResponseLogMiddleware),
        ]
        return middleware


class TestWebApp(BaseWebApp):
    pass


class ProductionWebApp(BaseWebApp):
    pass


config = get_config()
