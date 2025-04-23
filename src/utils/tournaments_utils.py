import streamlit as st


def get_qualified_tournaments():
    if 'settings' in st.secrets and "tournaments" in st.secrets["settings"]:
        return st.secrets["settings"]["tournaments"]
    else:
        return None


def calculate_win_rate(row):
    battles = row["wins"] + row["losses"]
    return round(row["wins"] / battles * 100) if battles > 0 else 0
