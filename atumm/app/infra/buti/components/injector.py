from buti import BootableComponent, ButiStore
from injector import Injector
from atumm.app.infra import injector

from atumm.app.infra.buti.keys import ContainerKeys
from atumm.app.infra.di.providers import app_providers
from atumm.user.infra.di.providers import user_providers as user_providers

class InjectorComponent(BootableComponent):
    def boot(self, store: ButiStore) -> None:
        store.set(ContainerKeys.injector, injector)
