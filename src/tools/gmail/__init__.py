"""Gmail tools for Automagik Agents.

Provides tools for sending emails via Gmail API.
"""

# Import from tool module
from src.tools.gmail.tool import (
    send_email,
    get_send_email_description
)

# Import schema models
from src.tools.gmail.schema import (
    SendEmailInput,
    SendEmailResult
)

# Import interface
from src.tools.gmail.interface import (
    GmailTools,
    gmail_tools
)

# Export public API
__all__ = [
    # Tool functions
    'send_email',
    
    # Description functions
    'get_send_email_description',
    
    # Schema models
    'SendEmailInput',
    'SendEmailResult',
    
    # Interface
    'GmailTools',
    'gmail_tools'
] 