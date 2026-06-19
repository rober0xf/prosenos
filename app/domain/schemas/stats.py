from pydantic import BaseModel


class FootballStatsCreate(BaseModel):
    season: str
    wins: int = 0
    losses: int = 0
    draws: int = 0
    goals_for: int = 0
    goals_against: int = 0
    points: int = 0


class FootballStats(BaseModel):
    id: int
    team_id: int
    season: str
    wins: int
    losses: int
    draws: int
    goals_for: int
    goals_against: int
    points: int

    model_config = {"from_attributes": True}


class NBAStatsCreate(BaseModel):
    season: str
    wins: int = 0
    losses: int = 0
    points_scored: int = 0
    points_allowed: int = 0


class NBAStats(BaseModel):
    id: int
    team_id: int
    season: str
    wins: int
    losses: int
    points_scored: int
    points_allowed: int

    model_config = {"from_attributes": True}
