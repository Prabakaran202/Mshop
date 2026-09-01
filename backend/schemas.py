# backend/schemas.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# User Schemas
class UserLogin(BaseModel):
    user_id: str
    password: str

class UserResponse(BaseModel):
    id: int
    user_id: str

    class Config:
        from_attributes = True

# Inventory Schemas
class InventoryBase(BaseModel):
    raw_message: str
    item_name: Optional[str] = None
    category: Optional[str] = None
    price: Optional[int] = None
    customer_name: Optional[str] = None

class InventoryResponse(InventoryBase):
    inventory_id: int
    status: str
    created_at: datetime
    delivered_at: Optional[datetime] = None
    confirmed_by_user: Optional[str] = None

    class Config:
        from_attributes = True

# Message Schemas
class MessageCreate(BaseModel):
    user_id: str
    message_text: str

class MessageResponse(BaseModel):
    message_id: int
    user_id: str
    message_text: str
    timestamp: datetime

    class Config:
        from_attributes = True
