from __future__ import annotations


class AppException(Exception):
    status_code: int = 500

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)


class NotFoundError(AppException):
    status_code = 404


class ConflictError(AppException):
    status_code = 409


class UnprocessableError(AppException):
    status_code = 422


class ForbiddenError(AppException):
    status_code = 403


class CustomException(AppException):
    """兼容 resource/service.py 调用方式的业务异常。"""
    def __init__(self, msg: str, status_code: int = 400) -> None:
        super().__init__(message=msg)
        self.status_code = status_code
