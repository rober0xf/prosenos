from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.domain.enums import Sport
from app.domain.models.team import TeamModel
from app.domain.schemas.stats import (
    FootballStats,
    FootballStatsCreate,
    NBAStats,
    NBAStatsCreate,
)
from app.infrastructure.repositories.stats import StatsRepository


class StatsService:
    def __init__(self, db: Session) -> None:
        self.repo = StatsRepository(db)
        self.db = db

    def get_stats(self, team_id: int, season: str) -> FootballStats | NBAStats:
        stats = self.repo.get_by_team_and_season(team_id, season)
        if not stats:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Stats not found for this season")

        team = self.db.get(TeamModel, team_id)
        if team.sport == Sport.FOOTBALL:
            return FootballStats.model_validate(stats)
        return NBAStats.model_validate(stats)

    def create_stats(
        self, team_id: int, data: FootballStatsCreate | NBAStatsCreate
    ) -> FootballStats | NBAStats:
        team = self.db.get(TeamModel, team_id)
        if not team:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team not found")

        if isinstance(data, FootballStatsCreate) and team.sport != Sport.FOOTBALL:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Team is not a football team")
        if isinstance(data, NBAStatsCreate) and team.sport != Sport.NBA:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Team is not an NBA team")

        stats = self.repo.create(team, data)
        if team.sport == Sport.FOOTBALL:
            return FootballStats.model_validate(stats)
        return NBAStats.model_validate(stats)
