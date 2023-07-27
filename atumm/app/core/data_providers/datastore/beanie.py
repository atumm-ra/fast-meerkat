from abc import ABC
from typing import Generic, TypeVar

from beanie import Document

from atumm.app.core.provider_definitions import DataProvider

DocumentType = TypeVar("DocumentType", bound=Document)


class BeanieDataProvider(DataProvider, Generic[DocumentType]):
    pass
