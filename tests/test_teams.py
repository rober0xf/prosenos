class TestTeamRoutes:
    def test_create_football_team(self, client):
        payload = {
            "name": "Flamengo",
            "sport": "football",
            "league": "Brasileirao",
            "nationality": "Brazil",
        }
        response = client.post("/api/v1/teams/", json=payload)
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Flamengo"
        assert data["sport"] == "football"
        assert data["league"] == "Brasileirao"
        assert "id" in data

    def test_create_nba_team(self, client):
        payload = {
            "name": "Lakers",
            "sport": "nba",
            "league": "NBA",
            "conference": "Western",
        }
        response = client.post("/api/v1/teams/", json=payload)
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Lakers"
        assert data["sport"] == "nba"
        assert data["conference"] == "Western"

    def test_list_teams(self, client):
        client.post("/api/v1/teams/", json={"name": "Palmeiras", "sport": "football", "league": "Brasileirao"})
        client.post("/api/v1/teams/", json={"name": "Bulls", "sport": "nba", "league": "NBA"})

        response = client.get("/api/v1/teams/")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2

    def test_list_teams_filter_by_league(self, client):
        client.post("/api/v1/teams/", json={"name": "Palmeiras", "sport": "football", "league": "Brasileirao"})
        client.post("/api/v1/teams/", json={"name": "Bulls", "sport": "nba", "league": "NBA"})

        response = client.get("/api/v1/teams/", params={"league": "Brasileirao"})
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["league"] == "Brasileirao"

    def test_get_team_not_found(self, client):
        response = client.get("/api/v1/teams/999")
        assert response.status_code == 404

    def test_get_team_by_id(self, client):
        create_resp = client.post("/api/v1/teams/", json={"name": "Santos", "sport": "football", "league": "Brasileirao"})
        team_id = create_resp.json()["id"]

        response = client.get(f"/api/v1/teams/{team_id}")
        assert response.status_code == 200
        assert response.json()["name"] == "Santos"


class TestTeamStatsRoutes:
    def _create_football_team(self, client):
        resp = client.post("/api/v1/teams/", json={"name": "Flamengo", "sport": "football", "league": "Brasileirao"})
        return resp.json()["id"]

    def _create_nba_team(self, client):
        resp = client.post("/api/v1/teams/", json={"name": "Lakers", "sport": "nba", "league": "NBA", "conference": "Western"})
        return resp.json()["id"]

    def test_create_football_stats(self, client):
        team_id = self._create_football_team(client)
        payload = {"season": "2024", "wins": 20, "losses": 5, "draws": 10, "goals_for": 60, "goals_against": 25, "points": 70}
        response = client.post(f"/api/v1/teams/{team_id}/stats", json=payload)
        assert response.status_code == 201
        data = response.json()
        assert data["wins"] == 20
        assert data["draws"] == 10
        assert data["goals_for"] == 60
        assert data["points"] == 70

    def test_create_nba_stats(self, client):
        team_id = self._create_nba_team(client)
        payload = {"season": "2024", "wins": 50, "losses": 32, "points_scored": 8500, "points_allowed": 7800}
        response = client.post(f"/api/v1/teams/{team_id}/stats", json=payload)
        assert response.status_code == 201
        data = response.json()
        assert data["wins"] == 50
        assert data["points_scored"] == 8500

    def test_get_football_stats(self, client):
        team_id = self._create_football_team(client)
        client.post(f"/api/v1/teams/{team_id}/stats", json={"season": "2024", "wins": 20, "losses": 5, "draws": 10, "goals_for": 60, "goals_against": 25, "points": 70})
        response = client.get(f"/api/v1/teams/{team_id}/stats", params={"season": "2024"})
        assert response.status_code == 200
        data = response.json()
        assert data["wins"] == 20
        assert data["goals_for"] == 60

    def test_get_nba_stats(self, client):
        team_id = self._create_nba_team(client)
        client.post(f"/api/v1/teams/{team_id}/stats", json={"season": "2024", "wins": 50, "losses": 32, "points_scored": 8500, "points_allowed": 7800})
        response = client.get(f"/api/v1/teams/{team_id}/stats", params={"season": "2024"})
        assert response.status_code == 200
        data = response.json()
        assert data["wins"] == 50
        assert data["points_scored"] == 8500

    def test_stats_not_found(self, client):
        team_id = self._create_football_team(client)
        response = client.get(f"/api/v1/teams/{team_id}/stats", params={"season": "9999"})
        assert response.status_code == 404
