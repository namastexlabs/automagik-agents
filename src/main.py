import asyncio
import logging
import os
from typing import Dict, Type

import logfire
from src.agents.simple_agent.agent import SimpleAgent
from src.agents.notion_agent.agent import NotionAgent
from src.config import init_config
from src.utils.logging import configure_logging

# Configure logging
configure_logging()

# Get our module's logger
logger = logging.getLogger(__name__)

# Available agents
AGENTS: Dict[str, Type] = {
    "simple": SimpleAgent,
    "notion": NotionAgent
}

def print_agent_menu():
    """Print the available agents menu."""
    print("\n🤖 Available Agents:")
    for idx, (key, agent_class) in enumerate(AGENTS.items(), 1):
        print(f"{idx}. {agent_class.__name__}")
    print("\nType 'switch' to change agents, 'exit' to quit.")

async def main():
    try:
        # Initialize config
        config = init_config()
        logger.info("Configuration initialized")
        
        # Configure logfire if token is present
        if config.get("LOGFIRE_TOKEN"):
            logfire.configure(
                send_to_logfire='if-token-present',
                service_name="sofia-agent",
                service_version="0.1.0"
            )
            logger.info("Logfire configured ✓")

        # Ensure OPENAI_API_KEY is set in the environment
        os.environ["OPENAI_API_KEY"] = config["OPENAI_API_KEY"]
        logger.info("OPENAI_API_KEY set ✓")

        print("\n💫 Welcome to SOFIA! Please choose an agent:")
        
        current_agent = None
        while True:
            if current_agent is None:
                print_agent_menu()
                choice = input("\n🎯 Choose an agent (1-{0}): ".format(len(AGENTS)))
                try:
                    idx = int(choice) - 1
                    if 0 <= idx < len(AGENTS):
                        agent_key = list(AGENTS.keys())[idx]
                        agent_class = AGENTS[agent_key]
                        current_agent = agent_class(config)
                        logger.info(f"{agent_class.__name__} ready")
                        continue
                except ValueError:
                    pass
                print("\n❌ Invalid choice. Please try again.")
                continue

            user_input = input("\n🧑 You: ")
            if user_input.lower() == "exit":
                print("\n👋 Goodbye!")
                break
            elif user_input.lower() == "switch":
                current_agent = None
                continue
                
            logger.info("Processing...")
            try:
                response = await current_agent.process_message(user_input)
                
                if response.message:
                    print(f"\n🤖 Assistant: {response.message}")
                else:
                    logger.error("No response message received")
                    print(f"🤖 Assistant: I'm sorry, but I couldn't generate a proper response.")
            except Exception as e:
                logger.error(f"Error processing message: {str(e)}")
                print(f"🤖 Assistant: I'm sorry, but I encountered an error while processing your request.")
    except KeyboardInterrupt:
        pass
    except Exception as e:
        logger.error(f"Error in main loop: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())
