# backend/websocket/chat.py
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.orm import Session
from datetime import datetime

from .. import database, models
from ..services.parser import parse_inventory_message

router = APIRouter()

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            await connection.send_json(message)

manager = ConnectionManager()

# Generator dependency for websocket
def get_ws_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.websocket("/ws/chat/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str, db: Session = Depends(get_ws_db)):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            
            # 1. Save chat message to database
            new_msg = models.Message(user_id=user_id, message_text=data)
            db.add(new_msg)
            db.commit()
            db.refresh(new_msg)

            response_data = {
                "type": "chat_message",
                "user_id": user_id,
                "message_text": data,
                "timestamp": new_msg.timestamp.isoformat()
            }

            # 2. Check for "Delivered" update (e.g., "Delivered 1001")
            if data.lower().startswith("delivered"):
                parts = data.split()
                if len(parts) == 2 and parts[1].isdigit():
                    inv_id = int(parts[1])
                    inv_item = db.query(models.Inventory).filter(models.Inventory.inventory_id == inv_id).first()
                    if inv_item and inv_item.status != "Delivered":
                        inv_item.status = "Delivered"
                        inv_item.delivered_at = datetime.utcnow()
                        inv_item.confirmed_by_user = user_id
                        db.commit()
                        response_data["inventory_update"] = {"inventory_id": inv_id, "status": "Delivered"}

            # 3. Check for new inventory entry using parser
            parsed_inv = parse_inventory_message(data)
            if parsed_inv:
                new_inv = models.Inventory(
                    raw_message=data,
                    item_name=parsed_inv["item_name"],
                    category=parsed_inv["category"],
                    price=parsed_inv["price"],
                    customer_name=parsed_inv["customer_name"]
                )
                db.add(new_inv)
                db.commit()
                db.refresh(new_inv)
                response_data["new_inventory"] = {"inventory_id": new_inv.inventory_id, "status": "Pending"}

            # Broadcast to all 5 users
            await manager.broadcast(response_data)

    except WebSocketDisconnect:
        manager.disconnect(websocket)
