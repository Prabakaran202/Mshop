# backend/routers/inventory.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas, database

router = APIRouter(
    prefix="/inventory",
    tags=["Inventory"]
)

@router.get("/", response_model=List[schemas.InventoryResponse])
def get_inventory(db: Session = Depends(database.get_db)):
    items = db.query(models.Inventory).order_by(models.Inventory.created_at.desc()).all()
    return items
