from sql_database import Base
from sqlalchemy import Column, Integer, String, Text, TIMESTAMP
from sqlalchemy.sql.expression import text


# Database Table Schema
class User(Base):
    __tablename__ = "Users"

    user_id = Column(Integer, primary_key=True, nullable=False)
    user_name = Column(String, nullable=False, unique=True)
    email = Column(Text, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"))
