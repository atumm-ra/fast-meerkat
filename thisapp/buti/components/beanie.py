from beanie import init_beanie
from buti import BootableComponent, ButiStore
from fastapi import FastAPI
from injector import Injector
from motor.motor_asyncio import AsyncIOMotorClient
from thisapp.beanie import init_my_beanie

from thisapp.buti.keys import ContainerKeys
from thisapp.config import Config


class BeanieComponent(BootableComponent):
    def boot(self, object_store: ButiStore):
        # get the configuration manager and FastAPI from the store
        config: Config = object_store.get(ContainerKeys.config)
        app: FastAPI = object_store.get(ContainerKeys.app)
        injector_obj: Injector = object_store.get(ContainerKeys.injector)
        beanie_client: AsyncIOMotorClient = injector_obj.get(AsyncIOMotorClient)

        @app.on_event("startup")
        async def beanie_startup():
            await init_my_beanie(beanie_client, config.MONGO_DB)

        @app.on_event("shutdown")
        async def beanie_shutdown():
            beanie_client.close()

        # Store the database connection in the ButiStore
        object_store.set(ContainerKeys.beanie, beanie_client)
