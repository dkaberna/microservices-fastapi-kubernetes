from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Column, Integer, String

from main.core.security import get_password_hash
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text, null
from main.db.base_class import Base


class User(Base):
    #__tablename__ = "user" # now defined in db.base_class
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'))
    disabled = Column(Boolean, default=False)

    def __init__(
        self, username: str, email: str, password: str
    ) -> None:
        self.username = username
        self.email = email
        self.password = get_password_hash(password=password)