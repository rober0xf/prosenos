from datetime import datetime

from fastapi import FastAPI, HTTPException, status

from clients.futbol import get_matches_by_date, get_today_matches
from models.match import Match

from .response import MatchResponse

app = FastAPI(title="futbol microservice")


@app.get("/matches/today", response_model=list[MatchResponse])
def today_matches() -> list[Match]:
    return get_today_matches()


@app.get("/matches/{day:path}", response_model=list[MatchResponse])
def get_matches(day: str) -> list[Match]:
    day = day.replace("/", "-").replace(".", "-")

    try:
        match_date = datetime.strptime(day, "%d-%m-%Y").date()  # noqa: DTZ007
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Use date format: DD-MM-YYYY (e.g. 06-07-2026 or 06/07/2026)",
        ) from None

    return get_matches_by_date(match_date)
