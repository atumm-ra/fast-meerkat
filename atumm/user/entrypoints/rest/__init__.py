from fastapi import APIRouter

from atumm.app.infra.injector import injector
from atumm.user.entrypoints.rest.tokens.tokens import TokensRouter
from atumm.user.entrypoints.rest.users.users import UserRouter

auth_router = injector.get(TokensRouter)
user_router = injector.get(UserRouter)

user_api_router = APIRouter()
user_api_router.include_router(user_router.router, prefix="/api/v1", tags=["Users"])
user_api_router.include_router(
    auth_router.router, prefix="/api/v1", tags=["AuthTokens"]
)


__all__ = ["user_api_router"]
