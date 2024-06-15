from datetime import date

from pydantic import BaseModel, EmailStr, Field


class CreateUserRequest(BaseModel):
    name: str = Field(max_length=25)
    identity_number: str = Field(max_length=50)
    email: EmailStr
    date_of_birth: date
