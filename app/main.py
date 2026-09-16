import uvicorn
from fastapi import FastAPI

from app.api.router import router as api_router
from app.core.config import settings

# @asynccontextmanager
# async def lifespan(_app: FastAPI):
#     # Base.metadata.create_all(bind=engine)
#     poll_task = asyncio.create_task(poll_live_futbol_matches())
#     yield

#     _ = poll_task.cancel()
#     with suppress(asyncio.CancelledError):
#         await poll_task


# app = FastAPI(title=settings.APP_TITLE, lifespan=lifespan)
app = FastAPI(title=settings.APP_TITLE)
app.include_router(api_router)


def main() -> None:
    uvicorn.run(
        "app.main:app",
        host=getattr(settings, "HOST", "127.0.0.1"),
        port=getattr(settings, "PORT", 8000),
        reload=getattr(settings, "DEBUG", True),
    )


if __name__ == "__main__":
    main()
