import asyncio
import logging
from datetime import UTC, datetime

from fastapi import HTTPException, status
from httpx import AsyncClient, ConnectError

from app.core.config import settings
from app.core.database import SessionLocal
from app.infrastructure.repositories.game import GameRepository
from app.infrastructure.services.connection_manager import manager
from app.infrastructure.services.game import GameService

logger = logging.getLogger(__name__)
POLL_INTERVAL = 15


async def get_matches(day: str):
    if day == "today":
        day = datetime.now(UTC).strftime("%d-%m-%Y")

    try:
        async with AsyncClient() as client:
            response = await client.get(f"{settings.FUTBOL_SCRAPER_URL}/matches/{day}")
            response.raise_for_status()
            return response.json()
    except ConnectError:
        logger.exception(
            "error to connect to scraper microservice at %s. day: %s",
            settings.FUTBOL_SCRAPER_URL,
            day,
        )
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="scraper service is unavailable",
        ) from None


async def poll_live_futbol_matches() -> None:
    previous: list = []
    while True:
        try:
            current = await get_matches("today")

            if current:
                db = SessionLocal()
                try:
                    repo = GameRepository(db)
                    svc = GameService(repo)
                    svc.persist_finished_matches(current)
                finally:
                    db.close()

                if current != previous:
                    await manager.broadcast({"type": "live_update", "matches": current})
                    previous = current
        except Exception:
            logger.exception("live poll failed")
        await asyncio.sleep(POLL_INTERVAL)
