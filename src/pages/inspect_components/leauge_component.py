import streamlit as st

from src.utils.icons import WEB_URL
from src.utils.static_enums import LEAGUE_MAPPING

league_info_style = """<style>
        .league-card {
            position: relative;
            background-size: cover;
            background-position: center;
            border-radius: 16px;
            padding: 10px;
            margin: 10px 0;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
            overflow: hidden;
        }
        .league-card::before {
            content: "";
            position: absolute;
            inset: 0;
            background: rgba(0, 0, 0, 0.1); /* Adjust transparency here */
            border-radius: 16px;
            z-index: 0;
        }
        .league-card h3 {
            margin-top: 0;
            font-size: 24px;
        }
        .league-card h3 {
            align: center;
            font-size: 24px;
        }
        .league-card p {
            margin: 6px 0;
            font-size: 16px;
        }
        </style>"""


def get_league_icon(league, format_type):
    return f"{WEB_URL}website/icons/leagues/{format_type}_150/league_{league}.png"


def league_info(league_df, format_type):
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
