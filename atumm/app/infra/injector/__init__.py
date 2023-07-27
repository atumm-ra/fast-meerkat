from injector import Injector

from atumm.user.infra.di.providers import ServicesInjectorModule, TokenizerProvider

injector = Injector(
    [
        ServicesInjectorModule(),
        TokenizerProvider(),
    ]
)
