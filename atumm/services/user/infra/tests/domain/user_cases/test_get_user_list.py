import pytest
from unittest.mock import AsyncMock, MagicMock

from atumm.services.user.domain.core.repositories import AbstractUserRepo
from atumm.services.user.domain.use_cases.user_list import GetUserListQuery, GetUserListUseCase

class TestGetUserListUseCase:
    @pytest.mark.anyio
    async def test_execute(self):
        # Arrange
        mock_user_repo = MagicMock(spec=AbstractUserRepo)
        mock_user_repo.find_all = AsyncMock(return_value=["user1", "user2", "user3"])

        use_case = GetUserListUseCase(user_repo=mock_user_repo)

        query = GetUserListQuery(start=0, limit=3)

        # Act
        result = await use_case.execute(query)

        # Assert
        mock_user_repo.find_all.assert_called_once_with(start=0, limit=3)
        assert result == ["user1", "user2", "user3"]
