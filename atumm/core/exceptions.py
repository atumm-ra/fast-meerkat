from enum import Enum, StrEnum, auto
from typing import Dict, List, Optional


class DomainException(Exception):
    pass


class ErrorStatus(StrEnum):
    INTERNAL_ERROR = auto()
    TOKEN_ERROR = auto()
    VALIDATION_ERROR = auto()


class ExceptionDetail:
    def __init__(
        self, type: str, reason: str, metadata: Optional[Dict[str, str]] = None
    ):
        self.type = type
        self.reason = reason
        self.metadata = metadata

    def dict(self):
        return {
            "type": self.type,
            "reason": self.reason,
            "metadata": self.metadata,
        }


class RuntimeException(Exception):
    def __init__(
        self,
        code: int,
        message: str,
        status: ErrorStatus,
        details: Optional[List[ExceptionDetail]] = None,
    ):
        self.code = code
        self.message = message
        self.status = status
        self.details = details
        super().__init__(self.message)

    def dict(self):
        return {
            "code": self.code,
            "message": self.message,
            "status": self.status.value,
            "details": [detail.dict() for detail in self.details]
            if self.details
            else None,
        }
