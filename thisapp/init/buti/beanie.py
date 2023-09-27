from atumm.extensions.beanie import init_my_beanie
from atumm.extensions.buti.keys import AtummContainerKeys
from atumm.extensions.config import Config
from atumm.services.user.dataproviders.beanie.models import User
from buti import BootableComponent, ButiStore
from fastapi import FastAPI
from injector import Injector
from motor.motor_asyncio import AsyncIOMotorClient


class BeanieComponent(BootableComponent):
    def boot(self, object_store: ButiStore):
        # get the configuration manager and FastAPI from the store
        config: Config = object_store.get(AtummContainerKeys.config)
        app: FastAPI = object_store.get(AtummContainerKeys.app)
        injector_obj: Injector = object_store.get(AtummContainerKeys.injector)
        beanie_client: AsyncIOMotorClient = injector_obj.get(AsyncIOMotorClient)

        @app.on_event("startup")
        async def beanie_startup():
            await init_my_beanie(beanie_client, config.MONGO_DB, [User])

        @app.on_event("shutdown")
        async def beanie_shutdown():
            beanie_client.close()

        # Store the database connection in the ButiStore
        object_store.set(AtummContainerKeys.beanie, beanie_client)
