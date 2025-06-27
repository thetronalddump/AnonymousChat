from starlette.websockets import WebSocket


class ConnectionManager:
    def __init__(self) -> None:
        # room_id -> list of WebSockets
        self.active_connections: dict[str, list[WebSocket]] = {}

    async def connect(self, room_id: str, websocket: WebSocket) -> None:
        await websocket.accept()
        self.active_connections.setdefault(room_id, []).append(websocket)

    async def disconnect(self, room_id: str, websocket: WebSocket) -> None:
        if room_id in self.active_connections:
            self.active_connections[room_id].remove(websocket)
            if not self.active_connections[room_id]:
                del self.active_connections[room_id]

    async def send_to_room(self, room_id: str, message: str) -> None:
        if room_id in self.active_connections:
            for connection in self.active_connections[room_id]:
                await connection.send_text(message)
