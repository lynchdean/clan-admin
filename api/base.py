from abc import ABC
import aiohttp
from typing import Optional, Dict, Any, Mapping, List, Union
from urllib.parse import urlencode
import logging

logger = logging.getLogger(__name__)

class ClashTag:
    """Utility class for Clash tag operations"""

    @staticmethod
    def format(tag: str) -> str:
        """Formats a tag for use in APIs."""
        tag = tag.upper().lstrip('#')
        return f"%23{tag}"

class BaseAPI(ABC):
    """Base class for API implementations with shared HTTP functionality"""
    
    API_URL: str

    async def _make_request(
        self,
        path_segments: List[str],
        headers: Optional[Mapping[str, str]] = None,
        params: Optional[Dict[str, Union[str, int]]] = None
    ) -> Optional[Dict[str, Any]]:
        """Makes an HTTP GET request to the API"""
        # Build the URL from segments
        url = self.API_URL
        for segment in path_segments:
            if segment:  # Skip empty segments
                url = f"{url}/{segment}"

        # Add query parameters if any
        if params:
            url = f"{url}?{urlencode(params)}"

        logger.info(f"Making request to: {url}")

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as resp:
                if resp.status == 200:
                    return await resp.json()
                logger.warning(f"Request failed with status {resp.status}")
                return None