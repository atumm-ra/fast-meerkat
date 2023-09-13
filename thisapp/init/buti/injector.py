from atumm.extensions.buti.keys import AtummContainerKeys
from buti import BootableComponent, ButiStore

from thisapp.init.injector import injector


class InjectorComponent(BootableComponent):
    def boot(self, store: ButiStore) -> None:
        store.set(AtummContainerKeys.injector, injector)
