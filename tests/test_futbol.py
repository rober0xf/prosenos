from unittest.mock import AsyncMock, patch

import pytest


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


class TestConnectionManager:
    @pytest.mark.anyio
    async def test_broadcast_sends_to_active_connections(self):
        from app.infrastructure.services.connection_manager import ConnectionManager

        mgr = ConnectionManager()
        mock_ws = AsyncMock()
        await mgr.connect(mock_ws)
        message = {"type": "test", "data": "hello"}
        await mgr.broadcast(message)
        mock_ws.send_json.assert_awaited_once_with(message)

    @pytest.mark.anyio
    async def test_disconnect_removes_websocket(self):
        from app.infrastructure.services.connection_manager import ConnectionManager

        mgr = ConnectionManager()
        mock_ws = AsyncMock()
        await mgr.connect(mock_ws)
        assert len(mgr.active) == 1
        mgr.disconnect(mock_ws)
        assert len(mgr.active) == 0

    @pytest.mark.anyio
    async def test_broadcast_handles_stale_connections(self):
        from app.infrastructure.services.connection_manager import ConnectionManager

        mgr = ConnectionManager()
        mock_ws = AsyncMock()
        mock_ws.send_json = AsyncMock(side_effect=Exception("gone"))
        await mgr.connect(mock_ws)
        await mgr.broadcast({"test": True})
        assert len(mgr.active) == 0
