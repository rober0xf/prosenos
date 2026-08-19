from datetime import UTC, datetime

from sqlalchemy import JSON, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class GameModel(Base):
    __tablename__: str = "games"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    external_id: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    sport: Mapped[str] = mapped_column(String, nullable=False)
    league: Mapped[str] = mapped_column(String, nullable=False)
    home_team: Mapped[str] = mapped_column(String, nullable=False)
    away_team: Mapped[str] = mapped_column(String, nullable=False)
    home_score: Mapped[int] = mapped_column(Integer, nullable=True)
    away_score: Mapped[int] = mapped_column(Integer, nullable=True)
    status: Mapped[str] = mapped_column(String, nullable=False)
    minute: Mapped[int] = mapped_column(Integer, nullable=True)
    played_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    agg_home_score: Mapped[int] = mapped_column(Integer, nullable=True)
    agg_away_score: Mapped[int] = mapped_column(Integer, nullable=True)
    home_penalties: Mapped[int] = mapped_column(Integer, nullable=True)
    away_penalties: Mapped[int] = mapped_column(Integer, nullable=True)
    qualifies: Mapped[int] = mapped_column(Integer, nullable=True)
    home_scorers: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)
    away_scorers: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(UTC), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
        nullable=False,
    )
