from datetime import datetime

from clients.helper import format_scorers, to_int_pair
from constants import LEAGUES, MATCH_TIMEZONE
from models.data import ExternalMatchesResponse, GameData
from models.match import Match


def map_match(game: GameData, league_name: str) -> Match:
    home_team, away_team = game.teams
    league_name = league_name.replace("-", " ").title()

    home_score, away_score = to_int_pair(game.scores)
    agg_home_score, agg_away_score = to_int_pair(game.agg_scores)
    home_penalties, away_penalties = to_int_pair(game.penalties)

    game_time = game.game_time or -1
    start_time_str = game.start_time
    kickoff_dt = datetime.strptime(start_time_str, "%d-%m-%Y %H:%M").replace(tzinfo=MATCH_TIMEZONE) if start_time_str else None

    return Match(
        id=game.id,
        league=league_name,
        home_team=home_team.name,
        away_team=away_team.name,
        home_score=home_score,
        away_score=away_score,
        status=game.status.name,
        minute=game_time,
        kickoff=kickoff_dt,
        agg_home_score=agg_home_score,
        agg_away_score=agg_away_score,
        home_penalties=home_penalties,
        away_penalties=away_penalties,
        qualifies=game.to_qualify,
        home_scorers=format_scorers(home_team),
        away_scorers=format_scorers(away_team),
    )


def map_matches(data: ExternalMatchesResponse) -> list[Match]:
    matches: list[Match] = []

    for league in data.leagues:
        league_name = league.url_name

        if league_name not in LEAGUES:
            continue

        for game in league.games:
            matches.append(map_match(game, league_name))

    return matches
