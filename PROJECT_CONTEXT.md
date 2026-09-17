# Project Context

## Overview

A FastAPI backend for tracking live Football matches.

The application collects data from a scraper provider, normalizes it, stores relevant information in SQLite, and exposes it through a REST API.

The football provider is integrated inside the app (`app/core/futbol.py`) and services fetch from it directly; a WebSocket route broadcasts live match updates. No separate microservice is required.

The architecture should remain flexible enough to support external sports APIs, additional sports, PostgreSQL, caching, and WebSockets in the future.

## Tech Stack

- Python 3.13+
- FastAPI
- Pydantic v2
- SQLAlchemy 2.x
- SQLite

## Core Features

- Live match tracking
- Match schedules
- Match details and scores
- Team and league information
- Background synchronization jobs

## Architecture

```text
Routes
  ↓
Services
  ↓
Repositories
  ↓
Database

Providers
  ↓
Services
```

### Responsibilities

- Routes: HTTP handling only
- Services: business logic
- Repositories: database access
- Providers: scraper/API integrations (`app/core/futbol.py`)

## Data Sources

Current:

- promiedos API (fetched by `app/core/futbol.py` via `curl_cffi`)

Future:

- External sports APIs

Services should never depend on a specific provider implementation.

## Long-Term Goals

- External API integrations
- Historical match data
- WebSocket updates
- PostgreSQL support
- Redis caching
