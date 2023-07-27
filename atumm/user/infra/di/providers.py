from injector import Module, singleton

from atumm.app.infra.config import get_config
from atumm.user.entrypoints.common.services.token import TokenService
from atumm.user.infra.auth.tokenizer import Tokenizer


class ServicesInjectorModule(Module):
    def configure(self, binder):
        binder.bind(TokenService, to=TokenService, scope=singleton)


class TokenizerProvider(Module):
    def configure(self, binder):
        config = get_config()
        tokenizer = Tokenizer(config.JWT_SECRET_KEY, config.JWT_ALGORITHM)
        binder.bind(Tokenizer, to=tokenizer, scope=singleton)


providers_list = [TokenizerProvider, ServicesInjectorModule]
