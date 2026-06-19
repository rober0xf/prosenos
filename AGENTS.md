# Agent Instructions

## General Rules

* Follow existing project structure.
* Prefer simple, maintainable solutions.
* Add type hints whenever possible.
* Use async code when appropriate.
* Do not introduce unnecessary abstractions.

## Architecture Rules

### Routes

Routes should only:

* Validate requests
* Call services
* Return responses

Do not place business logic in routes.

### Services

Services contain business logic.

Services may:

* Call providers
* Call repositories
* Transform data
* Apply business rules

### Repositories

Repositories handle database access only.

Do not place business logic inside repositories.

### Providers

Providers fetch external data.

Examples:

* Scrapers
* Future external APIs

Providers should be interchangeable.

## Database

* Use SQLAlchemy 2.x style.
* Access the database through repositories only.
* Avoid SQLite-specific behavior.

## Schemas

* Use Pydantic for request and response models.
* Do not return ORM models directly.

## Logging

Use the project's logger.

Do not use `print()`.

## Testing

When adding features:

* Add or update tests when practical.
* Mock external providers.
* Avoid real network calls.

## Configuration

* Read configuration from environment variables.
* Never hardcode secrets, tokens, or API keys.

## Before Finishing

Verify that:

* Business logic is in services.
* Database logic is in repositories.
* External integrations are in providers.
* Type hints are present.
* Tests still pass.
