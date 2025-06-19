import os
import json
from leagueManager import LeagueManager
from teams import Team

# Load saved team_id: team_name mapping
with open("teams.json", "r") as f:
    team_dict = json.load(f)

# Function to get team_index by team_id
def get_team_index_by_id(league, team_id):
    for i, team in enumerate(league.teams):
        if team.team_id == team_id:
            return i
    raise ValueError(f"Team ID '{team_id}' not found in league.")

# Create a folder to store rosters
output_dir = "rosters"
os.makedirs(output_dir, exist_ok=True)

# Connect to league
manager = LeagueManager(league_id=121531, year=2025)
league = manager.get_league()

# Loop through each team
for team_id_str, team_name in team_dict.items():
    team_id = int(team_id_str)
    try:
        team_index = get_team_index_by_id(league, team_id)
        team = Team(league, team_index)

        # Build roster data
        roster_list = team.get_roster()

        # Clean filename
        safe_name = team_name.replace(" ", "_").replace("/", "_")
        file_path = os.path.join(output_dir, f"{safe_name}.json")

        # Save to JSON
        with open(file_path, "w") as f:
            json.dump(roster_list, f, indent=4)

        print(f"✅ Saved roster for '{team_name}' to {file_path}")

    except ValueError as e:
        print(f"❌ Skipping {team_name}: {e}")
