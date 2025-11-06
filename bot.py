import os
import logging
import asyncio
import discord
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()

# Turn off NaCl warning as voice is not used
discord.VoiceClient.warn_nacl = False

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('discord.log')
    ]
)

# Set specific loggers to be less verbose
logging.getLogger('discord').setLevel(logging.WARNING)
logging.getLogger('aiohttp').setLevel(logging.WARNING)

# Set up intents
intents = discord.Intents.default()
intents.message_content = True

class Bot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='!', intents=intents)
        self.logger = logging.getLogger(__name__)

    async def setup_hook(self):
        """Async initialization"""
        title = 'ClanAdmin v1.0.0'
        title_padding = ' ' * int((50 - len(title)) / 2)
        print('='*50)

        print(title_padding + 'ClanAdmin v1.0.0' + title_padding)
        print('='*50)

        # Load cogs from cogs folder
        print('Loading cogs...')
        for cog in os.listdir('cogs'):
            if cog.endswith('.py'):
                try:
                    await self.load_extension(f"cogs.{cog[:-3]}")
                    print(f"Loaded Cog: {cog[:-3]}")
                except Exception as e:
                    print(f"Failed to load cog {cog}: {e}")

        # Sync Slash Commands
        print('\nLoading slash commands...')
        try:
            synced = await self.tree.sync()
            for item in synced:
                print(f"Synced {item.name} command.")
            print(f"Synced {len(synced)} slash commands.")
        except Exception as e:
            print(f"Failed to sync commands: {e}")

    async def on_ready(self):
        """Called when the bot is ready and connected"""
        print(f'\nBot is online as {self.user.name}!')
        print(f'Connected to {len(self.guilds)} servers')
        print('='*50)

async def main():
    # Create bot instance
    bot = Bot()
    
    try:
        await bot.start(os.getenv("BOT_TOKEN"))
    except KeyboardInterrupt:
        print("\nShutting down gracefully...")
    finally:
        await bot.close()  # Changed from super().close() to bot.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nBot shutdown complete.")