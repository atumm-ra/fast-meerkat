from buti import BootableComponent, ButiStore

from thisapp.injector import injector
from thisapp.buti.keys import ContainerKeys


class InjectorComponent(BootableComponent):
    def boot(self, store: ButiStore) -> None:
        store.set(ContainerKeys.injector, injector)
