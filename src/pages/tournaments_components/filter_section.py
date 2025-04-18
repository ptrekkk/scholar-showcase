import pandas as pd
import streamlit as st

from src.models.models import RoleEnum

filter_players = "filter_players"
filter_role = "filter_role"
filter_reward_split = "filter_reward_split"
filter_preferred_mode = "filter_preferred_mode"
filter_preferred_league = "filter_preferred_league"
sorting = "sorting"


def apply_filters(df: pd.DataFrame):
    if st.session_state.get(filter_players):
        df = df[df.player.isin(st.session_state[filter_players])]
    if st.session_state.get(filter_role):
        df = df[df.role == RoleEnum.Scholar.value]
    if st.session_state.get(filter_reward_split):
        df = df[df.reward_splut.isin(st.session_state[filter_reward_split])]
    if st.session_state.get(filter_preferred_mode):
        df = df[df.preferred_mode.isin(st.session_state[filter_preferred_mode])]
    if st.session_state.get(filter_preferred_league):
        df = df[df.preferred_league.isin(st.session_state[filter_preferred_league])]

    return df


def apply_sorting(df: pd.DataFrame):
    if st.session_state.get(sorting):
        sort_by = st.session_state.get(sorting).lower()
        if sort_by in df.columns.to_list():
            if sort_by == 'player':
                ascending = True
            else:
                ascending = False
            df = df.sort_values(by=sort_by, ascending=ascending)
    return df


def get_page(df: pd.DataFrame):
    filtered_df = df.copy()

    players_options = df['player'].dropna().sort_values().unique().tolist()
    reward_split_options = df['reward_split'].dropna().sort_values().unique().tolist()
    preferred_mode_options = df['preferred_mode'].dropna().sort_values().unique().tolist()
    preferred_league_options = df['preferred_league'].dropna().sort_values().unique().tolist()
    sorting_options = ['Win', 'Win Rate', 'Losses', 'Player', 'Battles', 'Tournaments']

    st.markdown("### 🎛️ Filters")
    st.multiselect(
        "Players",
        options=players_options,
        key=filter_players,
        default=st.session_state.get(filter_players, []))
    with st.container(border=True):
        st.write("Scholar filters")
        st.multiselect(
            "Preferred Modes",
            options=preferred_mode_options,
            key=filter_preferred_mode,
            default=st.session_state.get(filter_preferred_mode, []))
        st.multiselect(
            "Preferred League",
            options=preferred_league_options,
            key=filter_preferred_league,
            default=st.session_state.get(filter_preferred_league, []))
        st.multiselect(
            "Reward Split",
            options=reward_split_options,
            key=filter_reward_split,
            default=st.session_state.get(filter_reward_split, []))
        st.checkbox(
            "Registered Scholars",
            key=filter_role,
            value=False,
        )
    st.selectbox(
        "Sorting",
        options=sorting_options,
        key=sorting,
    )

    df = apply_filters(filtered_df)
    return apply_sorting(df)
