from abc import ABCMeta, abstractmethod

from db import models
from db.session import session


class UserRepository:
    __metaclass__ = ABCMeta

    @abstractmethod
    async def create(self, user: dict) -> models.User:
        pass

    @abstractmethod
    async def is_exists_identity(self, identity: str) -> bool:
        pass

    @abstractmethod
    async def is_exists_email(self, email: str) -> bool:
        pass


class UserPostgresRepo(UserRepository):
    async def create(self, user: dict) -> models.User:
        model = models.User(**user)
        session.add(model)
        session.flush()
        return model

    async def is_exists_identity(self, identity: str) -> bool:
        result: int = (
            session.query(models.User)
            .filter(models.User.identity_number == identity)
            .count()
        )

        return bool(result)

    async def is_exists_email(self, email: str) -> bool:
        result: int = (
            session.query(models.User).filter(models.User.email == email).count()
        )

        return bool(result)
