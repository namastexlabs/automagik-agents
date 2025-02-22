import os
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings

try:
    from dotenv import load_dotenv
except ImportError:
    print("Warning: python-dotenv is not installed. Environment variables may not be loaded from .env file.")
    load_dotenv = lambda: None

class LogLevel(str, Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"

class Environment(str, Enum):
    DEVELOPMENT = "development"
    PRODUCTION = "production"
    TESTING = "testing"

class Settings(BaseSettings):
    # Authentication
    AUTOMAGIK_AGENTS_API_KEY: str = Field(..., description="API key for authenticating requests")

    # OpenAI
    AUTOMAGIK_AGENTS_OPENAI_API_KEY: str = Field(..., description="OpenAI API key for agent operations")

    # Notion (Optional)
    AUTOMAGIK_AGENTS_NOTION_TOKEN: Optional[str] = Field(None, description="Notion integration token")

    # Server
    AUTOMAGIK_AGENTS_PORT: int = Field(8000, description="Port to run the server on")
    AUTOMAGIK_AGENTS_HOST: str = Field("0.0.0.0", description="Host to bind the server to")
    AUTOMAGIK_AGENTS_ENV: Environment = Field(Environment.DEVELOPMENT, description="Environment (development, production, testing)")

    # Logging
    AUTOMAGIK_AGENTS_LOG_LEVEL: LogLevel = Field(LogLevel.INFO, description="Logging level")
    AUTOMAGIK_AGENTS_LOGFIRE_TOKEN: Optional[str] = Field(None, description="Logfire token for logging service")
    AUTOMAGIK_AGENTS_LOGFIRE_IGNORE_NO_CONFIG: bool = Field(True, description="Suppress Logfire warning if no token")

    class Config:
        env_file = ".env"
        case_sensitive = True

def load_settings() -> Settings:
    """Load and validate settings from environment variables and .env file."""
    # Load environment variables from .env file
    load_dotenv()

    try:
        settings = Settings()
        
        # Print configuration info
        print("🔧 Configuration loaded:")
        print(f"├── Environment: {settings.AUTOMAGIK_AGENTS_ENV}")
        print(f"├── Log Level: {settings.AUTOMAGIK_AGENTS_LOG_LEVEL}")
        print(f"├── Server: {settings.AUTOMAGIK_AGENTS_HOST}:{settings.AUTOMAGIK_AGENTS_PORT}")
        print(f"├── OpenAI API Key: {settings.AUTOMAGIK_AGENTS_OPENAI_API_KEY[:5]}...{settings.AUTOMAGIK_AGENTS_OPENAI_API_KEY[-5:]}")
        print(f"└── API Key: {settings.AUTOMAGIK_AGENTS_API_KEY[:5]}...{settings.AUTOMAGIK_AGENTS_API_KEY[-5:]}")

        if settings.AUTOMAGIK_AGENTS_NOTION_TOKEN:
            print(f"    └── Notion Token: {settings.AUTOMAGIK_AGENTS_NOTION_TOKEN[:5]}...{settings.AUTOMAGIK_AGENTS_NOTION_TOKEN[-5:]}")

        return settings
    except Exception as e:
        print("❌ Error loading configuration:")
        print(f"   {str(e)}")
        raise

# Create a global settings instance
settings = load_settings()