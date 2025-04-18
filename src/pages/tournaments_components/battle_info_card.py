# CSS styles for battle card
battle_info_styles = """
<style>
.battle-card {
    flex: 2;
    position: relative;
    min-height: 60px;
    min-width: 500px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    background-color: transparent;
    padding-left: 1rem;
    background: url(https://img.icons8.com/ios-filled/100/crossed-swords.png) no-repeat left center;
    background-size: 40px;
    font-size: 16px;
}
.battle-card-content {
    display: flex;
    width: auto;
    justify-content: space-between;
}
.battle-col {
    display: flex;
    flex-direction: column;
    justify-content: left;
    padding-left: 1rem;
    padding-right: 1rem;
}
.battle-col span {
    margin-bottom: 2px;
}
.battle-winrate {
    font-weight: bold;
    font-size: 16px;
    margin-bottom: 5px;
}
</style>
"""


def format_finish_counts(places):
    return {
        "first": places.count(1),
        "second": places.count(2),
        "third": places.count(3),
        "top10": sum(1 for p in places if 4 <= p <= 10),
        "over10": sum(1 for p in places if p > 10),
    }


def get_battle_info_card(row):
    counts = format_finish_counts(row["finish"])
    battles = row['battles']
    tournaments_played = row['tournaments']
    winrate = row['win rate']

    return f"""<div class='battle-card' title='Wins: {row["wins"]}, Losses: {row["losses"]}'>
        <div class='battle-card-content'>
            <div class='battle-col'>⚔️ {winrate}% (WR)</div>
            <div class='battle-col'>
                <span>🥇 {counts["first"]}x</span>
                <span>🥈 {counts["second"]}x</span>
                <span>🥉 {counts["third"]}x</span>
            </div>
            <div class='battle-col'>
                <span>🔟 {counts["top10"]}x</span>
                <span>➕ {counts["over10"]}x</span>
            </div>
            <div class='battle-col'>
                <span># {tournaments_played} tournaments played</span>
                <span># {battles} amount of battles</span>
            </div>
        </div>
    </div>"""
