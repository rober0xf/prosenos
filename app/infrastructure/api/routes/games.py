from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from app.domain.schemas.game import Game
from app.infrastructure.api.routes.deps import DBSession
from app.infrastructure.repositories.game import GameRepository
from app.infrastructure.services.game import GameService

router = APIRouter(prefix="/api/v1/games", tags=["games"])


class GameFilterParams(BaseModel):
    sport: str | None = Field(None)
    league: str | None = Field(None)
    team: str | None = Field(None)
    date_from: date | None = Field(None, description="start date (YYYY-MM-DD)")
    date_to: date | None = Field(None, description="end date (YYYY-MM-DD)")


@router.get("/", response_model=list[Game])
def list_games(db: DBSession, filters: Annotated[GameFilterParams, Depends()]):
    repo = GameRepository(db)
    service = GameService(repo)

    return service.list_games(**filters.model_dump())


@router.get("/{game_id}", response_model=Game)
def get_game(db: DBSession, game_id: int):
    repo = GameRepository(db)
    service = GameService(repo)

    return service.get_game(game_id)
