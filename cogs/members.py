from discord.ext import commands
from api import ClashOfficialAPI, ClashKingAPI, ClashTag
from cogs.setup import SetupCog


class MembersCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.official_api = ClashOfficialAPI()
        self.king_api = ClashKingAPI()

    @commands.command(name='review')
    async def review(self, ctx, tag: str):
        """Get basic player info from official API"""
        display_tag = f"#{ClashTag.format(tag).replace('%23', '')}"

        try:
            player = await self.official_api.get_player(tag)
            if not player:
                await ctx.send(f"❌ No player found with tag `{display_tag}`.")
                return

            await ctx.send(
                f"✅ Player found with tag `{display_tag}` \n"
                f"Name: {player['name']} \n"
                f"Clan: {player['clan']['name']}"
            )

        except Exception as e:
            await ctx.send(f"❌ Clash API error: {e}")

    @commands.command(name='extended_info')
    async def extended_info(self, ctx, tag: str):
        """Get additional player info from ClashKing API"""
        display_tag = f"#{ClashTag.format(tag).replace('%23', '')}"

        try:
            extra_data = await self.king_api.get_player(tag)
            if not extra_data:
                await ctx.send(f"❌ No extended data found for tag `{display_tag}`.")
                return

            # Handle ClashKing-specific data here
            await ctx.send(f"✅ Extended data found for `{display_tag}`...")

        except Exception as e:
            await ctx.send(f"❌ ClashKing API error: {e}")

async def setup(bot):
    await bot.add_cog(MembersCog(bot))