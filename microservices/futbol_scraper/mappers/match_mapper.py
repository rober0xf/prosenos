from constants import LEAGUES
from models.match import Match


def map_match(game, league_name):
    home_team, away_team = game["teams"]
    scores = game.get("scores")

    home_score = int(scores[0]) if scores else None
    away_score = int(scores[1]) if scores else None

    return Match(
        id=game["id"],
        league=league_name,
        home_team=home_team["name"],
        away_team=away_team["name"],
        home_score=home_score,
        away_score=away_score,
        status=game["status"]["name"],
        minute=None,
    )


def map_matches(data):
    matches = []

    leagues = data.get("leagues") if isinstance(data, dict) else None
    if leagues is None:
        return matches

    for league in data["leagues"]:
        league_name = league["name"]

        if league_name not in LEAGUES:
            continue

        for game in league["games"]:
            matches.append(map_match(game, league_name))

    return matches
