from buti import BootableComponent, ButiStore
from injector import Injector

from atumm.app.infra.buti.keys import ContainerKeys
from atumm.user.infra.di.providers import providers_list as user_providers


class InjectorComponent(BootableComponent):
    def boot(self, store: ButiStore) -> None:
        all_providers = user_providers + []

        injector = Injector(modules=all_providers)
        store.set(ContainerKeys.injector, injector)
