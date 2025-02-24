"""Discord tools for Sofia."""

from typing import List, Optional, Dict, Any
from pydantic_ai.tools import Tool
from pydantic_ai import RunContext
import discord
from discord.ext import commands
import asyncio

class DiscordError(Exception):
    """Base exception for Discord API errors"""
    pass

class DiscordTools:
    def __init__(self, bot_token: str):
        self.bot_token = bot_token
        self.client = discord.Client(intents=discord.Intents.default())

    async def _run_coroutine(self, coroutine):
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, asyncio.run, coroutine)

    async def list_guilds_and_channels(self, ctx: RunContext[Dict]) -> Dict[str, Any]:
        """
        Lists all guilds and channels the bot has access to.

        Example call: list_guilds_and_channels()
        
        Returns:
            Dict[str, Any]: Dictionary containing guilds and their channels
        """
        async def _list_guilds_and_channels():
            await self.client.login(self.bot_token)
            guilds_info = []
            for guild in self.client.guilds:
                channels_info = [{"name": channel.name, "id": str(channel.id), "type": str(channel.type)} for channel in guild.channels]
                guilds_info.append({
                    "name": guild.name,
                    "id": str(guild.id),
                    "channels": channels_info
                })
            await self.client.close()
            return guilds_info

        guilds_info = await self._run_coroutine(_list_guilds_and_channels())
        return {"success": True, "guilds": guilds_info}

    async def get_guild_info(self, ctx: RunContext[Dict], guild_id: str) -> Dict[str, Any]:
        """
        Retrieves information about a specific guild.

        Example call: get_guild_info(guild_id=1234567890)
        
        Args:
            ctx: The run context
            guild_id (str): The ID of the guild to retrieve info for
        Returns:
            Dict[str, Any]: Information about the guild
        """
        async def _get_guild_info():
            await self.client.login(self.bot_token)
            guild = self.client.get_guild(int(guild_id))
            if guild:
                info = {
                    "name": guild.name,
                    "id": str(guild.id),
                    "member_count": guild.member_count,
                    "channels": [{"name": channel.name, "id": str(channel.id), "type": str(channel.type)} for channel in guild.channels]
                }
            else:
                info = None
            await self.client.close()
            return info

        guild_info = await self._run_coroutine(_get_guild_info())
        if guild_info:
            return {"success": True, "guild_info": guild_info}
        else:
            return {"success": False, "error": f"Guild with ID {guild_id} not found."}

    async def fetch_messages(self, ctx: RunContext[Dict], channel_id: str, limit: int = 100) -> Dict[str, Any]:
        """
        Fetches messages from a specific channel.

        Example call: fetch_messages(channel_id=1234567890, limit=50)
        
        Args:
            ctx: The run context
            channel_id (str): The ID of the channel to fetch messages from
            limit (int): The maximum number of messages to retrieve (default: 100)
        Returns:
            Dict[str, Any]: Dictionary containing fetched messages
        """
        async def _fetch_messages():
            await self.client.login(self.bot_token)
            channel = self.client.get_channel(int(channel_id))
            if isinstance(channel, discord.TextChannel):
                messages = await channel.history(limit=limit).flatten()
                message_data = [
                    {
                        "id": str(msg.id),
                        "content": msg.content,
                        "author": str(msg.author),
                        "timestamp": str(msg.created_at),
                        "attachments": [{"filename": a.filename, "url": a.url} for a in msg.attachments],
                        "embeds": [e.to_dict() for e in msg.embeds]
                    }
                    for msg in messages
                ]
            else:
                message_data = None
            await self.client.close()
            return message_data

        messages = await self._run_coroutine(_fetch_messages())
        if messages is not None:
            return {"success": True, "messages": messages}
        else:
            return {"success": False, "error": f"Channel with ID {channel_id} is not a text channel or not found."}

    async def send_message(self, ctx: RunContext[Dict], channel_id: str, content: str) -> Dict[str, Any]:
        """
        Sends a message to a specific channel.

        Example call: send_message(channel_id=1234567890, content="Hello, world!")
        
        Args:
            ctx: The run context
            channel_id (str): The ID of the channel to send the message to
            content (str): The content of the message to send
        Returns:
            Dict[str, Any]: Information about the sent message
        """
        async def _send_message():
            await self.client.login(self.bot_token)
            channel = self.client.get_channel(int(channel_id))
            if isinstance(channel, discord.TextChannel):
                message = await channel.send(content)
                result = {
                    "id": str(message.id),
                    "content": message.content,
                    "author": str(message.author),
                    "timestamp": str(message.created_at)
                }
            else:
                result = None
            await self.client.close()
            return result

        sent_message = await self._run_coroutine(_send_message())
        if sent_message:
            return {"success": True, "message": sent_message}
        else:
            return {"success": False, "error": f"Channel with ID {channel_id} is not a text channel or not found."}

    @property
    def tools(self) -> List:
        """Returns the list of available tool functions."""
        return [
            self.list_guilds_and_channels,
            self.get_guild_info,
            self.fetch_messages,
            self.send_message
        ] 