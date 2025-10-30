import aiohttp
import os
from typing import Optional, Dict, Any
from .base import ClashAPIBase, ClashTag

class ClashOfficialAPI(ClashAPIBase):
    API_URL = "https://api.clashofclans.com/v1"
    
    def __init__(self, token: str = None):
        self.token = token or os.getenv("CLASH_API_TOKEN")

    async def _make_request(self, endpoint: str, tag: str) -> Optional[Dict[str, Any]]:
        api_tag = ClashTag.format(tag)
        headers = {"Authorization": f"Bearer {self.token}"}
        
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.API_URL}/{endpoint}/{api_tag}", headers=headers) as resp:
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

    @staticmethod
    def _format_tag(tag: str) -> str:
        if not tag.startswith("#"):
            return "%23" + tag
        return tag.replace("#", "%23")