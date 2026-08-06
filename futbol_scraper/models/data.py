from typing import TypedDict


class TeamData(TypedDict):
    name: str


class StatusData(TypedDict):
    name: str


class GameData(TypedDict):
    id: str
    teams: tuple[TeamData, TeamData]
    scores: list[int] | None
    game_time: int | None
    start_time: str | None
    status: StatusData
