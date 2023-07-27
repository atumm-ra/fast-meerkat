from typing import List, Optional

from atumm.app.core.exceptions import ErrorStatus, ExceptionDetail, RuntimeException


class DataProviderException(RuntimeException):
    def __init__(self, message: str, details: Optional[List[ExceptionDetail]] = None):
        super().__init__(500, message, ErrorStatus.INTERNAL_ERROR, details)


class DuplicateKeyException(DataProviderException):
    def __init__(self, key: str):
        super().__init__(
            f"Duplicate key exception: {key}",
            [
                ExceptionDetail(
                    type="DuplicateKeyException", reason=f"Key '{key}' already exists"
                )
            ],
        )


class OperationFailureException(DataProviderException):
    def __init__(self, operation: str):
        super().__init__(
            f"Operation failed: {operation}",
            [
                ExceptionDetail(
                    type="OperationFailureException",
                    reason=f"Operation '{operation}' failed",
                )
            ],
        )


class ItemDoesNotExistException(DataProviderException):
    def __init__(self, document_id: str):
        super().__init__(
            f"Document does not exist: {document_id}",
            [
                ExceptionDetail(
                    type="ItemDoesNotExistException",
                    reason=f"Document with ID '{document_id}' does not exist",
                )
            ],
        )
