from sql_database import Base
from sqlalchemy import Column, ForeignKey, Integer, String, Text, TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship


class Review(Base):
    __tablename__ = "Reviews"
    # review_id = Column(Integer, nullable=False, unique=True)
    desc = Column(Text, nullable=False)
    rating = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey(
        "Users.user_id", ondelete="CASCADE"), nullable=False, primary_key=True,)
    item_id = Column(Integer, ForeignKey(
        "Items.item_id", ondelete="CASCADE"), nullable=False, primary_key=True, )
