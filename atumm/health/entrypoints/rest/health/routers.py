from classy_fastapi import Routable, get
from fastapi import Depends, Response

from atumm.app.infra.fastapi.dependencies import AllowAll, PermissionDependency


class HealthRouter(Routable):
    """Home router."""

    def __init__(self):
        super().__init__(prefix="")

    @get("/health")
    async def home(
        self,
        permission: PermissionDependency = Depends(PermissionDependency([AllowAll])),
    ):
        return Response(status_code=200)


health_router = HealthRouter().router
