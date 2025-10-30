from abc import ABC, abstractmethod
from typing import Optional, Dict, Any


class ClashTag:
    """Utility class for Clash tag operations"""

    @staticmethod
    def format(tag: str) -> str:
        """
        Formats a tag for use in APIs.
        Args:
            tag: The tag to format
            include_hash: If True, converts # to %23, if False removes #
        """
        tag = tag.upper().lstrip('#')
        return f"%23{tag}"


class ClashAPIBase(ABC):
    """Base class defining the interface for Clash API implementations"""
    
    @abstractmethod
    async def get_clan(self, tag: str) -> Optional[Dict[str, Any]]:
        """
        Fetch clan info by tag.
        Returns JSON dict if found, None if not found.
        Raises ClientError on network issues.
        """
        pass
    
    @abstractmethod
    async def get_player(self, tag: str) -> Optional[Dict[str, Any]]:
        """
        Fetch player info by tag.
        Returns JSON dict if found, None if not found.
        Raises ClientError on network issues.
        """
        pass