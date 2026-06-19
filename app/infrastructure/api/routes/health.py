from fastapi import HTTPException, status
from sqlalchemy import text

from app.infrastructure.api.routes.deps import DBSession


def health_check(db: DBSession):
    try:
        db.execute(text("SELECT 1"))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="database unavailable",
        ) from e

    return {"status": "healthy"}
