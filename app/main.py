from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.config import settings
from app.core.database import Base, engine
from app.infrastructure.api.routes.futbol import router as futbol_router
from app.infrastructure.api.routes.health import router as health_router
from app.infrastructure.api.routes.teams import router as teams_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)  # update later on
    yield


app = FastAPI(title=settings.APP_TITLE, lifespan=lifespan)

app.include_router(futbol_router)
app.include_router(teams_router)
app.include_router(health_router)


def main() -> None:
    import uvicorn  # noqa: PLC0415

    uvicorn.run(
        "app.main:app",
        host=getattr(settings, "HOST", "127.0.0.1"),
        port=getattr(settings, "PORT", 8000),
        reload=getattr(settings, "DEBUG", True),
    )


if __name__ == "__main__":
    main()
