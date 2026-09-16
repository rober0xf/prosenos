from fastapi import APIRouter

from .futbol import router as futbol_router

# from .games import router as games_router
# from .health import router as health_router
# from .teams import router as teams_router
from .ws import router as ws_router

router = APIRouter()

router.include_router(futbol_router)
# router.include_router(games_router)
# router.include_router(teams_router)
# router.include_router(health_router)
router.include_router(ws_router)
