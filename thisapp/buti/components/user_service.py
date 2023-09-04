from buti import BootableComponent, ButiStore
from fastapi import APIRouter, FastAPI
from injector import Injector
from atumm.services.user.entrypoints.rest.tokens.routers import TokensRouter
from atumm.services.user.entrypoints.rest.users.routers import UserRouter
from thisapp.buti.keys import ContainerKeys

from thisapp.config import Config


class UserServiceComponent(BootableComponent):
    def boot(self, object_store: ButiStore):
        app: FastAPI = object_store.get(ContainerKeys.app)
        injector_obj: Injector = object_store.get(ContainerKeys.injector)
        
        auth_router = injector_obj.get(TokensRouter)
        user_router = injector_obj.get(UserRouter)

        user_api_router = APIRouter()
        user_api_router.include_router(user_router.router, prefix="/api/v1", tags=["Users"])
        user_api_router.include_router(
            auth_router.router, prefix="/api/v1", tags=["AuthTokens"]
        )
        app.include_router(user_api_router)