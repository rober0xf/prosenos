from typing import TypedDict


class GoalData(TypedDict):
    player_name: str
    time_to_display: str
    goal_type: str | None


class TeamData(TypedDict):
    name: str
    goals: list[GoalData]


class StatusData(TypedDict):
    name: str


class GameData(TypedDict):
    id: str
    teams: tuple[TeamData, TeamData]
    scores: list[int] | None
    agg_scores: list[int] | None
    penalties: list[int] | None
    to_qualify: int | None
    game_time: int | None
    start_time: str | None
    status: StatusData
