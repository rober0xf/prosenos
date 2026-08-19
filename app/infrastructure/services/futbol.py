import asyncio
import logging
from datetime import UTC, datetime

from fastapi import HTTPException, status
from httpx import AsyncClient, ConnectError
from pydantic import TypeAdapter

from app.core.config import settings
from app.core.database import SessionLocal
from app.domain.schemas.game import ScraperGame
from app.infrastructure.repositories.game import GameRepository
from app.infrastructure.services.connection_manager import manager
from app.infrastructure.services.game import GameService

logger = logging.getLogger(__name__)
POLL_INTERVAL = 15


async def get_matches(day: str) -> list[ScraperGame]:
    if day == "today":
        day = datetime.now(UTC).strftime("%d-%m-%Y")

    try:
        async with AsyncClient() as client:
            response = await client.get(f"{settings.FUTBOL_SCRAPER_URL}/matches/{day}")
            _ = response.raise_for_status()

            return TypeAdapter(list[ScraperGame]).validate_python(response.json())
    except ConnectError:
        logger.exception(
            "error to connect to scraper microservice at %s. day: %s",
            settings.FUTBOL_SCRAPER_URL,
            day,
        )
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Scraper service is unavailable",
        ) from None


async def poll_live_futbol_matches() -> None:
    previous: list[ScraperGame] = []

    while True:
        try:
            current = await get_matches("today")

            if current:
                db = SessionLocal()
                try:
                    repo = GameRepository(db)
                    svc = GameService(repo)
                    _ = svc.persist_finished_matches(current)
                finally:
                    db.close()

                if current != previous:
                    await manager.broadcast({"type": "live_update", "matches": current})
                    previous = current

        except Exception:
            logger.exception("live poll failed")
        await asyncio.sleep(POLL_INTERVAL)
