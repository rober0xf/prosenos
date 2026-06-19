from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.config import settings
from app.core.database import Base, engine
from app.infrastructure.api.routes.health import health_check
from app.infrastructure.api.routes.teams import router as teams_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title=settings.APP_TITLE, lifespan=lifespan)
app.include_router(teams_router)
app.add_api_route("/health", health_check, tags=["health"])


def main() -> None:
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    main()
