from typing import Dict, List, Optional, Tuple

from pydantic import BaseModel

from atumm.app.core.exceptions import RuntimeException


class ExceptionDetailResponse(BaseModel):
    type: str
    reason: str
    metadata: Optional[Dict[str, str]]


class RuntimeExceptionResponse(BaseModel):
    code: int
    message: str
    status: str
    details: Optional[List[ExceptionDetailResponse]]


def map_exception_to_response(
    exception: RuntimeException,
) -> Tuple[int, RuntimeExceptionResponse]:
    details = (
        [ExceptionDetailResponse(**detail.dict()) for detail in exception.details]
        if exception.details
        else None
    )
    response = RuntimeExceptionResponse(
        code=exception.code,
        message=exception.message,
        status=str(exception.status),
        details=details,
    )
    return response.code, response
