from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING

from fastapi import HTTPException, status

from app.domain.schemas.game import Game
from app.infrastructure.services.helpers import check_if_finished, map_match_to_game

if TYPE_CHECKING:
    from app.domain.models.game import GameModel
    from app.infrastructure.repositories.game import GameRepository


class GameService:
    def __init__(self, repo: GameRepository) -> None:
        self.repo = repo

    def persist_finished_matches(self, matches: list[dict], sport: str = "football") -> int:
        finished = [m for m in matches if check_if_finished(m)]
        if not finished:
            return 0

        external_ids = {f"{sport}::{m['id']}" for m in finished}
        existing = self.repo.exists_by_external_ids(external_ids)

        new_games: list[GameModel] = []
        for match in finished:
            ext_id = f"{sport}::{match['id']}"
            if ext_id in existing:
                continue

            new_games.append(map_match_to_game(match, int(ext_id), sport))

        if new_games:
            self.repo.bulk_insert(new_games)
        return len(new_games)

    def list_games(
        self,
        *,
        sport: str | None = None,
        league: str | None = None,
        team: str | None = None,
        date_from: date | None = None,
        date_to: date | None = None,
    ) -> list[Game]:
        models = self.repo.list_all(
            sport=sport,
            league=league,
            team=team,
            date_from=date_from,
            date_to=date_to,
        )
        return [Game.model_validate(m) for m in models]

    def get_game(self, game_id: int) -> Game:
        model = self.repo.get_by_id(game_id)
        if not model:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="game not found",
            )
        return Game.model_validate(model)
