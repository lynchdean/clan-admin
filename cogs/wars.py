from discord.ext import commands

class WarsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def test(self, ctx):
        await ctx.send('Test Successful!')


async def setup(bot):
    await bot.add_cog(WarsCog(bot))