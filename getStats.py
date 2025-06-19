from leagueManager import LeagueManager
import json
from collections import OrderedDict

# Stats that need to be averaged
AVERAGE_STATS = {"WHIP", "ERA", "OBP"}

manager = LeagueManager(league_id=121531, year=2025)
league = manager.get_league()

max_period = league.currentMatchupPeriod
team_stats = {}
matchup_counts = {}

for period in range(1, max_period + 1):
    box_scores = league.box_scores(matchup_period=period)

    for box in box_scores:
        for team_obj, stats in [(box.home_team, box.home_stats), (box.away_team, box.away_stats)]:
            if not team_obj or not stats:
                continue

            team_name = team_obj.team_name

            if team_name not in team_stats:
                team_stats[team_name] = {}
                matchup_counts[team_name] = 0

            matchup_counts[team_name] += 1

            for stat, data in stats.items():
                value = data['value']
                if value is None:
                    continue

                if stat not in team_stats[team_name]:
                    team_stats[team_name][stat] = 0

                team_stats[team_name][stat] += value

# Normalize selected stats
STAT_ORDER = ['R', 'HR', 'RBI', 'OBP', 'SB', 'K', 'W', 'SV', 'ERA', 'WHIP']
for team, stats in team_stats.items():
    count = matchup_counts[team]
    for stat in AVERAGE_STATS:
        if stat in stats:
            stats[stat] = round(stats[stat] / count, 3)

# Ordered Output
ordered_stats = {}

for team in sorted(team_stats):  # Optional: sort teams alphabetically
    ordered_stats[team] = OrderedDict()
    for stat in STAT_ORDER:
        ordered_stats[team][stat] = team_stats[team].get(stat, 0)

# Print nicely formatted JSON
with open("team_stats.json", "w") as f:
    json.dump(team_stats, f, indent=4)
print(json.dumps(ordered_stats, indent=4))
