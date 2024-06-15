from sqlalchemy import Column, Date, Integer, String

from db.timestamp_mixin import Base


class User(Base):
    """user database model"""

    # id: orm.Mapped[int] = orm.mapped_column(primary_key=True, index=True)
    # name: orm.Mapped[str] = orm.mapped_column(nullable=False)
    # identify_number: orm.Mapped[str] = orm.mapped_column(nullable=False, unique=True)
    # email: orm.Mapped[str] = orm.mapped_column(nullable=False, unique=True)
    # date_of_birth: orm.Mapped[date] = orm.mapped_column(nullable=False)
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(25), nullable=False)
    identity_number = Column(String(25), nullable=False, unique=True)
    email = Column(String(50), nullable=False, unique=True)
    date_of_birth = Column(Date, nullable=False)

    __tablename__ = "users"
