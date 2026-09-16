from __future__ import annotations

# router = APIRouter(prefix="/api/v1/games", tags=["games"])


# class GameFilterParams(BaseModel):
#     sport: str | None = None
#     league: str | None = None
#     team: str | None = None
#     date_from: date | None = Field(None, description="start date (YYYY-MM-DD)")
#     date_to: date | None = Field(None, description="end date (YYYY-MM-DD)")


# @router.get("/", response_model=list[Game])
# def list_games(
#     db: DBSession, filters: Annotated[GameFilterParams, Depends()]
# ) -> list[Game]:
#     repo = GameRepository(db)
#     service = GameService(repo)

#     return service.list_games(
#         sport=filters.sport,
#         league=filters.league,
#         team=filters.team,
#         date_from=filters.date_from,
#         date_to=filters.date_to,
#     )


# @router.get("/{game_id}", response_model=Game)
# def get_game(db: DBSession, game_id: int) -> Game:
#     repo = GameRepository(db)
#     service = GameService(repo)
