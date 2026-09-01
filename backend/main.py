# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine
from . import models
from .websocket import chat
from .routers import auth
from .routers import messages, inventory

app.include_router(messages.router)   
app.include_router(inventory.router)
app.include_router(auth.router)
app.include_router(chat.router) 
# Tables automatic-aaga create aaga intha line thevai
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Mshop InventoryChat API")

# CORS middleware for Android app communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"status": "Mshop API is running successfully"}

