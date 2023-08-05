from atumm.core.exceptions import ErrorStatus, ExceptionDetail, RuntimeException


class UnauthorizedException(RuntimeException):
    def __init__(self):
        super().__init__(
            code=401,
            message="Unauthorized",
            status=ErrorStatus.TOKEN_ERROR,
            details=[
                ExceptionDetail(type="UnauthorizedException", reason="Unauthorized")
            ],
        )


class PasswordsDoNotMatchException(RuntimeException):
    def __init__(self):
        super().__init__(
            code=400,
            message="password does not match",
            status=ErrorStatus.TOKEN_ERROR,
            details=[
                ExceptionDetail(
                    type="PasswordsDoNotMatchException",
                    reason="password does not match",
                )
            ],
        )


class AccountLockedException(RuntimeException):
    def __init__(self):
        super().__init__(
            code=401,
            message="Account Locked",
            status=ErrorStatus.TOKEN_ERROR,
            details=[
                ExceptionDetail(
                    type="DeviceChangeDetectedException",
                    reason="different device used to login",
                )
            ],
        )


class DuplicateEmailOrUsernameException(RuntimeException):
    def __init__(self):
        super().__init__(
            code=400,
            message="duplicate email or username",
            status=ErrorStatus.VALIDATION_ERROR,
            details=[
                ExceptionDetail(
                    type="DuplicateEmailOrUsernameException",
                    reason="duplicate email or username",
                )
            ],
        )


class UserNotFoundException(RuntimeException):
    def __init__(self):
        super().__init__(
            code=404,
            message="user not found",
            status=ErrorStatus.VALIDATION_ERROR,
            details=[
                ExceptionDetail(type="UserNotFoundException", reason="user not found")
            ],
        )


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
