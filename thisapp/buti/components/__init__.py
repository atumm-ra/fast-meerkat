from thisapp.buti.components.beanie import BeanieComponent
from thisapp.buti.components.config import ConfigComponent
from thisapp.buti.components.fastapi import (
    AuthJWTComponent,
    FastAPIComponent,
    FastAPIMiddlewaresComponent,
    ListenersComponent,
)
from thisapp.buti.components.health_service import HealthServiceComponent
from thisapp.buti.components.injector import InjectorComponent
from thisapp.buti.components.user_service import UserServiceComponent

app_components = [
    ConfigComponent(),
    FastAPIComponent(),
    FastAPIMiddlewaresComponent(),
    ListenersComponent(),
    AuthJWTComponent(),
    InjectorComponent(),
    BeanieComponent(),
    UserServiceComponent(),
    HealthServiceComponent(),
]
