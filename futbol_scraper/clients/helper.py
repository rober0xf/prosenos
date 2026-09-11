import os
from datetime import date

from constants import GOAL_LABELS
from dotenv import load_dotenv
from models.data import TeamData

_ = load_dotenv()

BASE_URL = os.getenv("BASE_URL")
if not BASE_URL:
    raise ValueError("BASE_URL environment variable not set")


def build_date_url(match_date: date):
    formatted = match_date.strftime("%d-%m-%Y")
    return f"{BASE_URL}/{formatted}"


# mappers
def to_int_pair(values: list[int] | None) -> tuple[int | None, int | None]:
    if not values:
        return None, None
    return int(values[0]), int(values[1])


def format_scorers(team: TeamData) -> list[str]:
    scorers: list[str] = []

    for goal in team.goals:
        goal_type = goal.goal_type
        label = GOAL_LABELS.get(goal_type) if goal_type else None
        prefix = f"({label}) " if label else ""
        scorers.append(f"{prefix}{goal.player_name.strip()}. {goal.time_to_display}")
    return scorers
