# Prosenos Backend

Live sports match tracking API. Scrapes match data from provider sources, normalizes it, and exposes it through a FastAPI REST API.

## Project Structure

```text
app/
  api/            # HTTP routes
    futbol.py         # match routes (/api/v1/matches)
    ws.py             # WebSocket route
  core/           # config, providers
    config.py         # settings from environment variables
    futbol.py         # futbol provider (fetches external data)
  domain/         # models and schemas
    models/           # ORM models
    schemas/          # Pydantic schemas (incl. external data + Match)
  helpers.py      # provider helpers (URL building, formatting)
  mappers.py      # provider data -> Match mapping
  constants.py    # leagues and goal label definitions
  services/       # business logic
  repositories/   # database access only
  main.py         # FastAPI app entrypoint
```

## Routes

`app/api/futbol.py`:

- `GET /api/v1/matches/today`
- `GET /api/v1/matches/yesterday`
- `GET /api/v1/matches/{day}` — date in `DD-MM-YYYY` (or `DD/MM/YYYY`) format

WebSocket:

- `WS /ws/matches/live`

The app polls today's matches every 15 seconds and pushes a
`{"type": "live_update", "matches": [...]}` frame to all connected clients
whenever the payload changes.

## Running with Docker

```sh
docker compose up --build
```

The backend is served at `http://localhost:8000`.

## Running locally

```sh
uv sync
uv run fastapi run app/main.py
```
