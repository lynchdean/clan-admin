import os
from typing import Optional, Dict, Any
from .base import BaseAPI, ClashTag

class ClashOfficialAPI(BaseAPI):
    API_URL = "https://api.clashofclans.com/v1"
    
    def __init__(self, token: str = None):
        self.token = token or os.getenv("CLASH_API_TOKEN")
        self._headers = {"Authorization": f"Bearer {self.token}"}

    async def get_clan(self, tag: str) -> Optional[Dict[str, Any]]:
        """Get clan information from official API"""
        return await self._make_request(
            ["clans", ClashTag.format(tag)],
            headers=self._headers
        )

    async def get_player(self, tag: str) -> Optional[Dict[str, Any]]:
        """Get player information from official API"""
        return await self._make_request(
            ["players", ClashTag.format(tag)],
            headers=self._headers
        )