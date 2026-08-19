from fastapi.routing import APIRouter

from app.domain.schemas.game import ScraperGame
from app.infrastructure.services.futbol import get_matches

router = APIRouter(prefix="/api/v1/matches", tags=["matches"])


@router.get("/today")
async def today_matches() -> list[ScraperGame]:
    return await get_matches("today")


@router.get("/{day:path}")
async def matches(day: str) -> list[ScraperGame]:
    day = day.replace("/", "-")
    return await get_matches(day)
