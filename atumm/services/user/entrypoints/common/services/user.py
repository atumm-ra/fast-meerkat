from typing import List, Optional

from beanie.odm.operators.find.logical import And

from atumm.services.user.dataproviders.beanie.models import User
from atumm.services.user.domain.core.exceptions import UserNotFoundException


class UserService:
    def __init__(self):
        ...

    async def get_user_list(
        self,
        limit: int = 12,
        prev: Optional[int] = None,
    ) -> List[User]:
        find_kwargs = {}
        if prev:
            find_kwargs["id_lt"] = prev

        if limit > 12:
            limit = 12

        user_list = await User.find(find_kwargs).to_list(limit)
        return user_list

    async def is_admin(self, user_id: int) -> bool:
        user = await User.find_one(User.id == user_id)
        if not user:
            return False

        if user.is_admin is False:
            return False

        return True

    async def find_by_email(self, email: str) -> User:
        user = await User.find_one(
            And(User.email == email),
        )

        if not user:
            raise UserNotFoundException

        return user
