from typing import Dict, Optional, Any
import os
import logging
import traceback

from src.agents.simple.simple_agent.prompts.prompt import SIMPLE_AGENT_PROMPT

# Setup logging first
logger = logging.getLogger(__name__)


try:
    from src.agents.simple.simple_agent.agent import SimpleAgent
    from src.agents.models.placeholder import PlaceholderAgent
    
    # Standardized create_agent function
    def create_agent(config: Optional[Dict[str, str]] = None) -> Any:
        """Create and initialize a SimpleAgent instance.
        
        Args:
            config: Optional configuration override
            
        Returns:
            Initialized SimpleAgent instance
        """
        logger.info("Creating SimpleAgent with PydanticAI ")
        
        default_config = {
            "model": "openai:gpt-4o-mini",  
            "retries": "3"
        }
        
        # Check for environment variables
        if os.environ.get("OPENAI_API_KEY"):
            default_config["openai_api_key"] = os.environ.get("OPENAI_API_KEY")
         
        # Apply user config overrides
        if config:
            default_config.update(config)
        
        # Initialize the agent
        try:
            logger.info(f"Initializing SimpleAgent with config: {default_config}")
            agent = SimpleAgent(default_config)
            logger.info(f"SimpleAgent initialized successfully: {agent}")
            return agent
        except Exception as e:
            logger.error(f"Failed to initialize SimpleAgent: {str(e)}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            return PlaceholderAgent({"name": "simple_agent_error", "error": str(e)})
    
except Exception as e:
    logger.error(f"Failed to initialize SimpleAgent module: {str(e)}")
    logger.error(f"Traceback: {traceback.format_exc()}")
    