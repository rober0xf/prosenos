from datetime import datetime
from typing import ClassVar

from pydantic import BaseModel, ConfigDict


class MatchResponse(BaseModel):
    id: str
    league: str
    home_team: str
    away_team: str
    home_score: int | None
    away_score: int | None
    status: str
    minute: int
    kickoff: datetime | None
    agg_home_score: int | None = None
    agg_away_score: int | None = None
    home_penalties: int | None = None
    away_penalties: int | None = None
    qualifies: int | None = None
    home_scorers: list[str] = []
    away_scorers: list[str] = []

    model_config: ClassVar[ConfigDict] = ConfigDict(from_attributes=True)
