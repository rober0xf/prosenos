# Project Context

## Overview

A FastAPI backend for tracking live Football and NBA matches.

The application collects data from scraper-based providers, normalizes it, stores relevant information in SQLite, and exposes it through a REST API.

The architecture should remain flexible enough to support external sports APIs, additional sports, PostgreSQL, caching, and WebSockets in the future.

## Tech Stack

* Python 3.13+
* FastAPI
* Pydantic v2
* SQLAlchemy 2.x
* SQLite
* Pytest

## Core Features

* Live match tracking
* Match schedules
* Match details and scores
* Team and league information
* Background synchronization jobs

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

* Routes: HTTP handling only
* Services: business logic
* Repositories: database access
* Providers: scraper/API integrations

## Data Sources

Current:

* Scrapers

Future:

* External sports APIs

Services should never depend on a specific provider implementation.

## Long-Term Goals

* External API integrations
* Historical match data
* WebSocket updates
* PostgreSQL support
* Redis caching
