from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class TeamModel(Base):
    __tablename__: str = "teams"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    external_id: Mapped[str] = mapped_column(String, unique=True, nullable=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    sport: Mapped[str] = mapped_column(String, nullable=False)
    league: Mapped[str] = mapped_column(String, nullable=False)
    conference: Mapped[str] = mapped_column(String, nullable=True)
    nationality: Mapped[str] = mapped_column(String, nullable=True)
    logo_url: Mapped[str] = mapped_column(String, nullable=True)
