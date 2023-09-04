from buti import BootableComponent, ButiStore
from fastapi import FastAPI
from thisapp.buti.keys import ContainerKeys
from atumm.services.health.entrypoints.rest.health.routers import health_router


class HealthServiceComponent(BootableComponent):
    def boot(self, object_store: ButiStore):
        app: FastAPI = object_store.get(ContainerKeys.app)
        app.include_router(health_router)
        
