"""Gmail API provider implementation.

This module provides the API client implementation for interacting with the Gmail API.
"""
import base64
import json
import logging
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, List, Any, Optional

import google.auth.transport.requests
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow

from .schema import SendEmailInput, SendEmailResult

logger = logging.getLogger(__name__)

# Gmail API scopes
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

class GmailProvider:
    """Client for interacting with the Gmail API."""

    def __init__(self, credentials_path: Optional[str] = None, token_path: Optional[str] = None):
        """Initialize the Gmail API client.
        
        Args:
            credentials_path: Path to OAuth credentials JSON file
            token_path: Path to OAuth token file
        """
        self.credentials_path = credentials_path or os.environ.get('GOOGLE_CREDENTIAL_FILE')
        self.token_path = token_path or os.path.join('credentials', 'gmail_token.json')
        self.credentials = None
        logger.info(f"Initialized GmailProvider with credentials path: {self.credentials_path}")
    
    def _get_credentials(self):
        """Get or refresh OAuth credentials.
        
        Returns:
            Google OAuth credentials
        """
        creds = None
        # The file token.json stores the user's access and refresh tokens
        if os.path.exists(self.token_path):
            try:
                creds = Credentials.from_authorized_user_info(
                    json.load(open(self.token_path)), SCOPES
                )
            except Exception as e:
                logger.error(f"Error loading credentials from token file: {str(e)}")
        
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(google.auth.transport.requests.Request())
                except Exception as e:
                    logger.error(f"Error refreshing credentials: {str(e)}")
                    creds = None
            
            if not creds:
                try:
                    # Ensure directory exists
                    os.makedirs(os.path.dirname(self.token_path), exist_ok=True)
                    
                    flow = InstalledAppFlow.from_client_secrets_file(
                        self.credentials_path, SCOPES
                    )
                    creds = flow.run_local_server(port=0)
                    
                    # Save the credentials for the next run
                    with open(self.token_path, 'w') as token:
                        token.write(creds.to_json())
                    logger.info(f"Saved new credentials to {self.token_path}")
                except Exception as e:
                    logger.error(f"Error obtaining new credentials: {str(e)}")
                    return None
        
        self.credentials = creds
        return creds
    
    def _check_auth(self) -> Dict[str, Any]:
        """Check if authentication is available and get credentials.
        
        Returns:
            Dictionary with auth status information
        """
        if not self.credentials_path or not os.path.exists(self.credentials_path):
            return {"authenticated": False, "error": f"Credentials file not found: {self.credentials_path}"}
        
        credentials = self._get_credentials()
        if not credentials:
            return {"authenticated": False, "error": "Failed to authenticate with Google"}
            
        return {"authenticated": True, "credentials": credentials}
    
    def _create_message(self, input: SendEmailInput) -> dict:
        """Create a message for an email.
        
        Args:
            input: Email input parameters
            
        Returns:
            Raw message dictionary ready for Gmail API
        """
        # Determine if we're sending HTML or plain text
        is_html = input.content_type and "html" in input.content_type.lower()
        
        # Combine message with extra content if provided
        full_message = input.message
        if input.extra_content:
            if is_html:
                full_message = f"{input.message}<br><br>{input.extra_content}"
            else:
                full_message = f"{input.message}\n\n{input.extra_content}"
        
        # For HTML emails with plain text alternative, create multipart message
        if is_html and input.plain_text_alternative:
            message = MIMEMultipart('alternative')
            
            # Add plain text part
            text_part = MIMEText(input.plain_text_alternative, 'plain')
            message.attach(text_part)
            
            # Add HTML part
            html_part = MIMEText(full_message, 'html')
            message.attach(html_part)
        else:
            # For simple emails (HTML-only or plain text)
            subtype = 'html' if is_html else 'plain'
            message = MIMEText(full_message, subtype)
        
        message['to'] = input.to
        message['subject'] = input.subject
        
        if input.cc and len(input.cc) > 0:
            message['cc'] = ', '.join(input.cc)
            
        return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}
    
    async def send_email(self, input: SendEmailInput) -> SendEmailResult:
        """Send an email via Gmail API.
        
        Args:
            input: Email parameters
            
        Returns:
            Result of the email sending operation
        """
        logger.info(f"Sending email to: {input.to}")
        
        try:
            # Check authentication
            auth_status = self._check_auth()
            if not auth_status.get("authenticated", False):
                return SendEmailResult(
                    success=False,
                    error=auth_status.get("error", "Authentication failed")
                )
                
            # Create the email message
            message = self._create_message(input)
            
            try:
                # Create Gmail API service
                service = build('gmail', 'v1', credentials=self.credentials)
                
                # Send the email
                sent_message = service.users().messages().send(
                    userId='me', body=message
                ).execute()
                
                logger.info(f"Email sent successfully to {input.to} with ID: {sent_message['id']}")
                
                return SendEmailResult(
                    success=True,
                    message_id=sent_message['id']
                )
            except HttpError as error:
                error_msg = f"Gmail API error: {error}"
                logger.error(error_msg)
                return SendEmailResult(
                    success=False,
                    error=error_msg
                )
                
        except Exception as e:
            error_msg = f"Error sending email: {str(e)}"
            logger.error(error_msg)
            
            return SendEmailResult(
                success=False,
                error=error_msg
            ) 