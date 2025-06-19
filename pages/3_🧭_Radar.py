# pages/3_🧭_Radar.py

import streamlit as st
import json
import pandas as pd
import plotly.express as px



# Load saved stats
with open("team_stats.json") as f:
    team_stats = json.load(f)

# Convert to DataFrame
df_stats = pd.DataFrame.from_dict(team_stats, orient='index')
df_stats.index.name = "Team"

# Normalize stats
stats = ['R', 'HR', 'RBI', 'OBP', 'SB', 'K', 'W', 'SV', 'ERA', 'WHIP']
INVERT_STATS = {'ERA', 'WHIP', 'OBP'}

df_normalized = (df_stats - df_stats.min()) / (df_stats.max() - df_stats.min())

# Invert where lower is better
for stat in INVERT_STATS:
    if stat in df_normalized:
        df_normalized[stat] = 1 - df_normalized[stat]

# 🔷 Multi-Team Radar Chart
st.title("🧭 Multi-Team Radar Chart")

teams_selected = st.multiselect("Select Teams", df_normalized.index, default=[df_normalized.index[0]])

if teams_selected:
    df_long = df_normalized.loc[teams_selected][stats].reset_index().melt(
        id_vars='Team', var_name='Stat', value_name='Value'
    )

    fig_multi = px.line_polar(
        df_long,
        r='Value',
        theta='Stat',
        color='Team',
        line_close=True,
        title="Team Comparison Radar (Normalized & Adjusted)"
    )
    fig_multi.update_traces(fill='toself')
    st.plotly_chart(fig_multi)
else:
    st.warning("Please select at least one team to display the radar chart.")

# 🔹 Single-Team Radar Chart
st.title("🧭 Single-Team Radar Chart")

team_selected = st.selectbox("Select Team", df_normalized.index)

fig_single = px.line_polar(
    r=df_normalized.loc[team_selected][stats],
    theta=stats,
    line_close=True,
    title=f"{team_selected} Stat Radar (Normalized)"
)
fig_single.update_traces(fill='toself')
st.plotly_chart(fig_single)
