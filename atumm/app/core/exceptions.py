from enum import Enum
from typing import Dict, List, Optional


class DomainException(Exception):
    pass


class ErrorStatus(Enum):
    INTERNAL_ERROR = "INTERNAL_ERROR"
    TOKEN_ERROR = "TOKEN_ERROR"
    VALIDATION_ERROR = "VALIDATION_ERROR"


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
            "status": self.status,
            "details": [detail.dict() for detail in self.details]
            if self.details
            else None,
        }


class AssistantNotFound(RuntimeException):
    def __init__(self):
        super().__init__(500, "Internal Error", ErrorStatus.INTERNAL_ERROR, [])
