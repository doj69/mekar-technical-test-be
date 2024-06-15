from pythondi import inject

from api.schema import request
from app.user import repository
from app.user.errors import UniqueError
from db.transaction import Transaction


class UserService:
    @inject()
    def __init__(
        self, user_repo: repository.UserRepository = repository.UserRepository()
    ):
        self.user_repo = user_repo

    async def create_user(self, param: request.CreateUserRequest):
        exists_identity = await self.user_repo.is_exists_identity(param.identity_number)
        if exists_identity:
            raise UniqueError(message="identity number must be unique")
        exists_email = await self.user_repo.is_exists_email(param.email)
        if exists_email:
            raise UniqueError(message="email must be unique")

        with Transaction():
            result = await self.user_repo.create(param.model_dump())
        return result
