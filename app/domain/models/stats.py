from sqlalchemy import Column, ForeignKey, Integer, String

from app.core.database import Base


class FootballSeasonStatsModel(Base):
    __tablename__ = "football_season_stats"

    id = Column(Integer, primary_key=True)
    team_id = Column(Integer, ForeignKey("teams.id"), nullable=False)
    season = Column(String, nullable=False)
    wins = Column(Integer, default=0)
    losses = Column(Integer, default=0)
    draws = Column(Integer, default=0)
    goals_for = Column(Integer, default=0)
    goals_against = Column(Integer, default=0)
    points = Column(Integer, default=0)


class NBASeasonStatsModel(Base):
    __tablename__ = "nba_season_stats"

    id = Column(Integer, primary_key=True)
    team_id = Column(Integer, ForeignKey("teams.id"), nullable=False)
    season = Column(String, nullable=False)
    wins = Column(Integer, default=0)
    losses = Column(Integer, default=0)
    points_scored = Column(Integer, default=0)
    points_allowed = Column(Integer, default=0)
