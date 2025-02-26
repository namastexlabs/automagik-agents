"""Main entry point for the application when run as a module.

This allows running the Sofia application with:
    python -m src
"""

import sys
import logging
from importlib import import_module

# Import necessary modules for logging configuration
try:
    from src.utils.logging import configure_logging
    from src.config import settings
    
    # Configure logging before anything else
    configure_logging()
    
    # Get our module's logger
    logger = logging.getLogger(__name__)
except ImportError as e:
    print(f"Error importing core modules: {e}")
    sys.exit(1)

def main():
    """Run the Sofia application."""
    try:
        # Log startup message
        logger.info("Starting Sofia application via 'python -m src'")
        
        # Check if application is being run directly
        if len(sys.argv) > 1:
            # If arguments are passed, use them with the main module's argument parser
            import argparse
            
            # Create argument parser (duplicating what's in main.py)
            parser = argparse.ArgumentParser(description="Run the Sofia application server")
            parser.add_argument(
                "--reload", 
                action="store_true", 
                default=False,
                help="Enable auto-reload for development (default: False)"
            )
            parser.add_argument(
                "--host", 
                type=str, 
                default=settings.AM_HOST,
                help=f"Host to bind the server to (default: {settings.AM_HOST})"
            )
            parser.add_argument(
                "--port", 
                type=int, 
                default=int(settings.AM_PORT),
                help=f"Port to bind the server to (default: {settings.AM_PORT})"
            )
            
            # Parse arguments
            args = parser.parse_args()
            
            # Log the configuration
            logger.info("Starting server with configuration:")
            logger.info(f"├── Host: {args.host}")
            logger.info(f"├── Port: {args.port}")
            logger.info(f"└── Auto-reload: {'Enabled' if args.reload else 'Disabled'}")
            
            # Run the server with the provided arguments
            import uvicorn
            uvicorn.run(
                "src.main:app",
                host=args.host,
                port=args.port,
                reload=args.reload
            )
        else:
            # If no arguments are passed, run with default settings
            import uvicorn
            
            # Log the default configuration
            logger.info("Starting server with default configuration:")
            logger.info(f"├── Host: {settings.AM_HOST}")
            logger.info(f"├── Port: {settings.AM_PORT}")
            logger.info(f"└── Auto-reload: Disabled")
            
            uvicorn.run(
                "src.main:app",
                host=settings.AM_HOST,
                port=int(settings.AM_PORT),
                reload=False
            )
    except Exception as e:
        logger.error(f"Error running application: {str(e)}")
        # Print traceback for easier debugging
        import traceback
        logger.error(traceback.format_exc())
        sys.exit(1)

if __name__ == "__main__":
    main() 