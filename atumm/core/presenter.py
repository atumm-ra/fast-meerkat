from abc import abstractmethod
from typing import Generic, List, TypeVar

InputType = TypeVar("InputType")
OutputType = TypeVar("OutputType")


class AbstractPresenter(Generic[InputType, OutputType]):
    @abstractmethod
    def present(self, item: InputType) -> OutputType:
        pass

    def present_list(self, items: List[InputType]) -> List[OutputType]:
        return [self.present(item) for item in items]
