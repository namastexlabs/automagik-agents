from typing import Dict, Optional, Any
import os
import logging
import traceback

# Setup logging first
logger = logging.getLogger(__name__)

# Import pydantic-ai classes with error handling
try:
    from pydantic_ai.usage import UsageLimits
    from pydantic_ai.settings import ModelSettings
    PYDANTIC_AI_AVAILABLE = True
    logger.info("PydanticAI successfully imported")
except ImportError as e:
    PYDANTIC_AI_AVAILABLE = False
    # Create placeholder classes if imports fail
    class UsageLimits:
        def __init__(self, **kwargs):
            pass
    
    class ModelSettings:
        def __init__(self, **kwargs):
            pass
    
    logger.error(f"Failed to import PydanticAI: {str(e)}")

# Simple placeholder definition
class PlaceholderAgent:
    """Placeholder agent implementation for fallback."""
    
    def __init__(self, config):
        self.name = config.get("name", "placeholder")
        logger.info(f"Created PlaceholderAgent with name: {self.name}")

# Define the create_simple_agent function - will be updated if imports succeed
def create_simple_agent(config: Optional[Dict[str, str]] = None) -> Any:
    """Create a simple agent instance.
    
    Args:
        config: Optional configuration overrides
        
    Returns:
        An agent instance
    """
    logger.info(f"Called create_simple_agent function (fallback implementation)")
    # Return a placeholder that won't crash
    return PlaceholderAgent(config or {"name": "simple_agent_fallback"})

# Import agent class and try to define a proper implementation
try:
    from src.agents.simple.simple_agent.agent import SimpleAgent
    from src.agents.models.dependencies import SimpleAgentDependencies
    from src.agents.models.placeholder import PlaceholderAgent
    from src.config import settings
    
    logger.info("Successfully imported SimpleAgent dependencies")
    
    # Redefine the create_simple_agent function with the proper implementation
    def create_simple_agent(config: Optional[Dict[str, str]] = None) -> Any:
        """Create and initialize a SimpleAgent instance.
        
        Args:
            config: Optional configuration override
            
        Returns:
            Initialized SimpleAgent instance
        """
        logger.info("Creating SimpleAgent with PydanticAI available: " + str(PYDANTIC_AI_AVAILABLE))
        
        default_config = {
            "model": "openai:gpt-4o-mini",  # Default model
            "system_prompt": "You are a helpful assistant that provides accurate and concise information.",
            "retries": "3"
        }
        
        # Check for environment variables
        if os.environ.get("OPENAI_API_KEY"):
            default_config["openai_api_key"] = os.environ.get("OPENAI_API_KEY")
            
        if os.environ.get("TAVILY_API_KEY"):
            default_config["tavily_api_key"] = os.environ.get("TAVILY_API_KEY")
        
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
    
    # Create standard agent instances with safe error handling
    
    # Default instance with conservative usage limits
    try:
        logger.info("Creating default_agent instance")
        default_agent = create_simple_agent({
            "response_tokens_limit": "4000",  # Reasonable token limit for responses
            "request_limit": "5"              # Limit number of API requests
        })
        logger.info(f"default_agent created successfully: {default_agent}")
    except Exception as e:
        logger.error(f"Failed to create default_agent: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        default_agent = PlaceholderAgent({"name": "simple_agent"})
        logger.info(f"Created placeholder agent as fallback: {default_agent}")
    
    # Create an enhanced instance with search capabilities and higher limits
    try:
        search_agent = create_simple_agent({
            "enable_search": "true",
            "tavily_api_key": os.environ.get("TAVILY_API_KEY", ""),
            "response_tokens_limit": "8000",  # Higher limit for search responses
            "request_limit": "10",            # More requests allowed for search operations
            "model_settings.temperature": "0.7",  # Slightly creative responses
            "model_settings.timeout": "60"        # Longer timeout for search operations
        })
        logger.info(f"search_agent created successfully: {search_agent}")
    except Exception as e:
        logger.warning(f"Could not initialize search_agent: {str(e)}")
        logger.warning(f"Traceback: {traceback.format_exc()}")
        search_agent = PlaceholderAgent({"name": "search_agent"})
    
    # Create a streaming-optimized agent
    try:
        streaming_agent = create_simple_agent({
            "model_settings.temperature": "0.2",  # More factual responses for streaming
            "model_settings.timeout": "30"        # Standard timeout
        })
        logger.info(f"streaming_agent created successfully: {streaming_agent}")
    except Exception as e:
        logger.warning(f"Could not initialize streaming_agent: {str(e)}")
        logger.warning(f"Traceback: {traceback.format_exc()}")
        streaming_agent = PlaceholderAgent({"name": "streaming_agent"})

except Exception as e:
    logger.error(f"Failed to initialize SimpleAgent module: {str(e)}")
    logger.error(f"Traceback: {traceback.format_exc()}")
    # Make sure SimpleAgent is defined to avoid 'SimpleAgent = None' issue
    class SimpleAgent:
        """Placeholder for when real SimpleAgent can't be imported."""
        def __init__(self, config):
            logger.error("Using placeholder SimpleAgent class - real implementation failed to import")
    
    # Default agent instances use the fallback implementation of create_simple_agent
    default_agent = create_simple_agent({"name": "default_agent_fallback"})
    search_agent = create_simple_agent({"name": "search_agent_fallback"})
    streaming_agent = create_simple_agent({"name": "streaming_agent_fallback"}) 