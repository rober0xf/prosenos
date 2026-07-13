from contextlib import suppress
from datetime import datetime

from app.domain.models.game import GameModel


def check_if_finished(match: dict) -> bool:
    home_score = match.get("home_score")
    away_score = match.get("away_score")
    status = match.get("status")
    return status == "finished" and home_score is not None and away_score is not None


def map_match_to_game(match: dict, ext_id: int, sport: str) -> GameModel:
    played_at = None
    kickoff = match.get("kickoff")
    if kickoff:
        with suppress(ValueError, TypeError):
            played_at = datetime.fromisoformat(kickoff)

    return GameModel(
        external_id=ext_id,
        sport=sport,
        league=match.get("league", ""),
        home_team=match.get("home_team", ""),
        away_team=match.get("away_team", ""),
        home_score=match.get("home_score"),
        away_score=match.get("away_score"),
        status="finished",
        minute=match.get("minute"),
        played_at=played_at,
    )
