import asyncio
import logging
from datetime import UTC, date, datetime, timedelta

from fastapi import HTTPException, status

from app.core.futbol import get_matches_by_date
from app.domain.schemas.game import ScraperGame
from app.domain.schemas.match import Match
from app.services.connection_manager import manager

logger = logging.getLogger(__name__)
POLL_INTERVAL = 15

_DATE_FORMAT = "%d-%m-%Y"


def _resolve_date(day: str) -> date:
    if day == "yesterday":
        return datetime.now(UTC).date() - timedelta(days=1)

    if day == "today":
        return datetime.now(UTC).date()

    try:
        return datetime.strptime(day, _DATE_FORMAT).date()
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Use date format: DD-MM-YYYY (e.g. 06-07-2026 or 06/07/2026)",
        ) from None


def _to_scraper_game(match: Match) -> ScraperGame:
    return ScraperGame(
        id=match.id,
        league=match.league,
        home_team=match.home_team,
        away_team=match.away_team,
        home_score=match.home_score,
        away_score=match.away_score,
        status=match.status,
        minute=match.minute,
        kickoff=match.kickoff.isoformat() if match.kickoff else None,
        agg_home_score=match.agg_home_score,
        agg_away_score=match.agg_away_score,
        home_penalties=match.home_penalties,
        away_penalties=match.away_penalties,
        qualifies=match.qualifies,
        home_scorers=match.home_scorers,
        away_scorers=match.away_scorers,
    )


async def get_matches(day: str) -> list[ScraperGame]:
    target_date = _resolve_date(day)
    matches = await asyncio.to_thread(get_matches_by_date, target_date)
    return [_to_scraper_game(match) for match in matches]


async def poll_live_futbol_matches() -> None:
    previous: list[ScraperGame] = []

    while True:
        try:
            current = await get_matches("today")

            if current != previous:
                payload = [game.model_dump(mode="json") for game in current]
                await manager.broadcast({"type": "live_update", "matches": payload})
                previous = current

        except Exception:
            logger.exception("live poll failed")

        await asyncio.sleep(POLL_INTERVAL)
