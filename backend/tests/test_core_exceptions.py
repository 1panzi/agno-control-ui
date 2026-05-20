import pytest
from core.exceptions import (
    AppException,
    NotFoundError,
    ConflictError,
    UnprocessableError,
    ForbiddenError,
    CustomException,
)


def test_app_exception_default_status():
    exc = AppException("test error")
    assert exc.status_code == 500
    assert exc.message == "test error"


def test_not_found_error():
    exc = NotFoundError("not found")
    assert exc.status_code == 404


def test_conflict_error():
    exc = ConflictError("conflict")
    assert exc.status_code == 409


def test_unprocessable_error():
    exc = UnprocessableError("unprocessable")
    assert exc.status_code == 422


def test_forbidden_error():
    exc = ForbiddenError("forbidden")
    assert exc.status_code == 403


def test_custom_exception_default_status():
    exc = CustomException(msg="bad request")
    assert exc.status_code == 400
    assert exc.message == "bad request"


def test_custom_exception_custom_status():
    exc = CustomException(msg="not found", status_code=404)
    assert exc.status_code == 404


def test_custom_exception_is_app_exception():
    exc = CustomException(msg="err")
    assert isinstance(exc, AppException)
