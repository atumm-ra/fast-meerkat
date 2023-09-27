from atumm.services.user.infra.di.providers import user_providers
from injector import Injector

from thisapp.init.di.providers import app_providers

all_providers = app_providers + user_providers

injector = Injector(modules=all_providers)
