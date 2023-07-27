from buti import BootableComponent, ButiStore

from atumm.app.infra.buti.keys import ContainerKeys
from atumm.app.infra.config import Config, get_config


class ConfigComponent(BootableComponent):
    def boot(self, store: ButiStore) -> None:
        config: Config = get_config()

        store.set(ContainerKeys.config, config)
