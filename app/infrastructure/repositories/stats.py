from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.domain.enums import Sport
from app.domain.models.stats import FootballSeasonStatsModel, NBASeasonStatsModel
from app.domain.models.team import TeamModel
from app.domain.schemas.stats import FootballStatsCreate, NBAStatsCreate

_STAT_MODEL_MAP: dict[str, type[FootballSeasonStatsModel | NBASeasonStatsModel]] = {
    Sport.FOOTBALL: FootballSeasonStatsModel,
    Sport.NBA: NBASeasonStatsModel,
}


class StatsRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_team_and_season(self, team_id: int, season: str) -> FootballSeasonStatsModel | NBASeasonStatsModel | None:
        team = self.db.get(TeamModel, team_id)
        if not team:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team not found")

        model_cls = _STAT_MODEL_MAP.get(team.sport)
        if not model_cls:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Unknown sport: {team.sport}")

        return self.db.query(model_cls).filter_by(team_id=team_id, season=season).first()

    def create(self, team: TeamModel, data: FootballStatsCreate | NBAStatsCreate) -> FootballSeasonStatsModel | NBASeasonStatsModel:
        model_cls = _STAT_MODEL_MAP.get(team.sport)
        if not model_cls:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Unknown sport: {team.sport}")

        stats = model_cls(team_id=team.id, **data.model_dump(mode="json"))
        self.db.add(stats)
        self.db.commit()
        self.db.refresh(stats)
        return stats
