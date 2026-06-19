from typing import Annotated

from fastapi import APIRouter, Query, status

from app.domain.schemas.stats import FootballStats, FootballStatsCreate, NBAStats, NBAStatsCreate
from app.domain.schemas.team import Team, TeamCreate
from app.infrastructure.api.routes.deps import DBSession
from app.infrastructure.repositories.team import TeamRepository
from app.infrastructure.services.stats import StatsService
from app.infrastructure.services.team import TeamService

router = APIRouter(prefix="/api/v1/teams", tags=["teams"])

LeagueQuery = Annotated[str | None, Query(description="filter teams by league name")]


@router.get("/", response_model=list[Team])
def list_teams(
    db: DBSession,
    league: LeagueQuery = None,
):
    repo = TeamRepository(db)
    service = TeamService(repo)
    return service.list_teams(league=league)


@router.get("/{team_id}", response_model=Team)
def get_team(
    team_id: int,
    db: DBSession,
):
    repo = TeamRepository(db)
    service = TeamService(repo)
    return service.get_team(team_id)


@router.post("/", response_model=Team, status_code=status.HTTP_201_CREATED)
def create_team(
    data: TeamCreate,
    db: DBSession,
):
    repo = TeamRepository(db)
    service = TeamService(repo)
    return service.create_team(data)


@router.get("/{team_id}/stats", response_model=FootballStats | NBAStats)
def get_team_stats(
    team_id: int,
    season: str,
    db: DBSession,
):
    service = StatsService(db)
    return service.get_stats(team_id, season)


@router.post("/{team_id}/stats", response_model=FootballStats | NBAStats, status_code=status.HTTP_201_CREATED)
def create_team_stats(
    team_id: int,
    data: FootballStatsCreate | NBAStatsCreate,
    db: DBSession,
):
    service = StatsService(db)
    return service.create_stats(team_id, data)
