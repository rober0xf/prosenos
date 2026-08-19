from datetime import datetime
from typing import cast
from zoneinfo import ZoneInfo

from constants import LEAGUES
from models.data import GameData, TeamData
from models.match import Match

MATCH_TIMEZONE = ZoneInfo("UTC")

GOAL_LABELS = {"E.C": "EC", "Pen": "P"}


def _to_int_pair(values: list[int] | None) -> tuple[int | None, int | None]:
    if not values:
        return None, None
    return int(values[0]), int(values[1])


def _format_scorers(team: TeamData) -> list[str]:
    scorers: list[str] = []
    for goal in team.get("goals", []):
        goal_type = goal.get("goal_type")
        label = GOAL_LABELS.get(goal_type) if goal_type else None
        prefix = f"({label}) " if label else ""
        scorers.append(f"{prefix}{goal['player_name'].strip()}. {goal.get('time_to_display')}")
    return scorers


def map_match(game: GameData, league_name: str) -> Match:
    home_team, away_team = game["teams"]
    league_name = league_name.replace("-", " ").title()
    scores = game.get("scores")
    agg_scores = game.get("agg_scores")
    penalties = game.get("penalties")

    home_score, away_score = _to_int_pair(scores)
    agg_home_score, agg_away_score = _to_int_pair(agg_scores)
    home_penalties, away_penalties = _to_int_pair(penalties)

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
        agg_home_score=agg_home_score,
        agg_away_score=agg_away_score,
        home_penalties=home_penalties,
        away_penalties=away_penalties,
        qualifies=game.get("to_qualify"),
        home_scorers=_format_scorers(home_team),
        away_scorers=_format_scorers(away_team),
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
