from datetime import UTC, datetime
from unittest.mock import create_autospec

import pytest

from app.domain.models.game import GameModel
from app.domain.schemas.game import ScraperGame
from app.infrastructure.repositories.game import GameRepository
from app.infrastructure.services.game import GameService


def _make_match(
    *,
    match_id: str = "1",
    status: str = "finished",
    home_score: int | None = 2,
    away_score: int | None = 1,
) -> ScraperGame:
    return ScraperGame(
        id=match_id,
        league="Mundial",
        home_team="Argentina",
        away_team="Brazil",
        home_score=home_score,
        away_score=away_score,
        status=status,
        minute=None,
        kickoff="2024-07-09T21:00:00",
    )


class TestGameService:
    def test_persist_only_finished_matches(self):
        repo = create_autospec(GameRepository, instance=True)
        repo.exists_by_external_ids.return_value = set()
        svc = GameService(repo)

        matches = [
            _make_match(match_id="1", status="finished"),
            _make_match(match_id="2", status="live"),
            _make_match(match_id="3", status="finished"),
        ]
        count = svc.persist_finished_matches(matches)

        assert count == 2
        args, _ = repo.bulk_insert.call_args
        inserted: list = args[0]
        ext_ids = {g.external_id for g in inserted}
        assert ext_ids == {"football::1", "football::3"}

    def test_persist_skips_existing(self):
        repo = create_autospec(GameRepository, instance=True)
        repo.exists_by_external_ids.return_value = {"football::1"}
        svc = GameService(repo)

        matches = [
            _make_match(match_id="1", status="finished"),
            _make_match(match_id="2", status="finished"),
        ]
        count = svc.persist_finished_matches(matches)

        assert count == 1
        args, _ = repo.bulk_insert.call_args
        inserted: list = args[0]
        assert len(inserted) == 1
        assert inserted[0].external_id == "football::2"

    def test_persist_skips_matches_without_scores(self):
        repo = create_autospec(GameRepository, instance=True)
        repo.exists_by_external_ids.return_value = set()
        svc = GameService(repo)

        matches = [
            _make_match(match_id="1", home_score=None, away_score=None),
            _make_match(match_id="2", home_score=3, away_score=0),
        ]
        count = svc.persist_finished_matches(matches)

        assert count == 1
        assert repo.bulk_insert.call_count == 1

    def test_persist_supports_different_sport(self):
        repo = create_autospec(GameRepository, instance=True)
        repo.exists_by_external_ids.return_value = set()
        svc = GameService(repo)

        matches = [_make_match(match_id="42")]
        count = svc.persist_finished_matches(matches, sport="nba")

        assert count == 1
        args, _ = repo.bulk_insert.call_args
        assert args[0][0].external_id == "nba::42"

    def test_list_games_delegates_to_repo(self):
        repo = create_autospec(GameRepository, instance=True)
        repo.list_all.return_value = [
            GameModel(
                id=1,
                external_id="football::1",
                sport="football",
                league="Mundial",
                home_team="A",
                away_team="B",
                home_score=2,
                away_score=1,
                status="finished",
                minute=None,
                played_at=datetime(2024, 7, 9, 21, 0, 0, tzinfo=UTC),
            )
        ]
        svc = GameService(repo)

        result = svc.list_games(sport="football")
        assert len(result) == 1
        assert result[0].home_team == "A"
        repo.list_all.assert_called_once_with(
            sport="football",
            league=None,
            team=None,
            date_from=None,
            date_to=None,
        )


class TestGameRoutes:
    def test_list_games_empty(self, client):
        response = client.get("/api/v1/games/")
        assert response.status_code == 200
        assert response.json() == []

    def test_list_games_with_data(self, client, db_session):
        game = GameModel(
            external_id="football::1",
            sport="football",
            league="Mundial",
            home_team="Argentina",
            away_team="Brazil",
            home_score=2,
            away_score=1,
            status="finished",
            played_at=datetime(2024, 7, 9, 21, 0, 0, tzinfo=UTC),
        )
        db_session.add(game)
        db_session.commit()

        response = client.get("/api/v1/games/")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["home_team"] == "Argentina"

    def test_list_games_filter_by_team(self, client, db_session):
        db_session.add_all([
            GameModel(external_id="f1", sport="football", league="Mundial", home_team="Argentina", away_team="Brazil", home_score=2, away_score=1, status="finished", played_at=datetime(2024, 7, 9, 21, 0, 0, tzinfo=UTC)),
            GameModel(external_id="f2", sport="football", league="Mundial", home_team="Uruguay", away_team="Chile", home_score=0, away_score=0, status="finished", played_at=datetime(2024, 7, 10, 21, 0, 0, tzinfo=UTC)),
        ])
        db_session.commit()

        response = client.get("/api/v1/games/", params={"team": "argentina"})
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["home_team"] == "Argentina"

    def test_list_games_filter_by_sport(self, client, db_session):
        db_session.add_all([
            GameModel(external_id="f1", sport="football", league="Mundial", home_team="A", away_team="B", home_score=1, away_score=0, status="finished", played_at=datetime(2024, 7, 9, 21, 0, 0, tzinfo=UTC)),
            GameModel(external_id="n1", sport="nba", league="NBA", home_team="Lakers", away_team="Celtics", home_score=110, away_score=105, status="finished", played_at=datetime(2024, 7, 9, 21, 0, 0, tzinfo=UTC)),
        ])
        db_session.commit()

        response = client.get("/api/v1/games/", params={"sport": "nba"})
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["external_id"] == "n1"

    def test_get_game_found(self, client, db_session):
        game = GameModel(
            external_id="football::42",
            sport="football",
            league="Mundial",
            home_team="Argentina",
            away_team="Brazil",
            home_score=2,
            away_score=1,
            status="finished",
            played_at=datetime(2024, 7, 9, 21, 0, 0, tzinfo=UTC),
        )
        db_session.add(game)
        db_session.commit()

        response = client.get(f"/api/v1/games/{game.id}")
        assert response.status_code == 200
        assert response.json()["home_team"] == "Argentina"

    def test_get_game_not_found(self, client):
        response = client.get("/api/v1/games/999")
        assert response.status_code == 404

    def test_list_games_filter_by_date_range(self, client, db_session):
        db_session.add_all([
            GameModel(external_id="f1", sport="football", league="Mundial", home_team="A", away_team="B", home_score=1, away_score=0, status="finished", played_at=datetime(2024, 7, 9, 21, 0, 0, tzinfo=UTC)),
            GameModel(external_id="f2", sport="football", league="Mundial", home_team="C", away_team="D", home_score=2, away_score=2, status="finished", played_at=datetime(2024, 7, 15, 21, 0, 0, tzinfo=UTC)),
        ])
        db_session.commit()

        response = client.get("/api/v1/games/", params={"date_from": "2024-07-10", "date_to": "2024-07-20"})
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["external_id"] == "f2"
