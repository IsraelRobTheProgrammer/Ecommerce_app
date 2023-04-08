from sql_database import Base
from sqlalchemy import Column, ForeignKey, Integer, String, Text, TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship

# Database Table Schema

print(type(Base), "item")

class Item(Base):
    __tablename__ = "Items"

    item_id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    desc = Column(Text, nullable=False)
    inventory = Column(Integer, server_default="0", nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"))
    user_id = Column(Integer, ForeignKey(
        "Users.user_id", ondelete="CASCADE"), nullable=False)
    owner = relationship("User", foreign_keys=[user_id])
    
    # review_id = Column(Integer, ForeignKey(
    #     "Reviews.review_id", ondelete="CASCADE"), nullable=False)
    # review = relationship("Review", foreign_keys=[review_id])
