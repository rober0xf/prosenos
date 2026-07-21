from collections.abc import Sequence
from datetime import date

from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.domain.models.game import GameModel


class GameRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_id(self, game_id: int) -> GameModel | None:
        return self.db.get(GameModel, game_id)

    def list_all(
        self,
        *,
        sport: str | None = None,
        league: str | None = None,
        team: str | None = None,
        date_from: date | None = None,
        date_to: date | None = None,
    ) -> Sequence[GameModel]:
        query = self.db.query(GameModel)

        if sport:
            query = query.filter(GameModel.sport == sport)
        if league:
            query = query.filter(GameModel.league == league)
        if team:
            query = query.filter(
                or_(
                    GameModel.home_team.ilike(f"%{team}%"),
                    GameModel.away_team.ilike(f"%{team}%"),
                )
            )
        if date_from:
            query = query.filter(GameModel.played_at >= date_from)
        if date_to:
            query = query.filter(GameModel.played_at <= date_to)

        return query.order_by(GameModel.played_at.desc()).all()

    def exists_by_external_ids(self, external_ids: set[str]) -> set[str]:
        rows = (
            self.db.query(GameModel.external_id)
            .filter(GameModel.external_id.in_(external_ids))
            .all()
        )
        return {row[0] for row in rows}

    def bulk_insert(self, games: list[GameModel]) -> None:
        self.db.add_all(games)
        self.db.commit()
