import pandas as pd
import streamlit as st

from src.api import spl
from src.pages.tournaments_components.battle_info_card import get_battle_info_card
from src.utils.themes import get_back_colors
from src.utils.tournaments_utils import get_qualified_tournaments, calculate_win_rate


def add_tournaments_section(df, player):
    if df.empty:
        st.warning("❌ No qualified tournaments found")

    filtered_tournaments = df[df['name'].isin(get_qualified_tournaments())]

    all_tournaments_played_info = get_played_tournaments(filtered_tournaments, player)
    st.title(f"👤 {player} Entered '{all_tournaments_played_info.index.size}' Qualified Tournaments")
    add_tournaments_cards(all_tournaments_played_info)


def add_tournaments_cards(df):
    if df.empty:
        st.warning(
            "❌ No qualified tournaments for player found.\n\n Qualified tournaments are:\n\n" +
            "\n".join(f"- {t}" for t in get_qualified_tournaments())
        )
    if not df.empty:
        grouped = df.groupby('name').agg({
            'wins': 'sum',
            'losses': 'sum',
            'finish': lambda x: list(x),
        }).reset_index()
        grouped['tournaments_played'] = grouped['finish'].apply(len)
        grouped['tournaments'] = grouped['finish'].apply(len)
        grouped['battles'] = grouped["wins"] + grouped["losses"]
        grouped['win rate'] = grouped.apply(calculate_win_rate, axis=1)

        row_colors = get_back_colors()
        for idx, (_, row) in enumerate(grouped.iterrows()):
            bg_color = row_colors[idx % 2]
            st.subheader(f'⚔️ - {row['name']}')
            battle_info_card = get_battle_info_card(row)
            st.markdown(f"""
            <div style='background-color:{bg_color}; padding: 15px; border-radius: 10px; margin-bottom: 15px;'>
                <div class='flex-container'>
                    {battle_info_card}
                </div>
            </div>""", unsafe_allow_html=True)


def get_played_tournaments(filtered_tournaments, player):
    all_tournaments_played_info = pd.DataFrame()
    for idx, row in filtered_tournaments.iterrows():
        tournament = spl.get_tournament(row['id'])
        player_row = tournament[tournament.player == player].copy()
        player_row['name'] = row['name']
        all_tournaments_played_info = pd.concat([all_tournaments_played_info, player_row], ignore_index=True)
    return all_tournaments_played_info
