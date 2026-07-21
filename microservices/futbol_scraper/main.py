from datetime import datetime

from fastapi import FastAPI, HTTPException, status

from futbol_scraper.clients.futbol import get_matches_by_date, get_today_matches

app = FastAPI(title="futbol microservice")


@app.get("/matches/today")
def today_matches():
    matches = get_today_matches()
    return [match.to_dict() for match in matches]


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
