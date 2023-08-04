from typing import Dict, List, Optional, Tuple

from pydantic import BaseModel

from atumm.core.exceptions import RuntimeException


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
    response = RuntimeExceptionResponse(**exception.dict())
    return response.code, response
