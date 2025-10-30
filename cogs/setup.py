from discord.ext import commands
from api import ClashOfficialAPI, ClashTag

class SetupCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.guild_links = {}  # {guild_id: clan_tag}
        self.clash_api = ClashOfficialAPI()

    @commands.has_permissions(administrator=True)
    @commands.command(name="setup")
    async def setup(self, ctx, tag: str):
        """Links a verified Clash of Clans clan tag to this Discord server."""
        display_tag = f"#{ClashTag.format(tag).replace('%23', '')}"

        try:
            clan = await self.clash_api.get_clan(tag)
            if not clan:
                await ctx.send(f"❌ No clan found with tag `{display_tag}`.")
                return

            self.guild_links[ctx.guild.id] = display_tag
            await ctx.send(f"✅ Linked this server to `{display_tag}` ({clan.get('name')}).")

        except Exception as e:
            await ctx.send(f"❌ Clash API error: {e}")

    @commands.command(name="show_setup")
    async def show_setup(self, ctx):
        """Shows the clan tag linked to this server."""
        tag = self.guild_links.get(ctx.guild.id)
        if not tag:
            await ctx.send("⚠️ No clan tag linked. Use `!setup <clan_tag>` first.")
            return
        await ctx.send(f"🔗 This server is linked to `{tag}`.")

async def setup(bot):
    await bot.add_cog(SetupCog(bot))