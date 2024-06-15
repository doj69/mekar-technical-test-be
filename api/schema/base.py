from typing import Generic, Literal, TypeVar

from pydantic import BaseModel

# class ExceptionResponseSchema(BaseModel):
#     """A schema for return object of exception response"""


Data = TypeVar("Data", bound=BaseModel)


class BaseResponseAPISchema(BaseModel, Generic[Data]):
    """A schema for base response API"""

    status: Literal["success", "error"]
    status_code: int
    data: type[Data]
