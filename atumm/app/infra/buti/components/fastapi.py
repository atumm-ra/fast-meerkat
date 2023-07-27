from traceback import print_tb

from buti import BootableComponent, ButiStore
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from injector import inject
from pydantic import BaseModel
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

from atumm.app.core.exceptions import ErrorStatus, ExceptionDetail, RuntimeException
from atumm.app.infra.beanie import init_my_beanie
from atumm.app.infra.buti.keys import ContainerKeys
from atumm.app.infra.config import Config
from atumm.app.infra.exceptions.base import map_exception_to_response
from atumm.app.infra.fastapi.middlewares import (
    AuthBackend,
    AuthenticationMiddleware,
    ResponseLogMiddleware,
)
from atumm.user.entrypoints.rest import user_api_router
from atumm.health.entrypoints.rest.health.routers import health_router

class FastAPIComponent(BootableComponent):
    def boot(self, store: ButiStore) -> None:
        from atumm.app.infra.app.base import ProductionWebApp

        config: Config = store.get(ContainerKeys.config)
        app: FastAPI = ProductionWebApp(config).app
        store.set(ContainerKeys.app, app)


class FastAPIMiddlewaresComponent(BootableComponent):
    def boot(self, store: ButiStore) -> None:
        app: FastAPI = store.get(ContainerKeys.app)
        app.user_middleware = self.make_middlewares()

    def make_middlewares(self):
        return [
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


class RouterComponent(BootableComponent):
    def boot(self, store: ButiStore) -> None:
        app: FastAPI = store.get(ContainerKeys.app)

        app.include_router(user_api_router)
        app.include_router(health_router)


class ListenersComponent(BootableComponent):
    def boot(self, store: ButiStore) -> None:
        app: FastAPI = store.get(ContainerKeys.app)

        self.register_exception_listeners(app)

        @app.on_event("startup")
        async def app_init():
            app.db = await init_my_beanie()

    def register_exception_listeners(self, app):
        # @app.exception_handler(StarletteHTTPException)
        # async def exception_callback(request: Request, exc: Exception):
        #     print(print_tb(exc.__traceback__))
        #     return JSONResponse({"detail": "test_error"}, status_code=500)

        @app.exception_handler(RuntimeException)
        async def handle_runtime_exception(
            request: Request, exception: RuntimeException
        ):
            code, response = map_exception_to_response(exception)
            return JSONResponse(content=response.dict(), status_code=code)

        @app.exception_handler(AuthJWTException)
        async def on_auth_error(request: Request, exc: AuthJWTException):
            status_code, message = 401, exc.message
            status_code, response = map_exception_to_response(
                RuntimeException(
                    code=status_code,
                    message=message,
                    status=ErrorStatus.TOKEN_ERROR,
                    details=[
                        ExceptionDetail(type=exc.__class__.__name__, reason=message)
                    ],
                )
            )
            return JSONResponse(response.dict(), status_code=401)

        @app.exception_handler(RequestValidationError)
        async def validation_exception_handler(
            request: Request, exc: RequestValidationError
        ):
            details = []
            for error in exc.errors():
                details.append(
                    ExceptionDetail(
                        type=error["type"],
                        reason=error["msg"],
                        metadata={"location": ".".join(map(str, error["loc"]))},
                    )
                )
            api_exception = RuntimeException(
                code=400,
                message="Validation error",
                status=ErrorStatus.VALIDATION_ERROR,
                details=details,
            )
            code, response = map_exception_to_response(api_exception)
            return JSONResponse(response.dict(), status_code=code)


class AuthJWTComponent(BootableComponent):
    def boot(self, store: ButiStore) -> None:
        config: Config = store.get(ContainerKeys.config)

        class Settings(BaseModel):
            authjwt_secret_key: str = config.JWT_SECRET_KEY
            authjwt_algorithm: str = config.JWT_ALGORITHM

        # callback to get your configuration
        @AuthJWT.load_config
        def get_jwt_config():
            return Settings()
