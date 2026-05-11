from typing import Optional, Dict, Any

from models import season
from .base import BaseAPI, ClashTag


class ClashKingAPI(BaseAPI):
    API_URL = "https://api.clashk.ing"

    def _clean_tag(self, tag: str) -> str:
        """Format tag for API use"""
        return ClashTag.format(tag)

    async def get_clan(self, tag: str) -> Optional[Dict[str, Any]]:
        """Get clan information"""
        return await self._make_request(["clans", self._clean_tag(tag)])

    async def get_player(self, tag: str) -> Optional[Dict[str, Any]]:
        """Get player information"""
        return await self._make_request(["players", self._clean_tag(tag)])

    async def get_player_stats(self, tag: str) -> Optional[Dict[str, Any]]:
        """Get detailed player statistics"""
        return await self._make_request(["player", self._clean_tag(tag), "stats"])

    async def get_player_history(self, tag: str, season: str) -> Optional[Dict[str, Any]]:
        """Get player's historical data for a specific season"""
        return await self._make_request([
            "player",
            self._clean_tag(tag),
            "historical",
            season
        ])

    async def get_clan_wars(
            self,
            tag: str,
            *,
            timestamp_start: Optional[int] = None,
            timestamp_end: Optional[int] = None,
            limit: Optional[int] = None
    ) -> Optional[Dict[str, Any]]:
        """Get clan war history with optional filters"""
        params = {}
        if timestamp_start is not None:
            params['timestamp_start'] = timestamp_start
        if timestamp_end is not None:
            params['timestamp_end'] = timestamp_end
        if limit is not None:
            params['limit'] = limit

        return await self._make_request(
            ["war", self._clean_tag(tag), "previous"],
            params=params
        )

    async def get_player_warhits(
            self,
            tag: str,
            *,
            limit: Optional[int] = None,
            timestamp_start: Optional[int] = None,
            timestamp_end: Optional[int] = None
    ) -> Optional[Dict[str, Any]]:
        """Get player's war attack history

        Args:
            tag: Player tag
            limit: Optional number of wars to return
            timestamp_start: Optional start timestamp for filtering wars
            timestamp_end: Optional end timestamp for filtering wars
        Returns:
            Dictionary containing war hits or None if not found
        """
        params = {
            'timestamp_start': timestamp_start if timestamp_start is not None else 0,
            'timestamp_end': timestamp_end if timestamp_end is not None else 2527625513,
            'limit': limit if limit is not None else 10
        }

        return await self._make_request(
            ["player", f"%23{tag.lstrip('#').upper()}", "warhits"],
            params=params
        )

    async def get_cwl_season(self, clan_tag: str, season: str):
        """
        Get CWL season information for specific season YYYY-MM
        :arg season: CWL season YYYY-MM
        :return: Dictionary containing CWL season information
        """
        return await self._make_request([
            "cwl",
            ClashTag.format(clan_tag),
            season
        ])
