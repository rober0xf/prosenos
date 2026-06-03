from pydantic import BaseModel

from core.domain.enums import Conference, League, Nationality


class TeamCreate(BaseModel):
    name: str
    league: League
    conference: Conference | None = None
    nationality: Nationality | None = None
    logo_url: str | None = None


class Team(BaseModel):
    id: int
    external_id: str  # external api team id
    name: str
    league: League
    conference: Conference | None = None
    nationality: Nationality | None = None
    logo_url: str | None = None


class TeamSeasonStats(BaseModel):
    team_id: int
    wins: int
    losses: int
    draws: int | None = None
    points: int | None = None
