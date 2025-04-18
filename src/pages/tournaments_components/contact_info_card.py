import pandas as pd

from src.utils.icons import discord_icon_url, sps_icon_url

# CSS Styles for Contact Info Card
contact_info_styles = """
<style>
.contact-card {
    flex: 2;
    display: flex;
    flex-direction: column;
    justify-content: center;
    margin-left: 1rem;
    padding-left: 1rem;
}
.contact-item {
    display: flex;
    align-items: center;
    margin-bottom: 0.1rem;
}
.contact-label {
    width: 160px;
    display: flex;
    align-items: center;
    font-weight: bold;
}
.contact-label img {
    height: 20px;
    margin-right: 8px;
}
.contact-value {
    flex: 1;
}
</style>
"""


def get_contact_info_card(row: pd.Series):
    if pd.isna(row["role"]) or row["role"] == 'Undefined':
        return """<div class='contact-card'>
            <div class='contact-item'>No contact info</div>
        </div>"""

    discord_html = "<div />"
    preferred_mode_html = "<div />"
    preferred_league_html = "<div />"
    reward_split_html = "<div />"

    if row.get("discord_reference"):
        discord_html = f"""<div class='contact-item'>
            <div class='contact-label'><img src='{discord_icon_url}' alt='discord' />Discord</div>
            <div class='contact-value'>{row["discord_reference"]}</div>
        </div>"""

    if row.get("preferred_mode"):
        preferred_mode_html = f"""<div class='contact-item'>
            <div class='contact-label'>⚔️ Preferred modes</div>
            <div class='contact-value'>{row["preferred_mode"]}</div>
        </div>"""

    if row.get("preferred_league"):
        preferred_league_html = f"""<div class='contact-item'>
            <div class='contact-label'>⚔️ Preferred league</div>
            <div class='contact-value'>{row["preferred_league"]}</div>
        </div>"""

    if row.get("reward_split"):
        reward_split_html = f"""<div class='contact-item'>
            <div class='contact-label'><img src='{sps_icon_url}' alt='SPS' />Reward Split</div>
            <div class='contact-value'>{row["reward_split"]}</div>
        </div>"""

    return f"""{contact_info_styles}<div class='contact-card'>
        {discord_html}
        {preferred_mode_html}
        {preferred_league_html}
        {reward_split_html}
    </div>"""
