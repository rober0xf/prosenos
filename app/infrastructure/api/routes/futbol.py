from fastapi.routing import APIRouter

from app.infrastructure.services.futbol import get_matches

router = APIRouter(prefix="/api/v1/matches", tags=["matches"])


@router.get("/today")
async def today_matches():
    return await get_matches("today")


@router.get("/{day:path}")
async def matches(day: str):
    day = day.replace("/", "-")
    return await get_matches(day)
