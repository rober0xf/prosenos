import asyncio
from contextlib import asynccontextmanager, suppress

import uvicorn
from fastapi import FastAPI

from app.api.router import router as futbol_router
from app.core.config import settings
from app.services.futbol import poll_live_futbol_matches


@asynccontextmanager
async def lifespan(_app: FastAPI):
    poll_task = asyncio.create_task(poll_live_futbol_matches())
    yield

    _ = poll_task.cancel()
    with suppress(asyncio.CancelledError):
        await poll_task


app = FastAPI(title=settings.APP_TITLE, lifespan=lifespan)
app.include_router(futbol_router)


def main() -> None:
    uvicorn.run(
        "app.main:app",
        host=getattr(settings, "HOST", "127.0.0.1"),
        port=getattr(settings, "PORT", 8000),
        reload=getattr(settings, "DEBUG", True),
    )


if __name__ == "__main__":
    main()
