from fastapi import HTTPException, status

from app.domain.schemas.team import Team, TeamCreate
from app.infrastructure.repositories.team import TeamRepository


class TeamService:
    def __init__(self, repo: TeamRepository) -> None:
        self.repo = repo

    def get_team(self, team_id: int) -> Team:
        team = self.repo.get_by_id(team_id)
        if not team:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team not found")
        return Team.model_validate(team)

    def list_teams(self, league: str | None = None) -> list[Team]:
        teams = self.repo.list(league=league)
        return [Team.model_validate(t) for t in teams]

    def create_team(self, data: TeamCreate) -> Team:
        team = self.repo.create(data)
        return Team.model_validate(team)
