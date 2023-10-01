import uvicorn
from atumm.extensions.buti.components.config import ConfigComponent
from atumm.extensions.buti.keys import AtummContainerKeys
from atumm.extensions.fastapi.components import FastAPIComponent
from atumm.services.health.infra.buti import HealthServiceComponent
from atumm.services.user.infra.buti import UserServiceComponent
from buti import Bootloader, ButiStore

from thisapp.init.buti.beanie import BeanieComponent
from thisapp.init.buti.injector import InjectorComponent


def boot_app():
    
    app_components = [
        ConfigComponent(),
        InjectorComponent(),
        FastAPIComponent(),
        BeanieComponent(),
        UserServiceComponent(),
        HealthServiceComponent(),
    ]
    
    bootloader = Bootloader(app_components)
    return bootloader.boot()


store: ButiStore = boot_app()

app = store.get(AtummContainerKeys.app)

# used only for debugging
if __name__ == "__main__":
    uvicorn.run(app=app, port=5000, log_level="info")
