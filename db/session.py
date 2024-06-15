# from collections.abc import AsyncGenerator

# from sqlalchemy import exc
# from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

# from core.config.app import settings

# __db_url = settings.get_db_connection()


# async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
#     engine = create_async_engine(url=__db_url)
#     factory = async_sessionmaker(bind=engine, autoflush=True)
#     async with factory() as session:
#         try:
#             yield session
#             await session.commit()
#         except exc.SQLAlchemyError:
#             await session.rollback()
#             raise


from contextvars import ContextVar, Token
from typing import Union

from sqlalchemy.engine import create_engine
from sqlalchemy.orm import Session, scoped_session, sessionmaker

from core.config.app import settings

session_context: ContextVar[str] = ContextVar("session_context")


# def get_session_id() -> str:
#     ctx = session_context.get()
#     return ctx


# def set_session_context(session_id: str) -> Token:
#     ctx = session_context.set(session_id)
#     return ctx


# def reset_session_context(context: Token) -> None:
#     session_context.reset(context)


__db_url = settings.get_db_connection()
engine = create_engine(url=__db_url, echo=settings.ECHO, pool_pre_ping=True)

# Create a sessionmaker bound to the engine
session: Session = sessionmaker(autoflush=False, bind=engine)()
