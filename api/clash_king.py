import aiohttp
from typing import Optional, Dict, Any
from .base import ClashAPIBase

class ClashKingAPI(ClashAPIBase):
    API_URL = "https://api.clashk.ing"
    
    async def _make_request(self, endpoint: str, tag: str) -> Optional[Dict[str, Any]]:
        # Remove the # from the tag as this API might have different requirements
        clean_tag = tag.replace("#", "")
        
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.API_URL}/{endpoint}/{clean_tag}") as resp:
                if resp.status == 200:
                    return await resp.json()
                elif resp.status == 404:
                    return None
                resp.raise_for_status()
                return None

    async def get_clan(self, tag: str) -> Optional[Dict[str, Any]]:
        return await self._make_request("clans", tag)

    async def get_player(self, tag: str) -> Optional[Dict[str, Any]]:
        return await self._make_request("players", tag)