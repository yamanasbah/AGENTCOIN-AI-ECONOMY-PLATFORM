from fastapi import FastAPI, WebSocket, WebSocketDisconnect

from app.api.v1.router import api_router
from app.core.config import settings
from app.websocket.manager import manager

app = FastAPI(title=settings.app_name)
app.include_router(api_router, prefix=settings.api_v1_prefix)


@app.websocket("/ws/{channel}")
async def websocket_endpoint(websocket: WebSocket, channel: str):
    await manager.connect(channel, websocket)
    try:
        while True:
            message = await websocket.receive_text()
            await manager.broadcast(channel, {"channel": channel, "message": message})
    except WebSocketDisconnect:
        manager.disconnect(channel, websocket)
