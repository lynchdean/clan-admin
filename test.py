import asyncio
from cogs.cwl import CWLCog, cwl_season, get_all_seasons, get_cwl_data
from api import ClashKingAPI, ClashTag

if "__main__" == __name__:
    data = asyncio.run(get_cwl_data("#2Y8UJ0VPU", 2))
    for member in data:
        print(data[member])