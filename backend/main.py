from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine
from . import models

# Routers import
from .routers import auth, messages, inventory
from .websocket import chat

# Database tables create seiya
models.Base.metadata.create_all(bind=engine)

# INTHA VARI KANDIPAAGA ROUTERS-KKU MUNNAL IRUKKA VENDUM
app = FastAPI(title="Mshop InventoryChat API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers-ai inaikkum paguthi (app define aanatharku piragu)
app.include_router(auth.router)
app.include_router(messages.router)
app.include_router(inventory.router)
app.include_router(chat.router)

@app.get("/")
def read_root():
    return {"status": "Mshop API is running successfully"}
