from dataclasses import dataclass, field
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
    minute: int
    kickoff: datetime | None
    agg_home_score: int | None = None
    agg_away_score: int | None = None
    home_penalties: int | None = None
    away_penalties: int | None = None
    qualifies: int | None = None
    home_scorers: list[str] = field(default_factory=list)
    away_scorers: list[str] = field(default_factory=list)
