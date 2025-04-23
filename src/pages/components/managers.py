import streamlit as st

from src.api import db_actions
from src.pages.tournaments_components.contact_info_card import get_contact_info_card
from src.pages.tournaments_components.player_info_card import get_player_info_card
from src.utils.themes import get_back_colors

container_style = """<style>
    .flex-container {
        display: flex;
        justify-content: space-between;
        gap: 10px;
        flex-wrap: wrap;
    }

    @media screen and (max-width: 768px) {
        .flex-container {
            flex-direction: column;
        }
    }
    </style>"""


def get_page():
    st.title("Registered Managers")
    row_colors = get_back_colors()

    df = db_actions.get_all_managers()

    for idx, (_, row) in enumerate(df.iterrows()):
        bg_color = row_colors[idx % 2]

        player_info_card = get_player_info_card(row)
        contact_info_info = get_contact_info_card(row)

        st.markdown(f"""
        <div style='background-color:{bg_color}; padding: 15px; border-radius: 10px; margin-bottom: 15px;'>
            <div class='flex-container'>
                {player_info_card}
                {contact_info_info}
            </div>
        </div>
        """, unsafe_allow_html=True)
