from discord.ext import commands
from discord import app_commands, Interaction
import logging

from api import ClashKingAPI, ClashTag

async def cwl_season(clan_tag: str, season: str):
    api = ClashKingAPI()
    tag_clean = ClashTag.format(clan_tag)
    data = await api.get_cwl_season(tag_clean, season)


    # TODO reduce cognitive complexity of below code by breaking down into methods
    members = {}
    for clan in data['clans']:
        if clan['tag'] == clan_tag:
            for member in clan['members']:
                member['attacks'] = 0
                member['missed_attacks'] = 0
                member['stars'] = 0
                member['total_destruction'] = 0
                members[member['tag']] = member
            break

    for round in data['rounds']:
        for war in round['warTags']:
            if war['clan']['tag'] == clan_tag or war['opponent']['tag'] == clan_tag:
                war_focus = 'clan' if war['clan']['tag'] == clan_tag else 'opponent'
                war_members = war[war_focus]['members']

                for member in war_members:
                    if member.get('attacks'):
                        members[member['tag']]['attacks'] += 1
                        members[member['tag']]['stars'] += member['attacks'][0]['stars']
                        members[member['tag']]['total_destruction'] += member['attacks'][0]['destructionPercentage']
                        # print(f"War: {war['tag']} - Member: {member['name']} ({member['tag']}) Attacks: {member['attacks']}")
                    else:
                        members[member['tag']]['missed_attacks'] += 1
                        # print(f"War: {war['tag']} - Member: {member['name']} MISSED")

    for member in members:
        print(members[member])


class CWLCog(commands.Cog):
    """War-related commands"""

    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger(__name__)

    @app_commands.command(name='cwl-result', description='Shows a clans\'s CWL review player by player')
    @app_commands.describe(
        clan_tag='Clan tag',
        season='CWL season format YYYY-MM (e.g., 2024-09)'
    )
    async def cwl_result(self, interaction: Interaction, clan_tag: str, season: str):
        await cwl_season(clan_tag, season)


async def setup(bot):
    await bot.add_cog(CWLCog(bot))