import streamlit as st
import json
import pandas as pd
from leagueManager import LeagueManager

# Load saved stats
with open("team_stats.json") as f:
    team_stats = json.load(f)

# Create stats DataFrame
df_stats = pd.DataFrame.from_dict(team_stats, orient='index')
df_stats.index.name = "Team"
STAT_ORDER = ['R', 'HR', 'RBI', 'OBP', 'SB', 'K', 'W', 'SV', 'ERA', 'WHIP']
df_stats = df_stats[STAT_ORDER]

# Get live standings
manager = LeagueManager(league_id=121531, year=2025)
league = manager.get_league()
standings = league.standings()

# Create standings DataFrame (include image URL)
df_standings = pd.DataFrame([{
    "Overall": idx + 1,
    "Logo": team.logo_url ,
    "Team": team.team_name,
    "Wins": team.wins,
    "Losses": team.losses,
    "Ties": team.ties
} for idx, team in enumerate(standings)])

# Streamlit layout
st.title("📊 Fantasy Baseball Dashboard (2025)")

st.header("📈 Accumulated Stats")
st.dataframe(df_stats)

st.header("🏆 League Standings")
st.data_editor(
    df_standings,
    column_config={
        "Logo": st.column_config.ImageColumn(
            "Team Logo", width="medium"
        )
    },
    hide_index=True,
    use_container_width=True
)
