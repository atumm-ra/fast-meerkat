from atumm.core.exceptions import ErrorStatus, ExceptionDetail, RuntimeException


class DecodeTokenException(RuntimeException):
    def __init__(self):
        super().__init__(
            code=400,
            message="token decode error",
            status=ErrorStatus.TOKEN_ERROR,
            details=[
                ExceptionDetail(
                    type="DecodeTokenException", reason="token decode error"
                )
            ],
        )


class InvalidRefreshSubject(RuntimeException):
    def __init__(self):
        super().__init__(
            code=400,
            message="invalid subject in token creation",
            status=ErrorStatus.TOKEN_ERROR,
            details=[
                ExceptionDetail(
                    type="InvalidRefreshSubject",
                    reason="invalid subject in token creation",
                )
            ],
        )


class ExpiredTokenException(RuntimeException):
    def __init__(self):
        super().__init__(
            code=400,
            message="expired token",
            status=ErrorStatus.TOKEN_ERROR,
            details=[
                ExceptionDetail(type="ExpiredTokenException", reason="expired token")
            ],
        )
