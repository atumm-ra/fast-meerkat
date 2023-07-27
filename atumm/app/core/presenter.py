from typing import Generic, List, TypeVar

InputType = TypeVar("InputType")
OutputType = TypeVar("OutputType")


class AbstractCollectionPresenter(Generic[InputType, OutputType]):
    @staticmethod
    def present(item: InputType) -> OutputType:
        raise NotImplementedError

    @staticmethod
    def present_list(items: List[InputType]) -> List[OutputType]:
        raise NotImplementedError


class AbstractSinglePresenter(Generic[InputType, OutputType]):
    @staticmethod
    def present(item: InputType) -> OutputType:
        raise NotImplementedError
