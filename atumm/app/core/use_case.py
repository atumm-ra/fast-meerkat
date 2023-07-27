from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from pydantic import BaseModel


class Command(BaseModel, ABC):
    pass


class Query(BaseModel, ABC):
    pass


class UseCase(ABC):
    pass


CommandType = TypeVar("CommandType", bound=Command)
QueryType = TypeVar("QueryType", bound=Query)


class CommandUseCase(UseCase, Generic[CommandType]):
    @abstractmethod
    async def execute(self, command: CommandType):
        pass


class QueryUseCase(UseCase, Generic[QueryType]):
    @abstractmethod
    async def execute(self, query: QueryType):
        pass
