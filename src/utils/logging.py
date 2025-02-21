"""Logging configuration for Sofia."""

import logging

class PrettyFormatter(logging.Formatter):
    """A formatter that adds color and emoji to log messages."""
    
    def format(self, record):
        # Add color based on level
        colors = {
            logging.INFO: '\033[92m',  # Green
            logging.ERROR: '\033[91m',  # Red
            logging.WARNING: '\033[93m',  # Yellow
            logging.DEBUG: '\033[94m',  # Blue
        }
        reset = '\033[0m'
        
        # Add emoji based on level
        emojis = {
            logging.INFO: '📝',
            logging.ERROR: '❌',
            logging.WARNING: '⚠️',
            logging.DEBUG: '🔍',
        }
        
        # Get color and emoji for this level
        color = colors.get(record.levelno, '')
        emoji = emojis.get(record.levelno, '')
        
        # Format with color and emoji
        return f"{color}{emoji} {record.getMessage()}{reset}"

def configure_logging():
    """Configure root logger with pretty formatting."""
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    # Remove any existing handlers
    for handler in root_logger.handlers:
        root_logger.removeHandler(handler)

    # Add our pretty handler
    handler = logging.StreamHandler()
    handler.setFormatter(PrettyFormatter())
    root_logger.addHandler(handler)

    # Disable httpx logging
    logging.getLogger('httpx').setLevel(logging.WARNING)
