# router = APIRouter(prefix="/api/health", tags=["health"])


# def _health_check(db: DBSession):
#     try:
#         _ = db.execute(text("SELECT 1"))
#     except Exception as e:
#         raise HTTPException(
#             status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
#             detail="database unavailable",
#         ) from e

#     return {"status": "healthy"}


# @router.get("/")
# def health(db: DBSession):
#     return _health_check(db)
