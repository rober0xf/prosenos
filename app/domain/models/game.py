from datetime import UTC, datetime

from sqlalchemy import Column, DateTime, Integer, String

from app.core.database import Base


class GameModel(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True)
    external_id = Column(String, unique=True, nullable=False)
    sport = Column(String, nullable=False)
    league = Column(String, nullable=False)
    home_team = Column(String, nullable=False)
    away_team = Column(String, nullable=False)
    home_score = Column(Integer, nullable=True)
    away_score = Column(Integer, nullable=True)
    status = Column(String, nullable=False)
    minute = Column(Integer, nullable=True)
    played_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(UTC), nullable=False)
    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
        nullable=False,
    )
