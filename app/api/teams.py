# router = APIRouter(prefix="/api/v1/teams", tags=["teams"])

# LeagueQuery = Annotated[str | None, Query(description="filter teams by league name")]


# @router.get("/", status_code=status.HTTP_200_OK)
# def list_teams(db: DBSession, league: LeagueQuery = None) -> list[Team]:
#     repo = TeamRepository(db)
#     service = TeamService(repo)
#     return service.list_teams(league=league)


# @router.get("/{team_id}", status_code=status.HTTP_200_OK)
# def get_team(team_id: int, db: DBSession) -> Team:
#     repo = TeamRepository(db)
#     service = TeamService(repo)
#     return service.get_team(team_id)


# @router.post("/", status_code=status.HTTP_201_CREATED)
# def create_team(data: TeamCreate, db: DBSession) -> Team:
#     repo = TeamRepository(db)
#     service = TeamService(repo)
#     return service.create_team(data)
