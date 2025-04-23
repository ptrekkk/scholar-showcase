import logging

import streamlit as st

from src.api import spl
from src.pages.components.scholars import add_scholar_card
from src.pages.inspect_components.guild_info import add_guild_info
from src.pages.inspect_components.leauge_component import add_league_cards
from src.pages.inspect_components.qualitfied_tournaments import add_tournaments_section

log = logging.getLogger("Inspect")


def get_page():
    query_params = st.query_params.to_dict()
    player = query_params.get("player", None)

    st.title("🔍 Inspect Page - Player!")

    player = st.text_input("account name", value=player)
    if not player:
        st.info("Please enter a player account to begin.")
        return

    with st.spinner("Loading data..."):
        if player:
            log.info(f"Inspect player: {player}")
            result_dict = spl.get_player_profile(player)
            if not result_dict:
                st.warning("Player not found, enter valid splinterlands account")
                return
            if result_dict:
                add_league_cards(result_dict)

                add_guild_info(result_dict)

            with st.spinner("Loading finished tournaments"):
                df = spl.get_complete_tournaments()
                add_tournaments_section(df, player)

            add_scholar_card(player)
