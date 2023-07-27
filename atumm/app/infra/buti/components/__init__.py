from atumm.app.infra.buti.components.config import ConfigComponent
from atumm.app.infra.buti.components.fastapi import (
    AuthJWTComponent,
    FastAPIComponent,
    FastAPIMiddlewaresComponent,
    ListenersComponent,
    RouterComponent,
)

app_components = [
    ConfigComponent(),
    FastAPIComponent(),
    RouterComponent(),
    FastAPIMiddlewaresComponent(),
    ListenersComponent(),
    AuthJWTComponent(),
]
