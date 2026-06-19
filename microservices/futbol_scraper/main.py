from clients.futbol import get_today_matches, get_yesterday_matches

# today
today_matches = get_today_matches()

# yesterday
yesterday_matches = get_yesterday_matches()

matches = today_matches + yesterday_matches

print(f"matches: {len(matches)}")
for match in matches:
    print(match)
