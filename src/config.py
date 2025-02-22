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
    AM_API_KEY: str = Field(..., description="API key for authenticating requests")

    # OpenAI
    OPENAI_API_KEY: str = Field(..., description="OpenAI API key for agent operations")

    # Notion (Optional)
    NOTION_TOKEN: Optional[str] = Field(None, description="Notion integration token")

    # Server
    AM_PORT: int = Field(8000, description="Port to run the server on")
    AM_HOST: str = Field("0.0.0.0", description="Host to bind the server to")
    AM_ENV: Environment = Field(Environment.DEVELOPMENT, description="Environment (development, production, testing)")

    # Logging
    AM_LOG_LEVEL: LogLevel = Field(LogLevel.INFO, description="Logging level")
    LOGFIRE_TOKEN: Optional[str] = Field(None, description="Logfire token for logging service")
    LOGFIRE_IGNORE_NO_CONFIG: bool = Field(True, description="Suppress Logfire warning if no token")

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
        print(f"├── Environment: {settings.AM_ENV}")
        print(f"├── Log Level: {settings.AM_LOG_LEVEL}")
        print(f"├── Server: {settings.AM_HOST}:{settings.AM_PORT}")
        print(f"├── OpenAI API Key: {settings.OPENAI_API_KEY[:5]}...{settings.OPENAI_API_KEY[-5:]}")
        print(f"└── API Key: {settings.AM_API_KEY[:5]}...{settings.AM_API_KEY[-5:]}")

        if settings.NOTION_TOKEN:
            print(f"    └── Notion Token: {settings.NOTION_TOKEN[:5]}...{settings.NOTION_TOKEN[-5:]}")

        return settings
    except Exception as e:
        print("❌ Error loading configuration:")
        print(f"   {str(e)}")
        raise

# Create a global settings instance
settings = load_settings()