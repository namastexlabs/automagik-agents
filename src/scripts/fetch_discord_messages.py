from src.tools.discord_tools import DiscordTools
import asyncio
import os

async def main():
    discord_tools = DiscordTools(os.environ['DISCORD_BOT_TOKEN'])
    
    # List guilds and channels
    guilds_and_channels = await discord_tools.list_guilds_and_channels({})
    print('Guilds and Channels:', guilds_and_channels)
    
    # Assuming we found the channel ID for #QA in Namastex Labs
    qa_channel_id = '1283102887727202375'  # Replace with actual channel ID
    
    # Fetch messages
    messages = await discord_tools.fetch_messages({}, channel_id=qa_channel_id, limit=10)
    print('Recent messages:', messages)

if __name__ == "__main__":
    asyncio.run(main()) 