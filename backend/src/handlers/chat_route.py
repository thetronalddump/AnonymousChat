import json
import logging

from fastapi import APIRouter
from starlette.websockets import WebSocket, WebSocketDisconnect

from config import manager

logger = logging.getLogger(__name__)

chat_router = APIRouter()


@chat_router.websocket("/ws/{room_id}/{username}")
async def chat_websocket(websocket: WebSocket, room_id: int, username: str) -> None:
    await manager.connect(room_id, websocket)
    logger.info(f"Connected user {username} to room {room_id}")
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_to_room(
                room_id, json.dumps({"username": username, "data": data})
            )
    except WebSocketDisconnect as e:
        await manager.disconnect(room_id, websocket)
        logger.error("User disconnected", exc_info=e)
