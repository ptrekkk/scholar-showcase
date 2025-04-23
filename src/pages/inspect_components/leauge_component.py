import pandas as pd
import streamlit as st

from src.utils.icons import WEB_URL
from src.utils.static_enums import LEAGUE_MAPPING

league_info_style = """<style>
        .league-card {
            position: relative;
            border-radius: 16px;
            padding: 10px;
            margin: 10px 0;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.6);
            background-size: cover;
            background-position: center;
            overflow: hidden;
            height: 220px;
        }

        .league-card .overlay {
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0, 0, 0, 0.5);
            padding: 16px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            border-radius: 16px;
        }

        .league-card h2 {
            margin-top: 4px;
            font-size: 24px;
            color: #fefae0;
        }

        .league-card h3 {
            margin: 2px;
            font-size: 20px;
            color: #fefae0;
        }

        .league-card p {
            margin: 1px;
            font-size: 16px;
            color: #fefae0;
        }
        </style>"""


def get_league_icon(league, format_type):
    return f"{WEB_URL}website/icons/leagues/{format_type}_150/league_{league}.png"


def league_info(league_df, format_type):
    required_columns = {"rating", "league", "wins", "battles"}
    if league_df.empty or not required_columns.issubset(league_df.columns):
        return  # Skip the function safely if required data is missing

    rating = league_df.rating.iloc[0]
    league = league_df.league.iloc[0]
    wins = league_df.wins.iloc[0]
    battles = league_df.battles.iloc[0]
    rate = round(wins / battles * 100)
    if format_type == 'survival':
        icon = get_league_icon(league, "wild")
    else:
        icon = get_league_icon(league, format_type)

    league_name = LEAGUE_MAPPING.get(league, "Unknown")

    st.markdown(
        f"""
        <div class="league-card" style="background-image: url('{icon}');">
            <div class="overlay">
                <h2>{format_type.title()}</h2>
                <h3>{league_name}</h3>
                <p><strong>Rating:</strong> {rating}</p>
                <p><strong>Battles:</strong> {wins}/{battles - wins} (W/L)</p>
                <p><strong>Win Rate:</strong> {rate}%</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


def add_league_cards(player_info_dict):
    modern_df = pd.DataFrame(player_info_dict['season_details']['modern'], index=[0])
    wild_df = pd.DataFrame(player_info_dict['season_details']['wild'], index=[0])
    survival_df = pd.DataFrame(player_info_dict['season_details']['survival'], index=[0])
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
