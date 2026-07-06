from datetime import datetime

from clients.futbol import get_matches_by_date
from fastapi import FastAPI, HTTPException, status

app = FastAPI(title="futbol microservice")


@app.get("/matches/{day:path}")
def get_matches(day: str):
    day = day.replace("/", "-").replace(".", "-")

    try:
        match_date = datetime.strptime(day, "%d-%m-%Y").date()  # noqa: DTZ007
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Use date format: DD-MM-YYYY (e.g. 06-07-2026 or 06/07/2026)",
        ) from None

    matches = get_matches_by_date(match_date)
    return [match.to_dict() for match in matches]


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8001, reload=True)
