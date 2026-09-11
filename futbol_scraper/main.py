from datetime import date

from clients.futbol import get_matches_by_date, get_today_matches, get_yesterday_matches
from fastapi import FastAPI, HTTPException, status
from models.match import Match
from response import MatchResponse

app = FastAPI(title="futbol microservice")


@app.get("/matches/yesteday", response_model=list[MatchResponse])
def yesterday_matches() -> list[Match]:
    return get_yesterday_matches()


@app.get("/matches/today", response_model=list[MatchResponse])
def today_matches() -> list[Match]:
    return get_today_matches()


@app.get("/matches/{day:path}", response_model=list[MatchResponse])
def get_matches(day: str) -> list[Match]:
    day = day.replace("/", "-").replace(".", "-")

    try:
        parsed_day, parsed_month, parsed_year = (int(part) for part in day.split("-"))
        match_date = date(parsed_year, parsed_month, parsed_day)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Use date format: DD-MM-YYYY (e.g. 06-07-2026 or 06/07/2026)",
        ) from None

    return get_matches_by_date(match_date)
