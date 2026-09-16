import logging
from datetime import UTC, datetime, timedelta

import httpx
from fastapi import HTTPException, status
from httpx import AsyncClient
from pydantic import TypeAdapter

from app.core.config import settings
from app.domain.schemas.game import ScraperGame

logger = logging.getLogger(__name__)
POLL_INTERVAL = 15


async def get_matches(day: str) -> list[ScraperGame]:
    if day == "yesterday":
        target_date = datetime.now(UTC) - timedelta(days=1)
    elif day == "today":
        target_date = datetime.now(UTC)
    else:
        target_date = None

    date_str = target_date.strftime("%d-%m-%Y") if target_date else day

    try:
        async with AsyncClient() as client:
            response = await client.get(f"{settings.FUTBOL_SCRAPER_URL}/matches/{day}")
            _ = response.raise_for_status()

        return TypeAdapter(list[ScraperGame]).validate_python(response.json())

    except httpx.RequestError:
        logger.exception(
            "failed to connect to scraper microservice at %s. day: %s",
            settings.FUTBOL_SCRAPER_URL,
            date_str,
        )
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="scraper service service is unavailable",
        ) from None


# async def poll_live_futbol_matches() -> None:
#     previous: list[ScraperGame] = []

#     while True:
#         try:
#             current = await get_matches("today")

#             if current:
#                 db = SessionLocal()
#                 try:
#                     repo = GameRepository(db)
#                     service = GameService(repo)
#                     _ = service.persist_finished_matches(current)
#                 finally:
#                     db.close()

#                 if current != previous:
#                     await manager.broadcast({"type": "live_update", "matches": current})
#                     previous = current

#         except Exception:
#             logger.exception("live poll failed")

#         await asyncio.sleep(POLL_INTERVAL)
