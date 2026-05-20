from discord.ext import commands
from discord import app_commands, Interaction
import logging

from api import ClashKingAPI, ClashTag

async def get_all_seasons(clan_tag:str, seasons:int) -> list[dict]:
    api = ClashKingAPI()
    tag_clean = ClashTag.format(clan_tag)
    seasons_list = await api.get_season_list(seasons)

    result = []
    for season in seasons_list:
        result.append(await api.get_cwl_season(tag_clean, season))
    return result

async def get_cwl_data(clan_tag: str, seasons: int) -> dict:
    seasons_data = await get_all_seasons(clan_tag, seasons)  # Pass original

    members = {}
    for season_data in seasons_data:
        season = season_data['season']
        total_rounds = len(season_data['rounds'])

        # Step 1: Initialize/update members dict from clan data for this season
        for clan in season_data['clans']:
            if clan['tag'] == clan_tag:  # Compare with original clan_tag, not tag_clean
                for member in clan['members']:
                    member_tag = member['tag']
                    if member_tag not in members:
                        members[member_tag] = member.copy()
                        members[member_tag]['cwl_results'] = {}
                    members[member_tag]['cwl_results'][season] = [None] * total_rounds
                break

        # Step 2: Process each round and update member stats
        for round_index, round_data in enumerate(season_data['rounds']):
            for war in round_data['warTags']:
                if war['clan']['tag'] == clan_tag:  # Use original clan_tag here too
                    war_side = war['clan']
                elif war['opponent']['tag'] == clan_tag:  # And here
                    war_side = war['opponent']
                else:
                    continue

                for member in war_side['members']:
                    if member['tag'] in members:
                        result = member['attacks'][0]['stars'] if member.get('attacks') else -1
                        members[member['tag']]['cwl_results'][season][round_index] = result

    return members

async def cwl_season(clan_tag: str, season: str):
    api = ClashKingAPI()
    tag_clean = ClashTag.format(clan_tag)
    data = await api.get_cwl_season(tag_clean, season)

    total_rounds = len(data['rounds'])

    # Step 1: Initialize members dict from clan data
    members = {}
    for clan in data['clans']:
        if clan['tag'] == clan_tag:
            for member in clan['members']:
                member['cwl_results'] = {season: [None] * total_rounds}
                members[member['tag']] = member
            break

    # Step 2: Process each round and update member stats
    for round_index, round_data in enumerate(data['rounds']):
        for war in round_data['warTags']:
            # Determine which team we're tracking
            if war['clan']['tag'] == clan_tag:
                war_side = war['clan']
            elif war['opponent']['tag'] == clan_tag:
                war_side = war['opponent']
            else:
                continue

            # Update stats for each member in this war
            for member in war_side['members']:
                if member['tag'] in members:
                    result = member['attacks'][0]['stars'] if member.get('attacks') else -1
                    members[member['tag']]['cwl_results'][season][round_index] = result

    for x in members:
        print(members[x])

    return members


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