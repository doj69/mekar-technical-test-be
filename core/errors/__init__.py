from http import HTTPStatus
from typing import Literal

from pydantic import BaseModel


class ErrorDetail(BaseModel):
    code: str
    message: str


class ApplicationError(Exception):
    status: Literal["success", "error"] = "error"
    status_code: int = HTTPStatus.BAD_REQUEST
    error: ErrorDetail = ErrorDetail(
        code="aplication.error", message=HTTPStatus.BAD_REQUEST.description
    )

    def __init__(self, message="", code: str = error.code):
        if message:
            self.error.message = message
            self.error.code = code

    def to_dict(self):
        return dict(
            status=self.status,
            status_code=self.status_code,
            error=self.error.model_dump(),
        )


class UnauthorizedError(ApplicationError):
    status_code = HTTPStatus.UNAUTHORIZED
    message = HTTPStatus.UNAUTHORIZED.description
    error = ErrorDetail(
        code="unauthorized.error", message=HTTPStatus.UNAUTHORIZED.description
    )


# class CustomValidationError(BaseModel):
