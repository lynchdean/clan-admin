import asyncio
from cogs.cwl import CWLCog, cwl_season
from api import ClashKingAPI, ClashTag




# Test the function
if __name__ == "__main__":
    asyncio.run(cwl_season(clan_tag="#2Y8UJ0VPU", season="2026-05"))
