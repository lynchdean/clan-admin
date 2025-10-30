import os
import logging
import asyncio
import discord
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()

# Set up intents
intents = discord.Intents.default()
intents.message_content = True

# Logging handler
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

# Create the bot instance
bot = commands.Bot(command_prefix='!', intents=intents)

# Define async main entrypoint
async def main():
    async with bot:
        for cog in os.listdir('cogs'):
            if cog.endswith('.py'):
                await bot.load_extension(f"cogs.{cog[:-3]}")
                print(f"Loaded Cog: {cog[:-3]}")

        await bot.start(os.getenv("BOT_TOKEN"))

# Run the bot
if __name__ == "__main__":
    asyncio.run(main())