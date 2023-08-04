from thisapp.buti.components.beanie import BeanieComponent
from thisapp.buti.components.config import ConfigComponent
from thisapp.buti.components.fastapi import (
    AuthJWTComponent,
    FastAPIComponent,
    FastAPIMiddlewaresComponent,
    ListenersComponent,
    RouterComponent,
)
from thisapp.buti.components.injector import InjectorComponent

app_components = [
    ConfigComponent(),
    FastAPIComponent(),
    RouterComponent(),
    FastAPIMiddlewaresComponent(),
    ListenersComponent(),
    AuthJWTComponent(),
    InjectorComponent(),
    BeanieComponent(),
]
