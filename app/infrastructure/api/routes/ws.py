import logging

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.infrastructure.services.connection_manager import manager

logger = logging.getLogger(__name__)

router = APIRouter(tags=["websocket"])


@router.websocket("/ws/matches/live")
async def live_scores(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception:
        logger.exception("websocket error")
        manager.disconnect(websocket)
