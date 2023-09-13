import os

from atumm.core.infra.config import Config, configure
from atumm.extensions.buti.keys import AtummContainerKeys
from atumm.services.user import UserConfig  # to make sure UserConfig is registered
from buti.core import BootableComponent, ButiStore
from injector import Module, provider, singleton


@configure
class AppConfig(Config):
    STAGE: str = "dev"
    DEBUG: bool
    APP_HOST: str
    APP_PORT: int

    # OpenAPI configs
    API_TITLE: str
    API_DESCRIPTION: str = ""
    API_VERSION: str = "1.0.0"

    MONGO_DB: str
    MONGO_URL: str


env_file = ".env" if os.environ.get("STAGE") != "test" else ".env.test"
config = configure.build(env_file=env_file)


class ConfigProvider(Module):
    @singleton
    @provider
    def provide(self) -> Config:
        return config


class ConfigComponent(BootableComponent):
    def boot(self, object_store: ButiStore):
        object_store.set(AtummContainerKeys.config, config)
