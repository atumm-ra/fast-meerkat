from unittest.mock import AsyncMock, MagicMock

import pytest

from atumm.services.user.domain.repositories import AbstractUserRepo
from atumm.services.user.domain.usecases.get_users import GetUsersQuery, GetUsersUseCase


class TestGetUsersUsecase:
    @pytest.mark.anyio
    async def test_execute(self):
        mock_user_repo = MagicMock(spec=AbstractUserRepo)
        mock_user_repo.find_all = AsyncMock(return_value=["user1", "user2", "user3"])

        use_case = GetUsersUseCase(user_repo=mock_user_repo)

        query = GetUsersQuery(start=0, limit=3)

        result = await use_case.execute(query)

        mock_user_repo.find_all.assert_called_once_with(start=0, limit=3)
        assert result == ["user1", "user2", "user3"]
