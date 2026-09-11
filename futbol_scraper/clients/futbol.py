from datetime import UTC, date, datetime, timedelta

from clients.helper import build_date_url
from clients.match_mapper import map_matches
from curl_cffi import requests as cffi_requests
from models.data import ExternalMatchesResponse
from models.match import Match
from pydantic import TypeAdapter

_matches_response_adapter = TypeAdapter(ExternalMatchesResponse)


def fetch_matches(url: str) -> ExternalMatchesResponse:
    session = cffi_requests.Session(impersonate="firefox133")
    response = session.get(url, headers={"X-VER": "1.11.7.5"}, timeout=30)
    response.raise_for_status()

    return _matches_response_adapter.validate_python(response.json())  # pyright: ignore[reportUnknownMemberType]


def get_matches_by_date(target_date: date) -> list[Match]:
    url = build_date_url(target_date)
    data = fetch_matches(url)
    return map_matches(data)


def get_today_matches() -> list[Match]:
    today = datetime.now(UTC).date()
    return get_matches_by_date(today)


def get_yesterday_matches() -> list[Match]:
    yesterday = datetime.now(UTC).date() - timedelta(days=1)
    return get_matches_by_date(yesterday)


def get_tomorrow_matches() -> list[Match]:
    tomorrow = datetime.now(UTC).date() + timedelta(days=1)
    return get_matches_by_date(tomorrow)
