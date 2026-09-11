from pydantic import BaseModel


class GoalData(BaseModel):
    player_name: str
    time_to_display: str
    goal_type: str | None = None


class TeamData(BaseModel):
    name: str
    goals: list[GoalData] = []


class StatusData(BaseModel):
    name: str


class GameData(BaseModel):
    id: str
    teams: tuple[TeamData, TeamData]
    scores: list[int] | None = None
    agg_scores: list[int] | None = None
    penalties: list[int] | None = None
    to_qualify: int | None = None
    game_time: int | None = None
    start_time: str | None = None
    status: StatusData


class LeagueData(BaseModel):
    url_name: str
    games: list[GameData]


class ExternalMatchesResponse(BaseModel):
    leagues: list[LeagueData]
