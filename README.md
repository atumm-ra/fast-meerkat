# Fast Meerkat [WIP]

This is how the dependencies are linked, from the outermost (infrastructure) to the innermost (domain logic/interface adapters)

![dependency-graph](./docs/dependency-graph.png)



A typical service within this application should follow the following directory structure:
```
atumm/services/user

├── domain			# the innermost layer (domain logic)
│   ├── models.py
│   ├── repositories.py
│   ├── exceptions.py
│   └── usecases
│       ├── get_user.py
│       ├── login.py
│       ├── register.py
│       └── user_list.py

├── dataproviders		# concrete data providers
│   └── beanie
│       ├── models.py
│       └── repositories.py

├── entrypoints		 # entrypoints of the service, such as RESTful API endpoints, cli...etc

└── infra		# Contains infrastructure code including authentication, dependency injection, and testing.
    ├── di
    │   └── providers.py
    └── tests
        ├── conftest.py
        └── domain
            ├── test_user_model.py
            └── usecases
                ├── test_get_user_info.py
                ├── test_get_user_list.py
                ├── test_login.py
                └── test_register.py

```

To create the previous structure we can use the following command:
```bash
make new-svc <service-name>
```

Let's zoom in on the entrypoints part of the system, as you may know, these entrypoints, expose the applications' features through interfaces, whether rest, cli, workers ...etc.

If we examine the REST entrypoint structure we can see the following:

```
atumm/services/user/entrypoints/rest
├── tokens
│   ├── controllers.py
│   ├── presenters.py
│   ├── requests.py
│   ├── responses.py
│   └── routers.py
└── users
    ├── controllers.py
    ├── presenters.py
    ├── requests.py
    ├── responses.py
    └── routers.py
```

The example above, explains a service with 2 REST resources, where Classy FastAPI is used.

We can start with the routers to examine how this part of the system works.

Router: defining REST routes, along with the documentation for the OpenAPI endpoints, it delegates all the actual work to the controller
Controller: Handles any business logic (Assembles and execute the use cases), and returns a final representation for the router calls
Presenter: Present Business Objects.
Requests: Pydantic objects to be received
Responses: Pydantic objects for the response models.

```python
## routers.py
from classy_fastapi import Routable, post
from injector import inject

from atumm.core.entrypoints.rest.responses import RuntimeExceptionResponse
from atumm.services.user.entrypoints.rest.tokens.controllers import TokensController
from atumm.services.user.entrypoints.rest.tokens.requests import (
    LoginRequest,
    RefreshTokenRequest,
)
from atumm.services.user.entrypoints.rest.tokens.responses import (
    AuthenticatedTokensResponse,
)


class TokensRouter(Routable):
    @inject
    def __init__(self, controller: TokensController):
        super().__init__(prefix="/tokens")
        self.controller = controller

    @post(
        "/refresh",
        responses={
            "200": {"model": AuthenticatedTokensResponse},
            "400": {"model": RuntimeExceptionResponse},
            "401": {"model": RuntimeExceptionResponse},
        },
    )
    async def refresh_token(
        self, request: RefreshTokenRequest
    ) -> AuthenticatedTokensResponse:
        return await self.controller.refresh_token(request)

    @post(
        "/access",
        responses={
            "200": {"model": AuthenticatedTokensResponse},
            "401": {"model": RuntimeExceptionResponse},
            "404": {"model": RuntimeExceptionResponse},
        },
    )
    async def login(self, request: LoginRequest) -> AuthenticatedTokensResponse:
        return await self.controller.login(request)


## controllers.py
from injector import inject

from atumm.services.user.domain.usecases.login import LoginCommand, LoginUseCase
from atumm.services.user.domain.usecases.refresh_token import (
    RefreshTokenCommand,
    RefreshTokenUseCase,
)
from atumm.services.user.entrypoints.rest.tokens.presenters import TokenPresenter
from atumm.services.user.entrypoints.rest.tokens.requests import (
    LoginRequest,
    RefreshTokenRequest,
)
from atumm.services.user.entrypoints.rest.tokens.responses import (
    AuthenticatedTokensResponse,
)


class TokensController:
    @inject
    def __init__(
        self,
        presenter: TokenPresenter,
        refresh_token_use_case: RefreshTokenUseCase,
        login_use_case: LoginUseCase,
    ):
        self.presenter = presenter
        self.refresh_token_use_case = refresh_token_use_case
        self.login_use_case = login_use_case

    async def refresh_token(
        self, request: RefreshTokenRequest
    ) -> AuthenticatedTokensResponse:
        tokens = await self.refresh_token_use_case.execute(
            RefreshTokenCommand(
                token=request.token, refresh_token=request.refresh_token
            )
        )
        return self.presenter.present(tokens)

    async def login(self, request: LoginRequest) -> AuthenticatedTokensResponse:
        tokens = await self.login_use_case.execute(
            LoginCommand(
                email=request.email,
                password=request.password,
                device_id=request.device_id,
            )
        )
        return self.presenter.present(tokens)

## presenters.py
from atumm.core.presenter import AbstractPresenter
from atumm.services.user.entrypoints.rest.tokens.responses import (
    AuthenticatedTokensResponse,
)


class TokenPresenter(AbstractPresenter[dict, AuthenticatedTokensResponse]):
    def present(self, tokens: dict) -> AuthenticatedTokensResponse:
        return AuthenticatedTokensResponse(
            token=tokens["token"], refresh_token=tokens["refresh_token"]
        )

## requests.py
from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    email: str = Field(..., description="Email")
    password: str = Field(..., description="Password")
    device_id: str = Field(..., description="Device ID")


class RefreshTokenRequest(BaseModel):
    token: str = Field(..., description="Token")
    refresh_token: str = Field(..., description="Refresh token")


## responses.py
from pydantic import BaseModel, Field


class AuthenticatedTokensResponse(BaseModel):
    token: str = Field(..., description="Token")
    refresh_token: str = Field(..., description="Refresh token")


```


