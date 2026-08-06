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

    model_config: ClassVar[ConfigDict] = ConfigDict(from_attributes=True)
