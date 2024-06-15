from datetime import date
from http import HTTPStatus
from typing import Literal

from pydantic import BaseModel

from api.schema.base import BaseResponseAPISchema


class UserData(BaseModel):
    name: str
    identity_number: str
    email: str
    date_of_birth: date


class CreateUserResponse(BaseResponseAPISchema):
    status: Literal["success", "error"] = "success"
    status_code: int = HTTPStatus.CREATED
    data: UserData
