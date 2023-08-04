from abc import ABC
from typing import Generic, TypeVar

from beanie import Document

from atumm.core.data_providers.provider import DataProvider

DocumentType = TypeVar("DocumentType", bound=Document)


class BeanieDataProvider(DataProvider, Generic[DocumentType]):
    pass
