from atumm.app.infra.buti.components.beanie import BeanieComponent
from atumm.app.infra.buti.components.config import ConfigComponent
from atumm.app.infra.buti.components.fastapi import (
    AuthJWTComponent,
    FastAPIComponent,
    FastAPIMiddlewaresComponent,
    ListenersComponent,
    RouterComponent,
)
from atumm.app.infra.buti.components.injector import InjectorComponent

app_components = [
    ConfigComponent(),
    FastAPIComponent(),
    RouterComponent(),
    FastAPIMiddlewaresComponent(),
    ListenersComponent(),
    AuthJWTComponent(),
    BeanieComponent(),
    InjectorComponent(),
]
