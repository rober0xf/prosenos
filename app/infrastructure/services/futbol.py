import logging

from fastapi import HTTPException, status
from httpx import AsyncClient, ConnectError

from app.core.config import settings

logger = logging.getLogger(__name__)


async def get_matches(day: str):
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
            detail="Scraper service is unavailable",
        ) from None
