from contextlib import suppress
from datetime import datetime

from app.domain.models.game import GameModel
from app.domain.schemas.game import ScraperGame


def check_if_finished(match: ScraperGame) -> bool:
    return match.status == "finished" and match.home_score is not None and match.away_score is not None


def map_match_to_game(match: ScraperGame, ext_id: str, sport: str) -> GameModel:
    played_at = None
    if match.kickoff:
        with suppress(ValueError, TypeError):
            played_at = datetime.fromisoformat(match.kickoff)

    return GameModel(
        external_id=ext_id,
        sport=sport,
        league=match.league,
        home_team=match.home_team,
        away_team=match.away_team,
        home_score=match.home_score,
        away_score=match.away_score,
        status=match.status,
        minute=match.minute,
        played_at=played_at,
    )
