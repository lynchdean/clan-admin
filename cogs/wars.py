from datetime import datetime
from dateutil.relativedelta import relativedelta
from discord.ext import commands
from discord import app_commands, Interaction
import logging

from api import ClashKingAPI, ClashTag
from models import Attack

def get_cwl_timestamps(num_months):
    now = datetime.now()
    current = datetime(now.year, now.month, 1)
    timestamps = []
    for _ in range(num_months):
        start_dt = current
        end_dt = current.replace(day=10)
        timestamps.append((int(start_dt.timestamp()),
                           int(end_dt.timestamp()),
                           f"{start_dt.month}-{start_dt.year}"))
        current -= relativedelta(months=1)
    return timestamps

async def cwl_review(player_tag, num_cwls=1):
    """Review previous CWLs for a player"""
    timestamps = get_cwl_timestamps(num_cwls)

    seasons = {}
    for start, end, season in timestamps:
        print(f"Season {season}")

        api = ClashKingAPI()
        war_data = await api.get_player_warhits(
            tag=player_tag,
            limit=50,
            timestamp_start=start,
            timestamp_end=end
        )

        wars = []
        if war_data and war_data.get('items'):
            for item in war_data['items']:
                attack = Attack.from_api(item)
                wars.append(attack)


        seasons[season] = wars

    for s in seasons:
        print(f"Season {s}")
        for attack in seasons[s]:
            print(attack)

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
