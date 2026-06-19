from dataclasses import dataclass
from datetime import datetime


@dataclass
class Match:
    id: str
    league: str

    home_team: str
    away_team: str

    home_score: int | None
    away_score: int | None

    status: str
    kickoff: datetime | None
    minute: int | None
