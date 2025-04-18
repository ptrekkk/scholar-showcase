import pandas as pd
import streamlit as st

from src.api import spl
from src.pages.inspect_components.leauge_component import league_info, league_info_style


def get_page():
    query_params = st.query_params.to_dict()
    player = query_params.get("player", None)

    st.title("🔍 Inspect Page - Player!")

    player = st.text_input("account name", value=player)
    if not player:
        st.info("Please enter a player account to begin.")

    with st.spinner("Loading data..."):
        if player:
            result = spl.get_player_profile(player)
            if not result:
                st.warning("Player not found, enter valid splinterlands account")
            if result:
                modern_df = pd.DataFrame(result['season_details']['modern'], index=[0])
                wild_df = pd.DataFrame(result['season_details']['wild'], index=[0])
                survival_df = pd.DataFrame(result['season_details']['survival'], index=[0])

                league_data = []
                if not modern_df.empty:
                    league_data.append(("modern", modern_df))
                if not wild_df.empty:
                    league_data.append(("wild", wild_df))
                if not survival_df.empty:
                    league_data.append(("survival", survival_df))

                # Show cards in left-to-right order using columns
                st.markdown(league_info_style, unsafe_allow_html=True)
                columns = st.columns(3)

                for i, (format_type, df) in enumerate(league_data):
                    with columns[i]:
                        league_info(df, format_type)

                guild_name = find_guild_name(result)
                if guild_name:
                    st.subheader(f"Member of guild: {guild_name}")
                else:
                    st.subheader("No member of a guild")


def find_guild_name(d):
    if isinstance(d, dict):
        for key, value in d.items():
            if key == "guild_name":
                return value
            result = find_guild_name(value)
            if result is not None:
                return result
    elif isinstance(d, list):
        for item in d:
            result = find_guild_name(item)
            if result is not None:
                return result
    return None
