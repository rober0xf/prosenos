from pydantic import BaseModel

from app.domain.enums import Conference, League, Nationality, Sport


class TeamCreate(BaseModel):
    name: str
    sport: Sport
    league: League
    conference: Conference | None = None
    nationality: Nationality | None = None
    logo_url: str | None = None


class TeamUpdate(BaseModel):
    name: str | None = None
    league: League | None = None
    conference: Conference | None = None
    nationality: Nationality | None = None
    logo_url: str | None = None


class Team(BaseModel):
    id: int
    external_id: str | None = None
    name: str
    sport: Sport
    league: League
    conference: Conference | None = None
    nationality: Nationality | None = None
    logo_url: str | None = None

    model_config = {"from_attributes": True}
