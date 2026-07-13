from datetime import datetime

from pydantic import BaseModel


class Game(BaseModel):
    id: int
    external_id: str
    sport: str
    league: str
    home_team: str
    away_team: str
    home_score: int | None
    away_score: int | None
    status: str
    minute: int | None
    played_at: datetime | None

    model_config = {"from_attributes": True}
