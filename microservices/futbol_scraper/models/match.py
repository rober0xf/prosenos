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
    minute: int
    kickoff: datetime | None

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "league": self.league,
            "home_team": self.home_team,
            "away_team": self.away_team,
            "home_score": self.home_score,
            "away_score": self.away_score,
            "status": self.status,
            "minute": self.minute,
            "kickoff": self.kickoff.strftime("%d/%m/%Y %H:%M") if self.kickoff else None,
        }
