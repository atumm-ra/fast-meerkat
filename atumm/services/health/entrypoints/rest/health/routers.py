from classy_fastapi import Routable, get
from fastapi import Response


class HealthRouter(Routable):
    """Home router."""

    def __init__(self):
        super().__init__(prefix="")

    @get("/health")
    async def home(self):
        return Response(status_code=200)


health_router = HealthRouter().router
