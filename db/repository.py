from typing import Generic, TypeVar

from sqlalchemy import BinaryExpression, select, update

from db.session import session
from db.timestamp_mixin import Base

Model = TypeVar("Model", bound=Base)


class DatabaseRepository(Generic[Model]):
    """Repository for performing database queries."""

    def __init__(self, model: type[Model]) -> None:
        self.model = model

    async def create(self, data: dict) -> Model:
        instance = self.model(**data)
        session.add(instance)
        return instance

    async def get(self, id: int) -> Model | None:
        return session.get(self.model, id)

    async def update(self, id: int, data: dict):
        stmt = (
            update(self.model)
            .where(self.model.id == id)
            .execution_options(synchronize_session=False)
        )
        for k, v in data.items():
            stmt = stmt.values({k: v})

        return session.execute(stmt)

    async def filter(
        self,
        *expressions: BinaryExpression,
    ) -> list[Model]:
        query = select(self.model)
        if expressions:
            query = query.where(*expressions)
        return list(session.scalars(query))
