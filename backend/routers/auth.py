# backend/routers/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import models, schemas, database

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post("/register", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserLogin, db: Session = Depends(database.get_db)):
    existing_user = db.query(models.User).filter(models.User.user_id == user.user_id).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User ID already registered")
    
    new_user = models.User(user_id=user.user_id, password=user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login", response_model=schemas.UserResponse)
def login(user_credentials: schemas.UserLogin, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.user_id == user_credentials.user_id).first()
    
    # Simple plain-text password check for lightweight app
    if not user or user.password != user_credentials.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid User ID or Password"
        )
    
    return user
