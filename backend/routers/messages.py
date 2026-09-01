# backend/routers/messages.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas, database

router = APIRouter(
    prefix="/messages",
    tags=["Messages"]
)

@router.get("/", response_model=List[schemas.MessageResponse])
def get_messages(db: Session = Depends(database.get_db), limit: int = 100):
    # Palaiya messages-ai order-aaga edukka
    messages = db.query(models.Message).order_by(models.Message.timestamp.asc()).limit(limit).all()
    return messages
