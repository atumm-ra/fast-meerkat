from beanie import init_beanie
from buti import BootableComponent, ButiStore
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient

from atumm.app.infra.buti.keys import ContainerKeys
from atumm.app.infra.config import Config
from atumm.app.infra.injector import injector
from atumm.user.dataproviders.beanie.models import User


class BeanieComponent(BootableComponent):
    def boot(self, object_store: ButiStore):
        # get the configuration manager and FastAPI from the store
        config: Config = object_store.get(ContainerKeys.config)
        app: FastAPI = object_store.get(ContainerKeys.app)
        beanie_client: AsyncIOMotorClient = injector.get(AsyncIOMotorClient)

        @app.on_event("startup")
        async def beanie_startup():
            await init_beanie(db=beanie_client.db, document_models=[User])

        @app.on_event("shutdown")
        async def beanie_shutdown():
            beanie_client.close()

        # Store the database connection in the ButiStore
        object_store.set(ContainerKeys.beanie, beanie_client)
