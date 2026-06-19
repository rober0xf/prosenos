from sqlalchemy.orm import Session

from app.domain.models.team import TeamModel
from app.domain.schemas.team import TeamCreate


class TeamRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_id(self, team_id: int) -> TeamModel | None:
        return self.db.get(TeamModel, team_id)

    def list(self, league: str | None = None) -> list[TeamModel]:
        query = self.db.query(TeamModel)
        if league:
            query = query.filter(TeamModel.league == league)
        return query.all()

    def create(self, data: TeamCreate) -> TeamModel:
        team = TeamModel(**data.model_dump(mode="json"))
        self.db.add(team)
        self.db.commit()
        self.db.refresh(team)
        return team
