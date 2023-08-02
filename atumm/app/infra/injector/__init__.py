from injector import Injector

from atumm.app.infra.di.providers import app_providers
from atumm.user.infra.di.providers import user_providers

all_providers = user_providers + app_providers

injector = Injector(modules=all_providers)
