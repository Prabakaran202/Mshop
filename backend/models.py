# backend/models.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)

class Inventory(Base):
    __tablename__ = "inventory"

    inventory_id = Column(Integer, primary_key=True, index=True)
    raw_message = Column(String, nullable=False)
    item_name = Column(String)
    category = Column(String)
    price = Column(Integer)
    customer_name = Column(String)
    status = Column(String, default="Pending")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    delivered_at = Column(DateTime(timezone=True))
    confirmed_by_user = Column(String, ForeignKey("users.user_id"))

class Message(Base):
    __tablename__ = "messages"

    message_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.user_id"), nullable=False)
    message_text = Column(String, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
