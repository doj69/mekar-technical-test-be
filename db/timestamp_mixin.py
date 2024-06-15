from sqlalchemy import Column, DateTime, Integer, String, func, orm


class Base(orm.DeclarativeBase):
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    created_by = Column(String(100), default="system", nullable=False)
    updated_at = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = Column(String(100), default="system", nullable=False)
