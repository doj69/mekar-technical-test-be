import logging
from enum import Enum
from functools import wraps

from sqlalchemy.exc import SQLAlchemyError

from db.session import session

logger = logging.getLogger(__name__)


class Transaction:
    def __call__(self, function):
        @wraps(function)
        async def decorator(*args, **kwargs):
            try:
                result = await self.run_requires_new(
                    function=function,
                    args=args,
                    kwargs=kwargs,
                )
            except SQLAlchemyError as e:
                session.rollback()
                logger.exception(e)
                raise e
            return result

        return decorator

    async def run_requires_new(self, function, args, kwargs):
        if not session.is_active:
            session.begin()
        result = await function(*args, **kwargs)
        session.commit()
        return result

    def __enter__(self):
        return session

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            session.commit()
        except Exception as e:
            session.rollback()
            logger.exception(e)
            raise e
