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

    # Get the LOGFIRE_TOKEN
    LOGFIRE_TOKEN = os.getenv("LOGFIRE_TOKEN")
    if not LOGFIRE_TOKEN:
        print("Warning: LOGFIRE_TOKEN is not set. Tracing will be disabled.")

    # Set environment variables
    os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
    if LOGFIRE_TOKEN:
        os.environ["LOGFIRE_TOKEN"] = LOGFIRE_TOKEN
    else:
        # Suppress Logfire warning if no token
        os.environ["LOGFIRE_IGNORE_NO_CONFIG"] = "1"

    print(f"OPENAI_API_KEY set: {OPENAI_API_KEY[:5]}...{OPENAI_API_KEY[-5:]}")
    if LOGFIRE_TOKEN:
        print(f"LOGFIRE_TOKEN set: {LOGFIRE_TOKEN[:5]}...{LOGFIRE_TOKEN[-5:]}")

    return {
        "OPENAI_API_KEY": OPENAI_API_KEY,
        "LOGFIRE_TOKEN": LOGFIRE_TOKEN,
    }

# Explicitly export the init_config function
init_config = init_config 