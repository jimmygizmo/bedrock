from sqlalchemy import Column, Integer, String
from magma.core.database import Base


# ########    SQLALCHEMY MODEL:  user    ########


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, unique=True, nullable=False)
    full_name = Column(String, nullable=True)

