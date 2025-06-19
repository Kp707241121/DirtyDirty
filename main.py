# main.py
import streamlit as st

st.set_page_config(
    page_title="Fantasy Baseball Dashboard",
    page_icon="⚾",
    layout="wide",
)

st.title("⚾ Welcome to the Fantasy Baseball Dashboard")
st.markdown("""
This dashboard lets you explore:
- 🏆 Standings  
- 📈 Team stats  
- 🧭 Radar
- ⚾ Rosters     
Use the left sidebar to navigate between pages.
""")
