from src.utils.icons import player_icon_url
from src.utils.themes import get_text_color

player_info_styles = """
<style>
.player-card {
    flex: 1;
    position: relative;
    min-height: 60px;
    min-width: 150px;
    display: flex;
    align-items: center;
    justify-content: flex-start;
    background-color: transparent;
    padding-left: 10px;
    border-radius: 10px;
    overflow: hidden;
}

.player-card-link {
    display: flex;
    align-items: center;
    text-decoration: none !important;
    color: inherit;
    width: 100%;
    height: 100%;
    padding: 10px;
    border-radius: 10px;
    transition: background 0.2s ease;
}

.player-card-link:hover {
    background-color: rgba(255, 255, 255, 0.05);
}

.player-card img {
    height: 30px;
    opacity: 0.8;
    margin-right: 5px;
}

.player-card span {
    color: """ + get_text_color() + """;
    font-weight: bold;
    font-size: 18px;
    text-decoration: none !important;
}
</style>
"""


def get_player_info_card(row):
    return f"""<div class='player-card'>
            <a href='inspect?player={row["player"]}' target='_self' class='player-card-link'>
                <img src='{player_icon_url}' alt='player icon' />
                <span>{row["player"]}</span>
            </a>
        </div>"""
