
# pages/1_🏆_Standings.py

import streamlit as st
import pandas as pd
from leagueManager import LeagueManager  # Your LeagueManager class

st.header("🏆 League Standings")

# Initialize
manager = LeagueManager(league_id=121531, year=2025)
league = manager.get_league()

# Fetch standings
standings = league.standings()

df_standings = pd.DataFrame([{
    "Overall": idx + 1,
    "Logo": team.logo_url ,
    "Team": team.team_name,
    "Wins": team.wins,
    "Losses": team.losses,
    "Ties": team.ties
} for idx, team in enumerate(standings)])

# Streamlit layout

st.data_editor(
    df_standings,
    column_config={
        "Logo": st.column_config.ImageColumn(
            "Team Logo", width="small"
        )
    },
    hide_index=True,
    use_container_width=True
)

# Schedule
st.title("📅 Team Schedule Viewer")

# Collect schedule info
schedule_data = []

team_names = [team.team_name for team in league.teams]
selected_team_name = st.selectbox("Select a team to view schedule:", team_names)
selected_team = next(team for team in league.teams if team.team_name == selected_team_name)

st.subheader(f"Schedule for {selected_team_name}")

for matchup in selected_team.schedule:
    if matchup.home_team == selected_team:
        opponent = matchup.away_team
        location = "Home"
        score = matchup.home_team_live_score
    else:
        opponent = matchup.home_team
        location = "Away"

    opponent_name = opponent.team_name if opponent else "BYE"
    week = getattr(matchup, "matchup_period", None)

    schedule_data.append({
        "Week": matchup.week,
        "Opponent": opponent_name,
        "Location": location,
        "Score": score,
        "OpponentScore": matchup.away_team_live_score
    })

df = pd.DataFrame(schedule_data).sort_values(by="Week")
df["Result"] = df.apply(lambda row: "W" if row["Score"] > row["OpponentScore"] else "L" if row["Score"] < row["OpponentScore"] else "T" if row["Score"] == row["OpponentScore"] else "Pending", axis=1)
df_schedule = st.write(df, hide_index=True)