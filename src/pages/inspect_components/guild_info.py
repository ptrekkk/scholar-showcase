import streamlit as st


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


def add_guild_info(player_info_dict):
    guild_name = find_guild_name(player_info_dict)
    if guild_name:
        st.subheader(f"🏰 Member of guild: {guild_name}")
    else:
        st.subheader("❌ Not a member of any guild")
