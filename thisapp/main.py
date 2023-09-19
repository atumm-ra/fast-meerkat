import uvicorn
from atumm.core.infra.config import Config, configure
from atumm.extensions.buti.components.config import ConfigComponent
from atumm.extensions.buti.keys import AtummContainerKeys
from atumm.extensions.fastapi.components import AuthJWTComponent, FastAPIComponent
from atumm.services.health.infra.buti import HealthServiceComponent
from atumm.services.user import UserConfig
from atumm.services.user.infra.buti import UserServiceComponent
from buti import Bootloader, ButiStore

from thisapp.config import AppConfig
from thisapp.init.buti.injector import InjectorComponent

app_components = [
    ConfigComponent(),
    InjectorComponent(),
    FastAPIComponent(),
    AuthJWTComponent(),
    UserServiceComponent(),
    HealthServiceComponent(),
]

config = configure.build(".env")
bootloader = Bootloader(app_components)
store: ButiStore = bootloader.boot()

app = store.get(AtummContainerKeys.app)

if __name__ == "__main__":
    uvicorn.run(app=app, port=5000, log_level="info")
