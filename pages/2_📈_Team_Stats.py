# pages/2_📈_Team_Stats.py

import streamlit as st
import json
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from leagueManager import LeagueManager
from sklearn.preprocessing import MinMaxScaler
from pages import STAT_ORDER as stats

# Title
st.title("📈 Accumulated Team Stats")

# Load data
with open("team_stats.json") as f:
    team_stats = json.load(f)

# Convert to DataFrame
df = pd.DataFrame.from_dict(team_stats, orient="index")
df.index.name = "Team"
df = df[stats]  # Reorder columns

# Define formatting
float_cols = {'ERA', 'WHIP', 'OBP'}
format_dict = {col: "{:.3f}" if col in float_cols else "{:.0f}" for col in df.columns}

# Display styled DataFrame
st.dataframe(df.style.format(format_dict), use_container_width=True)

ASCENDING_STATS = {'ERA', 'WHIP'}

# --- Load Saved Stats ---
with open("team_stats.json") as f:
    team_stats = json.load(f)

df_stats = pd.DataFrame.from_dict(team_stats, orient='index')
df_stats.index.name = "Team"

# --- Load Logos Live ---
manager = LeagueManager(league_id=121531, year=2025)
league = manager.get_league()
logo_map = {team.team_name: team.logo_url for team in league.teams}

# --- Streamlit Page UI ---
st.title("📊 Team Performance Charts")

# --- Stat Selector & Bar Chart ---
selected_stat = st.selectbox("Choose a Stat to Compare", stats)

# Set sort order
ascending = True if selected_stat in ASCENDING_STATS else False

# Sort
df_sorted = df_stats.sort_values(by=selected_stat, ascending=ascending)

# Plot bar chart
fig, ax = plt.subplots(figsize=(12, 6))
bars = ax.bar(df_sorted.index, df_sorted[selected_stat], color='lightcoral')
ax.set_title(f"{selected_stat} by Team")
ax.set_xlabel("Team")
ax.set_ylabel(selected_stat)
plt.xticks(rotation=45)

# Add value labels
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width() / 2, height + 0.5, round(height, 2), ha='center', va='bottom')

st.pyplot(fig)

# --- Line Chart ---
selected_stat = st.selectbox("Choose a Stat to Plot Over Teams", stats)

# Set sort order
ascending = True if selected_stat in ASCENDING_STATS else False

# Sort
df_sorted = df_stats.sort_values(by=selected_stat, ascending=ascending)

# Plot line chart
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(df_sorted.index, df_sorted[selected_stat], marker='o', linestyle='-')
ax.set_title(f"{selected_stat} by Team")
ax.set_xlabel("Team")
ax.set_ylabel(selected_stat)
plt.xticks(rotation=45)
st.pyplot(fig)

# Normalize stats 0-1 range
scaler = MinMaxScaler()
df_normalized = pd.DataFrame(scaler.fit_transform(df_stats), 
                             columns=df_stats.columns,
                             index=df_stats.index)

# Melt for line plot
df_melt = df_normalized.reset_index().melt(id_vars='Team', var_name='Stat', value_name='Value')

fig_all = px.line(
    df_melt,
    x='Stat',
    y='Value',
    color='Team',
    line_group='Team',
    markers=True,
    title='Normalized Stat Comparison Across Teams'
)
st.plotly_chart(fig_all)