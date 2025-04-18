import re

import streamlit as st

from src.api import db_actions
from src.models.models import User, RoleEnum, RewardSplitEnum, PreferredModesEnum, PreferredLeagueEnum
from src.utils import notifications, local_storage_manager


def is_valid_discord(discord: str) -> bool:
    if not discord:
        return True

    if len(discord) > 50:
        return False

    # Legacy format: Username#1234
    legacy_pattern = r"^[\w]{2,32}#\d{4}$"

    # New Discord username format
    # Must be 2–32 chars, only a-z, 0-9, _ and ., no __ or .. or ._ or _.,
    # cannot start/end with . or _
    new_format_pattern = r"^(?!.*[_.]{2})[a-z0-9](?:[a-z0-9._]{0,30}[a-z0-9])?$"

    # Also allow user ID (Discord Snowflake ID)
    user_id_pattern = r"^\d{17,20}$"

    return bool(
        re.match(legacy_pattern, discord.lower()) or
        re.match(new_format_pattern, discord.lower()) or
        re.match(user_id_pattern, discord.lower())
    )


@st.dialog("User Settings")
def show_settings_dialog(user: User):
    if not user:
        st.warning("You must be logged in to access settings.")
        return

    st.text_input("Username", value=user.account, disabled=True)

    role_options = list(RoleEnum)
    current_index = role_options.index(user.role)
    role = st.selectbox("Role", options=RoleEnum, index=current_index)

    preferred_mode = None
    reward_split = None

    # Scholar-specific fields
    if role == RoleEnum.Scholar:
        with st.container(border=True):
            preferred_options = list(PreferredModesEnum)
            current_index = preferred_options.index(user.preferred_mode) if user.preferred_mode else 0
            preferred_mode = st.selectbox(
                "Preferred Mode",
                options=PreferredModesEnum,
                index=current_index
            )

            preferred_league_options = list(PreferredLeagueEnum)
            current_index = preferred_league_options.index(user.preferred_league) if user.preferred_league else 0
            preferred_league = st.selectbox(
                "Preferred League",
                options=PreferredLeagueEnum,
                index=current_index
            )

            reward_split_options = list(RewardSplitEnum)
            current_index = reward_split_options.index(user.reward_split) if user.reward_split else 0
            reward_split = st.selectbox(
                "Reward Split (Manager/Scholar)",
                options=RewardSplitEnum,
                index=current_index
            )

    discord = st.text_input("Discord", value=user.discord_reference or "")

    valid_discord = is_valid_discord(discord)
    if discord and not valid_discord:
        st.error("Please enter a valid discord name.")

    st.write("By entering these fields you consent that others can see your Discord username to contact you.")

    col_save, col_cancel = st.columns(2)
    with col_save:
        if st.button("💾 Save", key="save_settings_btn", disabled=not valid_discord):
            if is_valid_discord(discord):
                user.role = role
                user.discord_reference = discord.lower() if discord else None

                if role == RoleEnum.Scholar:
                    # Ensure Scholar always sets these fields
                    if not preferred_mode or not reward_split:
                        st.error("Preferred Mode and Reward Split are required for Scholars.")
                        return
                    user.preferred_mode = preferred_mode
                    user.preferred_league = preferred_league
                    user.reward_split = reward_split
                else:
                    # Not a Scholar? Clear the fields
                    user.preferred_mode = None
                    user.preferred_league = None
                    user.reward_split = None

                notifications.set_start_up_message("Settings saved.")
                updated_user = db_actions.update_user(user)
                local_storage_manager.save_user(updated_user)
                st.rerun()
            else:
                st.error("Invalid Discord name. Unable to perform save.")

    with col_cancel:
        if st.button("❌ Cancel", key="cancel_settings_btn"):
            st.rerun()
