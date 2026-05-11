from datetime import datetime
from dateutil.relativedelta import relativedelta
from discord.ext import commands
from discord import app_commands, Interaction
import logging

from api import ClashKingAPI, ClashTag
from models import Attack
from models.season import Season


def get_cwl_timestamps(num_months):
    now = datetime.now()
    current = datetime(now.year, now.month, 1)
    timestamps = []
    for _ in range(num_months):
        start_dt = current
        end_dt = current.replace(day=10)
        timestamps.append((int(start_dt.timestamp()),
                           int(end_dt.timestamp()),
                           start_dt.month,
                           start_dt.year))
        current -= relativedelta(months=1)
    return timestamps

async def cwl_review(player_tag, num_cwls=1):
    """Review previous CWLs for a player"""
    timestamps = get_cwl_timestamps(num_cwls)

    seasons = []
    for start, end, month, year in timestamps:
        print(f"Season {month}-{year}")

        api = ClashKingAPI()
        war_data = await api.get_player_warhits(
            tag=ClashTag.format(player_tag),
            limit=50,
            timestamp_start=start,
            timestamp_end=end
        )

        attacks = []
        if war_data and war_data.get('items'):
            for item in war_data['items']:
                attack = Attack.from_api(item)
                attacks.append(attack)

        season = Season.from_data(year, month, attacks)
        seasons.append(season)

    for s in seasons:
        print(s)
        print(f"- Avg stars: {round(s.avg_stars(), 1)}")
        print(f"- Avg destruction: {round(s.avg_destruction(), 1)}")

class WarsCog(commands.Cog):
    """War-related commands"""
    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger(__name__)

    @app_commands.command(name='cwlhits', description='Shows a player\'s CWL attacks grouped by season')
    @app_commands.describe(
        tag='Player tag (e.g., #ABC123 or ABC123)',
        seasons='Number of CWL seasons to show (default: 1, max: 6)'
    )
    async def cwlhits(self, interaction: Interaction, tag: str, seasons: int = 1):
        await cwl_review(player_tag=tag, num_cwls=seasons)

async def setup(bot):
    await bot.add_cog(WarsCog(bot))
