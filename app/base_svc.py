# from typing import TypeVar

# from db.repository import DatabaseRepository
# from db.timestamp_mixin import Base
# from db.transaction import TransactinHandler

# Model = TypeVar("Model", bound=Base)


# class ServiceBase:
#     session = TransactinHandler().session

#     def __init__(self, model: type[Model]) -> None:
#         self.repository = DatabaseRepository(model=model, session=self.session)
