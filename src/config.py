import os

try:
    from dotenv import load_dotenv
except ImportError:
    print("Warning: python-dotenv is not installed. Environment variables may not be loaded from .env file.")
    load_dotenv = lambda: None

def init_config():
    # Load the .env file
    load_dotenv()

    # Get the OPENAI_API_KEY
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY is not set in the environment variables or .env file")

    # Set the OPENAI_API_KEY as an environment variable
    os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

    # Suppress Logfire warning
    os.environ["LOGFIRE_IGNORE_NO_CONFIG"] = "1"

    print(f"OPENAI_API_KEY set: {OPENAI_API_KEY[:5]}...{OPENAI_API_KEY[-5:]}")

    # You can add other configuration variables here if needed
    return {
        "OPENAI_API_KEY": OPENAI_API_KEY,
        # Add other configuration variables as needed
    }

# Explicitly export the init_config function
init_config = init_config 