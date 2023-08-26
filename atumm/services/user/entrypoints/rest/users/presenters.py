from atumm.core.presenter import AbstractPresenter
from atumm.services.user.domain.models import UserModel
from atumm.services.user.entrypoints.rest.users.responses import RegisterResponse


class UserPresenter(AbstractPresenter[UserModel, RegisterResponse]):
    def present(self, user: UserModel) -> RegisterResponse:
        return RegisterResponse(**user.dict())
