from unittest.mock import patch


class TestFutbolRoutes:
    def test_get_matches_dash_format(self, client):
        async def fake(day: str):
            assert day == "09-07-2024"
            return [
                {
                    "id": "123",
                    "league": "Mundial",
                    "home_team": "Argentina",
                    "away_team": "Brazil",
                    "home_score": 2,
                    "away_score": 1,
                    "status": "finished",
                    "kickoff": "2024-07-09T21:00:00",
                    "minute": None,
                }
            ]

        with patch("app.infrastructure.api.routes.futbol.get_matches", side_effect=fake):
            response = client.get("/api/v1/matches/09-07-2024")
            assert response.status_code == 200
            data = response.json()
            assert len(data) == 1
            assert data[0]["home_team"] == "Argentina"

    def test_get_matches_slash_format(self, client):
        async def fake(day: str):
            assert day == "09-07-2024", f"expected normalized day, got {day}"
            return [
                {
                    "id": "123",
                    "league": "Mundial",
                    "home_team": "Argentina",
                    "away_team": "Brazil",
                    "home_score": 2,
                    "away_score": 1,
                    "status": "finished",
                    "kickoff": "2024-07-09T21:00:00",
                    "minute": None,
                }
            ]

        with patch("app.infrastructure.api.routes.futbol.get_matches", side_effect=fake):
            response = client.get("/api/v1/matches/09/07/2024")
            assert response.status_code == 200
            data = response.json()
            assert len(data) == 1
            assert data[0]["home_team"] == "Argentina"

    def test_get_matches_empty(self, client):
        async def fake(day: str):
            return []

        with patch("app.infrastructure.api.routes.futbol.get_matches", side_effect=fake):
            response = client.get("/api/v1/matches/10-07-2024")
            assert response.status_code == 200
            assert response.json() == []

    def test_get_matches_scraper_down(self, client):
        response = client.get("/api/v1/matches/11-07-2024")
        assert response.status_code == 503
        assert response.json()["detail"] == "Scraper service is unavailable"
