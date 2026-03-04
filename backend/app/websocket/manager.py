from collections import defaultdict

from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.connections: dict[str, list[WebSocket]] = defaultdict(list)

    async def connect(self, channel: str, websocket: WebSocket):
        await websocket.accept()
        self.connections[channel].append(websocket)

    def disconnect(self, channel: str, websocket: WebSocket):
        if websocket in self.connections[channel]:
            self.connections[channel].remove(websocket)

    async def broadcast(self, channel: str, message: dict):
        for connection in self.connections[channel]:
            await connection.send_json(message)


manager = ConnectionManager()
