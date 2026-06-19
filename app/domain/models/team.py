from sqlalchemy import Column, Integer, String

from app.core.database import Base


class TeamModel(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True)
    external_id = Column(String, unique=True, nullable=True)
    name = Column(String, nullable=False)
    sport = Column(String, nullable=False)
    league = Column(String, nullable=False)
    conference = Column(String, nullable=True)
    nationality = Column(String, nullable=True)
    logo_url = Column(String, nullable=True)
