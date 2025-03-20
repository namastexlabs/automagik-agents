"""Discord tool implementation.

This module provides the core functionality for Discord tools.
"""
import logging
from typing import List, Optional, Dict, Any, Callable, Awaitable
import discord
import asyncio
from pydantic_ai import RunContext

from .schema import (
    DiscordChannel, DiscordGuild, DiscordMessage, DiscordResponse,
    ListGuildsResponse, GuildInfoResponse, FetchMessagesResponse, SendMessageResponse
)

logger = logging.getLogger(__name__)

class DiscordError(Exception):
    """Base exception for Discord API errors."""
    pass

def get_list_guilds_description() -> str:
    """Get description for the list_guilds_and_channels function."""
    return "Lists all guilds and channels the bot has access to."

def get_guild_info_description() -> str:
    """Get description for the get_guild_info function."""
    return "Retrieves information about a specific guild."

def get_fetch_messages_description() -> str:
    """Get description for the fetch_messages function."""
    return "Fetches messages from a specific channel."

def get_send_message_description() -> str:
    """Get description for the send_message function."""
    return "Sends a message to a specific channel."

async def _with_temp_client(bot_token: str, func: Callable[[discord.Client], Awaitable[Any]]) -> Any:
    """
    Helper function to create a temporary Discord client, perform an operation, then close the client.
    
    Args:
        bot_token: Discord bot token
        func: Async function to execute with the client
        
    Returns:
        Result of the function execution
    """
    client = discord.Client(intents=discord.Intents.default())
    ready_event = asyncio.Event()

    @client.event
    async def on_ready():
        ready_event.set()

    await client.login(bot_token)
    # Start the client in the background
    client_task = asyncio.create_task(client.connect())
    # Wait until the client signals it is ready
    await ready_event.wait()
    # Optional delay to ensure connection stability and guild population
    await asyncio.sleep(2)
    
    try:
        result = await func(client)
    finally:
        await client.close()
        await client_task
    
    return result

async def list_guilds_and_channels(ctx: RunContext[Dict], bot_token: str) -> Dict[str, Any]:
    """
    Lists all guilds and channels the bot has access to.
    
    Args:
        ctx: The run context
        bot_token: Discord bot token
        
    Returns:
        Dict with the guild and channel information
    """
    try:
        logger.info("Listing Discord guilds and channels")
        
        async def _list(client: discord.Client):
            guilds_info = []
            for guild in client.guilds:
                channels_info = [
                    {"name": channel.name, "id": str(channel.id), "type": str(channel.type)}
                    for channel in guild.channels
                ]
                guilds_info.append({
                    "name": guild.name,
                    "id": str(guild.id),
                    "channels": channels_info
                })
            return guilds_info

        guilds_info = await _with_temp_client(bot_token, _list)
        response = ListGuildsResponse(success=True, guilds=guilds_info)
        return response.dict()
    except Exception as e:
        logger.error(f"Error listing Discord guilds: {str(e)}")
        response = ListGuildsResponse(success=False, error=f"Error: {str(e)}")
        return response.dict()

async def get_guild_info(ctx: RunContext[Dict], bot_token: str, guild_id: str) -> Dict[str, Any]:
    """
    Retrieves information about a specific guild.
    
    Args:
        ctx: The run context
        bot_token: Discord bot token
        guild_id: ID of the guild to retrieve information for
        
    Returns:
        Dict with the guild information
    """
    try:
        logger.info(f"Getting information for Discord guild ID: {guild_id}")
        
        async def _get(client: discord.Client):
            guild = client.get_guild(int(guild_id))
            if guild:
                info = {
                    "name": guild.name,
                    "id": str(guild.id),
                    "member_count": guild.member_count,
                    "channels": [{"name": channel.name, "id": str(channel.id), "type": str(channel.type)} for channel in guild.channels]
                }
            else:
                info = None
            return info

        guild_info = await _with_temp_client(bot_token, _get)
        if guild_info:
            response = GuildInfoResponse(success=True, guild_info=guild_info)
        else:
            response = GuildInfoResponse(success=False, error=f"Guild with ID {guild_id} not found.")
        return response.dict()
    except Exception as e:
        logger.error(f"Error getting Discord guild info: {str(e)}")
        response = GuildInfoResponse(success=False, error=f"Error: {str(e)}")
        return response.dict()

async def fetch_messages(ctx: RunContext[Dict], bot_token: str, channel_id: str, limit: int = 100) -> Dict[str, Any]:
    """
    Fetches messages from a specific channel.
    
    Args:
        ctx: The run context
        bot_token: Discord bot token
        channel_id: ID of the channel to fetch messages from
        limit: Maximum number of messages to retrieve
        
    Returns:
        Dict with the fetched messages
    """
    try:
        logger.info(f"Fetching messages from Discord channel ID: {channel_id}, limit: {limit}")
        
        async def _fetch(client: discord.Client):
            channel = client.get_channel(int(channel_id))
            if isinstance(channel, discord.TextChannel):
                messages = []
                async for msg in channel.history(limit=limit):
                    messages.append(msg)
                message_data = [
                    {
                        "id": str(msg.id),
                        "content": msg.content,
                        "author": str(msg.author),
                        "timestamp": str(msg.created_at),
                        "attachments": [{"filename": a.filename, "url": a.url} for a in msg.attachments],
                        "embeds": [e.to_dict() for e in msg.embeds],
                        "type": str(msg.type),
                        "reference": {
                            "message_id": str(msg.reference.message_id),
                            "channel_id": str(msg.reference.channel_id),
                            "guild_id": str(msg.reference.guild_id)
                        } if msg.reference else None
                    }
                    for msg in messages
                ]
            else:
                message_data = None
            return message_data

        messages = await _with_temp_client(bot_token, _fetch)
        if messages is not None:
            response = FetchMessagesResponse(success=True, messages=messages)
        else:
            response = FetchMessagesResponse(success=False, error=f"Channel with ID {channel_id} is not a text channel or not found.")
        return response.dict()
    except Exception as e:
        logger.error(f"Error fetching Discord messages: {str(e)}")
        response = FetchMessagesResponse(success=False, error=f"Error: {str(e)}")
        return response.dict()

async def send_message(ctx: RunContext[Dict], bot_token: str, channel_id: str, content: str) -> Dict[str, Any]:
    """
    Sends a message to a specific channel.
    
    Args:
        ctx: The run context
        bot_token: Discord bot token
        channel_id: ID of the channel to send the message to
        content: Content of the message to send
        
    Returns:
        Dict with information about the sent message
    """
    try:
        logger.info(f"Sending message to Discord channel ID: {channel_id}")
        
        async def _send(client: discord.Client):
            channel = client.get_channel(int(channel_id))
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
            return result

        sent_message = await _with_temp_client(bot_token, _send)
        if sent_message:
            response = SendMessageResponse(success=True, message=sent_message)
        else:
            response = SendMessageResponse(success=False, error=f"Channel with ID {channel_id} is not a text channel or not found.")
        return response.dict()
    except Exception as e:
        logger.error(f"Error sending Discord message: {str(e)}")
        response = SendMessageResponse(success=False, error=f"Error: {str(e)}")
        return response.dict() 