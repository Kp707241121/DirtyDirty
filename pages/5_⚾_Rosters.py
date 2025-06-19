import json
import streamlit as st
import pandas as pd
from leagueManager import LeagueManager
from teams import Team

# Load team mapping
with open("teams.json", "r") as f:
    team_dict = json.load(f)

# Helper
def get_team_index_by_id(league, team_id):
    for i, team in enumerate(league.teams):
        if team.team_id == team_id:
            return i
    raise ValueError(f"Team ID '{team_id}' not found in league.")

# Connect to league
manager = LeagueManager(league_id=121531, year=2025)
league = manager.get_league()

# Build nested dict: {team_name: roster_list}
team_rosters = {}

for team_id_str, team_name in team_dict.items():
    try:
        team_id = int(team_id_str)
        team_index = get_team_index_by_id(league, team_id)
        team = Team(league, team_index)
        roster = team.get_roster()  # assumed list of "Name (Position)"
        team_rosters[team_name] = roster
    except Exception as e:
        st.warning(f"Skipping {team_name}: {e}")

# --- UI: Dropdown to select a team ---
team_names = sorted(team_rosters.keys())
selected_team = st.selectbox("Select a team", team_names)

# --- Show roster as a table ---
if selected_team:
    roster_list = team_rosters[selected_team]

    # Convert to DataFrame and extract player/position
    df = pd.DataFrame(roster_list, columns=["Raw"])
    df["Position"] = df["Raw"].str.extract(r'\((.*?)\)')
    df["Player"] = df["Raw"].str.replace(r'\s*\(.*?\)', '', regex=True)
    df = df[["Player", "Position"]]

    st.subheader(f"Roster for {selected_team}")
    st.dataframe(df, use_container_width=True, hide_index=True)
