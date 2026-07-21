import os
from datetime import UTC, date, datetime, timedelta

from curl_cffi import requests as cffi_requests
from dotenv import load_dotenv

from futbol_scraper.mappers.match_mapper import map_matches

load_dotenv()

BASE_URL = os.getenv("BASE_URL")
if not BASE_URL:
    raise ValueError("BASE_URL environment variable not set")


def fetch_matches(url: str):
    session = cffi_requests.Session(
        impersonate="firefox133",
    )

    response = session.get(
        url,
        headers={"X-VER": "1.11.7.5"},
        timeout=30,
    )

    response.raise_for_status()
    return response.json()


def build_date_url(match_date: date):
    formatted = match_date.strftime("%d-%m-%Y")
    return f"{BASE_URL}/{formatted}"


def get_matches_by_date(target_date: date):
    url = build_date_url(target_date)
    data = fetch_matches(url)
    return map_matches(data)


def get_today_matches():
    today = datetime.now(UTC).date()
    return get_matches_by_date(today)


def get_yesterday_matches():
    yesterday = datetime.now(UTC).date() - timedelta(days=1)
    return get_matches_by_date(yesterday)


def get_tomorrow_matches():
    tomorrow = datetime.now(UTC).date() + timedelta(days=1)
    return get_matches_by_date(tomorrow)
