from buti import BootableComponent, ButiStore
from injector import Injector

from thisapp import injector
from thisapp.buti.keys import ContainerKeys
from thisapp.di.providers import app_providers
from atumm.services.user.infra.di.providers import user_providers as user_providers


class InjectorComponent(BootableComponent):
    def boot(self, store: ButiStore) -> None:
        store.set(ContainerKeys.injector, injector)
