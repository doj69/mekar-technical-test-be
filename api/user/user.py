import logging
from http import HTTPStatus

from fastapi import APIRouter

from api.schema import reponse, request
from api.schema.base import BaseResponseAPISchema
from api.schema.reponse.user import UserData
from app.user.services.user_svc import UserService

user_router = APIRouter()

logger = logging.getLogger(__name__)


@user_router.post(
    "", status_code=HTTPStatus.CREATED, response_model=BaseResponseAPISchema
)
async def create_user(data: request.CreateUserRequest):
    user = await UserService().create_user(data)
    response_data = UserData.model_validate(user, from_attributes=True)

    return reponse.CreateUserResponse(data=response_data)
