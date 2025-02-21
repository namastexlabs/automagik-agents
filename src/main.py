import asyncio
import json
import logging
import os
from src.agents.simple_agent.agent import SimpleAgent, PrettyFormatter
from src.config import init_config

# Configure root logger with pretty formatting
root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)

# Remove any existing handlers
for handler in root_logger.handlers:
    root_logger.removeHandler(handler)

# Add our pretty handler
handler = logging.StreamHandler()
handler.setFormatter(PrettyFormatter())
root_logger.addHandler(handler)

# Get our module's logger
logger = logging.getLogger(__name__)

async def main():
    try:
        # Initialize config
        config = init_config()
        logger.info("Configuration initialized")

        # Ensure OPENAI_API_KEY is set in the environment
        os.environ["OPENAI_API_KEY"] = config["OPENAI_API_KEY"]
        logger.info("OPENAI_API_KEY set ✓")

        simple_agent = SimpleAgent(config)
        logger.info("SimpleAgent ready")
        
        print("\n💫 Welcome to the Simple Assistant! Type 'exit' to quit.\n")
        
        while True:
            user_input = input("\n🧑 You: ")
            
            if user_input.lower() == 'exit':
                print("\n👋 Goodbye!")
                break
            
            logger.info("Processing...")
            try:
                response = await simple_agent.process_message(user_input)
                
                if response.tool_calls:
                    logger.debug({"tool_calls": response.tool_calls})
                if response.tool_outputs:
                    logger.debug({"tool_outputs": response.tool_outputs})
                
                print(f"\n🤖 Assistant: {response.message}")
            except Exception as e:
                logger.error(f"Error: {str(e)}")
                print(f"\n🤖 Assistant: I'm sorry, but I encountered an error while processing your request.")
    except Exception as e:
        logger.error(f"Error in main loop: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main()) 