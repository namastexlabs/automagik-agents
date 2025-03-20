"""Discord tools interface.

This module provides a compatibility layer for Discord tools.
"""
import logging
from typing import List, Dict, Any
from pydantic_ai import RunContext
from pydantic_ai.tools import Tool

from .tool import (
    list_guilds_and_channels,
    get_guild_info,
    fetch_messages,
    send_message
)

logger = logging.getLogger(__name__)

class DiscordTools:
    """Discord tools interface for compatibility with old code."""
    
    def __init__(self, bot_token: str):
        """Initialize Discord tools with a bot token.
        
        Args:
            bot_token: Discord bot token
        """
        self.bot_token = bot_token
    
    async def list_guilds_and_channels(self, ctx: RunContext[Dict]) -> Dict[str, Any]:
        """Lists all guilds and channels the bot has access to.
        
        Args:
            ctx: The run context
            
        Returns:
            Dict with the guild and channel information
        """
        return await list_guilds_and_channels(ctx, self.bot_token)
    
    async def get_guild_info(self, ctx: RunContext[Dict], guild_id: str) -> Dict[str, Any]:
        """Retrieves information about a specific guild.
        
        Args:
            ctx: The run context
            guild_id: ID of the guild to retrieve information for
            
        Returns:
            Dict with the guild information
        """
        return await get_guild_info(ctx, self.bot_token, guild_id)
    
    async def fetch_messages(self, ctx: RunContext[Dict], channel_id: str, limit: int = 100) -> Dict[str, Any]:
        """Fetches messages from a specific channel.
        
        Args:
            ctx: The run context
            channel_id: ID of the channel to fetch messages from
            limit: Maximum number of messages to retrieve
            
        Returns:
            Dict with the fetched messages
        """
        return await fetch_messages(ctx, self.bot_token, channel_id, limit)
    
    async def send_message(self, ctx: RunContext[Dict], channel_id: str, content: str) -> Dict[str, Any]:
        """Sends a message to a specific channel.
        
        Args:
            ctx: The run context
            channel_id: ID of the channel to send the message to
            content: Content of the message to send
            
        Returns:
            Dict with information about the sent message
        """
        return await send_message(ctx, self.bot_token, channel_id, content)
    
    @property
    def tools(self) -> List:
        """Returns the list of available tool functions."""
        return [
            self.list_guilds_and_channels,
            self.get_guild_info,
            self.fetch_messages,
            self.send_message
        ] 