"""Test configuration for pytest."""
import os
from pathlib import Path
from dotenv import load_dotenv

# Get the project root directory
project_root = Path(__file__).parent.parent

# Load environment variables from .env file
env_path = project_root / '.env'
load_dotenv(env_path)

# Verify OMIE credentials are loaded
if not os.getenv("OMIE_APP_KEY") or not os.getenv("OMIE_APP_SECRET"):
    print("Warning: OMIE credentials not found in .env file") 