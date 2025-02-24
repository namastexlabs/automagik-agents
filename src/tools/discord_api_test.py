import discord
from discord.ext import commands
import asyncio
from src.config import settings
from datetime import datetime, timedelta
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

async def list_guilds_and_channels():
    guilds_info = []
    for guild in bot.guilds:
        channels_info = [{"name": channel.name, "id": channel.id, "type": str(channel.type)} for channel in guild.channels]
        guilds_info.append({
            "name": guild.name,
            "id": guild.id,
            "channels": channels_info
        })
    return guilds_info

async def fetch_messages(guild_id: int = None, channel_id: int = None, limit: int = 100, days: int = 10, simplified: bool = True, content_filter: str = None):
    if guild_id:
        guild = bot.get_guild(guild_id)
        if not guild:
            logger.error(f"Error: Guild with ID {guild_id} not found.")
            return []
        channels = guild.text_channels
    elif channel_id:
        channel = bot.get_channel(channel_id)
        if not channel:
            logger.error(f"Error: Channel with ID {channel_id} not found.")
            return []
        if not isinstance(channel, discord.TextChannel):
            logger.error(f"Error: Channel with ID {channel_id} is not a text channel.")
            return []
        channels = [channel]
    else:
        logger.error("Error: Either guild_id or channel_id must be provided.")
        return []

    cutoff_date = datetime.utcnow() - timedelta(days=days)
    all_messages = []

    for channel in channels:
        try:
            async for message in channel.history(limit=limit, after=cutoff_date):
                if content_filter and content_filter.lower() not in message.content.lower():
                    continue
                
                thread_id = message.thread.id if message.thread else None
                
                if simplified:
                    msg_data = {
                        "id": message.id,
                        "content": message.content[:100] + "..." if len(message.content) > 100 else message.content,
                        "author": str(message.author),
                        "timestamp": str(message.created_at),
                        "channel_id": channel.id,
                        "thread_id": thread_id
                    }
                else:
                    msg_data = {
                        "id": message.id,
                        "content": message.content,
                        "author": str(message.author),
                        "timestamp": str(message.created_at),
                        "channel_id": channel.id,
                        "thread_id": thread_id,
                        "attachments": [{"filename": a.filename, "url": a.url} for a in message.attachments],
                        "embeds": [e.to_dict() for e in message.embeds],
                        "reactions": [{"emoji": str(r.emoji), "count": r.count} for r in message.reactions]
                    }
                
                all_messages.append(msg_data)
                
                if len(all_messages) >= limit:
                    break
            
            if len(all_messages) >= limit:
                break
        
        except discord.errors.Forbidden:
            logger.error(f"Error: Bot doesn't have permission to read messages in channel {channel.id}")
        except Exception as e:
            logger.exception(f"Error fetching messages from channel {channel.id}: {str(e)}")

    return all_messages

async def get_guild_info(guild_id: int):
    guild = bot.get_guild(guild_id)
    if guild:
        return {
            "name": guild.name,
            "id": guild.id,
            "member_count": guild.member_count,
            "channels": [{"name": channel.name, "id": channel.id, "type": str(channel.type)} for channel in guild.channels]
        }
    else:
        logger.error(f"Guild with ID {guild_id} not found.")
        return None

@bot.event
async def on_ready():
    try:
        print(f'Logged in as {bot.user.name} (ID: {bot.user.id})')
        print('------')

        # List all guilds and channels
        guilds_and_channels = await list_guilds_and_channels()
        print("Guilds and Channels:")
        for guild in guilds_and_channels:
            print(f"- {guild['name']} (ID: {guild['id']})")
            for channel in guild['channels']:
                print(f"  - {channel['name']} (ID: {channel['id']}, Type: {channel['type']})")

        # Test the fetch_messages function
        test_guild_id = 1095114867012292758  # Namastex Labs guild ID
        test_channel_id = 1283102887727202375  # qa channel ID
        
        print(f"\nFetching messages from guild {test_guild_id}:")
        guild_messages = await fetch_messages(guild_id=test_guild_id, limit=50, days=5, simplified=True, content_filter="test")
        for msg in guild_messages:
            print(f"{msg['author']} - {msg['timestamp']} (Channel: {msg['channel_id']}): {msg['content']}")

        print(f"\nFetching messages from channel {test_channel_id}:")
        channel_messages = await fetch_messages(channel_id=test_channel_id, limit=20, days=3, simplified=False)
        for msg in channel_messages:
            print(f"{msg['author']} - {msg['timestamp']}: {msg['content'][:50]}... (Attachments: {len(msg['attachments'])}, Embeds: {len(msg['embeds'])}, Reactions: {len(msg['reactions'])})")

    except Exception as e:
        logger.exception(f"An error occurred during execution: {e}")
    finally:
        # Signal that we're done with our tasks
        print("Finished fetching messages. Closing the bot...")
        await bot.close()

async def main():
    try:
        await bot.start(settings.DISCORD_BOT_TOKEN)
    except Exception as e:
        logger.exception(f"An error occurred while starting the bot: {e}")
    finally:
        # Ensure the bot is properly closed
        if not bot.is_closed():
            await bot.close()
        # Close the aiohttp session
        await bot.http.close()
        await bot.http._HTTPClient__session.close()

if __name__ == "__main__":
    asyncio.run(main()) 