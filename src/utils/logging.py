import os
import logging
from src.config import settings, LogLevel

class PrettyFormatter(logging.Formatter):
    """A formatter that adds colors and emojis to log messages."""

    def __init__(self):
        super().__init__()
        self.colors = {
            logging.INFO: '\033[92m',  # Green
            logging.ERROR: '\033[91m',  # Red
            logging.WARNING: '\033[93m',  # Yellow
            logging.DEBUG: '\033[94m',  # Blue
        }
        self.reset = '\033[0m'

        self.emojis = {
            logging.INFO: '📝',
            logging.ERROR: '❌',
            logging.WARNING: '⚠️',
            logging.DEBUG: '🔍',
        }

    def format(self, record):
        if not record.exc_info:
            level = record.levelno
            if level in self.colors:
                record.msg = f"{self.emojis.get(level, '')} {self.colors[level]}{record.msg}{self.reset}"
        return super().format(record)

def get_log_level(level: LogLevel) -> int:
    """Convert LogLevel enum to logging level."""
    log_levels = {
        LogLevel.DEBUG: logging.DEBUG,
        LogLevel.INFO: logging.INFO,
        LogLevel.WARNING: logging.WARNING,
        LogLevel.ERROR: logging.ERROR,
        LogLevel.CRITICAL: logging.CRITICAL
    }
    return log_levels[level]

def configure_logging():
    """Configure logging with pretty formatting and proper log level."""
    # Get log level from settings
    log_level = get_log_level(settings.AM_LOG_LEVEL)
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    # Remove existing handlers
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    # Create and configure stream handler
    handler = logging.StreamHandler()
    handler.setFormatter(PrettyFormatter())
    root_logger.addHandler(handler)

    # Configure Logfire if token is present
    if settings.LOGFIRE_TOKEN:
        try:
            import logfire
            os.environ["LOGFIRE_TOKEN"] = settings.LOGFIRE_TOKEN
            logfire.configure()  # Logfire reads token from environment
        except Exception as e:
            print(f"Warning: Failed to configure Logfire: {str(e)}")
    elif not settings.LOGFIRE_IGNORE_NO_CONFIG:
        print("Warning: LOGFIRE_TOKEN is not set. Tracing will be disabled.")

    # Disable httpx logging unless in DEBUG mode
    if log_level > logging.DEBUG:
        logging.getLogger('httpx').setLevel(logging.WARNING)
