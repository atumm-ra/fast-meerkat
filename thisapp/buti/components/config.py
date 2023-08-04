from buti import BootableComponent, ButiStore

from thisapp.buti.keys import ContainerKeys
from thisapp.config import Config, get_config


class ConfigComponent(BootableComponent):
    def boot(self, store: ButiStore) -> None:
        config: Config = get_config()

        store.set(ContainerKeys.config, config)
