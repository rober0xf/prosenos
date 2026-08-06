from datetime import datetime
from typing import cast
from zoneinfo import ZoneInfo

from constants import LEAGUES
from models.data import GameData
from models.match import Match

MATCH_TIMEZONE = ZoneInfo("UTC")


def map_match(game: GameData, league_name: str) -> Match:
    home_team, away_team = game["teams"]
    league_name = league_name.replace("-", " ").title()
    scores = game.get("scores")

    home_score = int(scores[0]) if scores else None
    away_score = int(scores[1]) if scores else None

    game_time = game.get("game_time") or -1
    start_time_str = game.get("start_time")
    kickoff_dt = datetime.strptime(start_time_str, "%d-%m-%Y %H:%M").replace(tzinfo=MATCH_TIMEZONE) if start_time_str else None

    return Match(
        id=game["id"],
        league=league_name,
        home_team=home_team["name"],
        away_team=away_team["name"],
        home_score=home_score,
        away_score=away_score,
        status=game["status"]["name"],
        minute=game_time,
        kickoff=kickoff_dt,
    )


def map_matches(data: dict[str, object]) -> list[Match]:
    matches: list[Match] = []

    leagues = cast("list[dict[str, object]]", data["leagues"])

    for league in leagues:
        league_name = cast("str", league["url_name"])

        if league_name not in LEAGUES:
            continue

        for game in cast("list[GameData]", league["games"]):
            matches.append(map_match(game, league_name))

    return matches
