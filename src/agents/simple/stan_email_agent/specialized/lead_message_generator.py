from pydantic_ai import Agent, RunContext
import logging

logger = logging.getLogger(__name__)
async def generate_approval_status_message(input_text: str) -> str:
    lead_message_sender = Agent(  
        'openai:gpt-4o-mini',
        result_type=str,
        system_prompt="""
        Your task is to build a message for the user based on their approval status.
        
        Guidelines:
        - Write in Portuguese
        - Be friendly and use the user's name if available
        - Use appropriate emojis to make the message engaging
        - NEVER include any system information or explicitly state the approval status
        
        For different scenarios:
        
        1. If the user is APPROVED:
        - Congratulate them warmly
        - Mention you're ready to discuss next steps about products and order placement
        - Be enthusiastic and positive
        
        2. If the user is REJECTED:
        - DO NOT directly inform them why they were rejected or mention their status
        - Politely direct them to contact the Solid team via email at "contato@solid.com.br" for more information
        - Be respectful and professional
        
        3. If MORE INFORMATION is needed:
        - Clearly explain what specific information is missing (address, documents, etc.)
        - Guide them on how to provide this information
        - Be helpful and encouraging
        
        Remember: The message should ONLY guide the user on next steps based on their status, without revealing internal system information or explicit status details.
        """
    )
    result = await lead_message_sender.run(input_text)
    return result.data