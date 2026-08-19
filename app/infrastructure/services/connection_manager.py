import logging
from typing import TypedDict

from fastapi import WebSocket

from app.domain.schemas.game import ScraperGame

logger = logging.getLogger(__name__)


class LiveUpdateMessage(TypedDict):
    type: str
    matches: list[ScraperGame]


class ConnectionManager:
    active: list[WebSocket]

    def __init__(self) -> None:
        self.active = []

    async def connect(self, websocket: WebSocket) -> None:
        await websocket.accept()
        self.active.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active:
            self.active.remove(websocket)

    async def broadcast(self, message: LiveUpdateMessage):
        stale: list[WebSocket] = []

        for ws in list(self.active):
            try:
                await ws.send_json(message)
            except Exception as e:
                logger.warning("broadcast failed for %s: %s", ws.client, e)
                stale.append(ws)

        for ws in stale:
            self.disconnect(ws)


manager = ConnectionManager()
