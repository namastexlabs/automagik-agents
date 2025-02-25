import logging
from datetime import datetime
from typing import List

from fastapi import APIRouter, HTTPException
from src.agents.models.agent_factory import AgentFactory
from src.config import settings
from src.memory.message_history import MessageHistory
from src.api.models import (
    AgentRunRequest,
    AgentInfo,
    DeleteSessionResponse,
    MessageModel,
    SessionResponse
)

# Create API router for v1 endpoints
router = APIRouter()

# Get our module's logger
logger = logging.getLogger(__name__)

@router.get("/agent/list", response_model=List[AgentInfo])
async def list_agents():
    """List all available agents."""
    return [
        AgentInfo(name=name, type=AgentFactory._agents[name][0].__name__)
        for name in AgentFactory.list_available_agents()
    ]

@router.post("/agent/{agent_name}/run")
async def run_agent(agent_name: str, request: AgentRunRequest):
    """Run an agent with the given name."""
    try:
        agent = AgentFactory.get_agent(agent_name)
        
        # Get message history
        message_history = MessageHistory(request.session_id) if request.session_id else None
        
        if message_history and message_history.messages:
            # Get filtered messages up to the limit
            filtered_messages = message_history.get_filtered_messages(
                message_limit=request.message_limit,
                sort_desc=False  # Sort chronologically for agent processing
            )
            message_history.update_messages(filtered_messages)

        response = await agent.process_message(
            request.message_input,
            session_id=request.session_id
        )
        
        # Log the tool call and output counts
        tool_call_count = len(response.history.get('messages', [])[-1].get('tool_calls', []))
        tool_output_count = len(response.history.get('messages', [])[-1].get('tool_outputs', []))
        logging.info(f"Agent run completed. Tool calls: {tool_call_count}, Tool outputs: {tool_output_count}")
        
        return response
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.exception(f"Error running agent {agent_name}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/session/{session_id}")
async def delete_session(session_id: str):
    """Delete a session's message history.
    
    Args:
        session_id: The ID of the session to delete.
        
    Returns:
        Status of the deletion operation.
    """
    try:
        # Get the message store from MessageHistory
        message_store = MessageHistory._store
        
        # Check if session exists
        if not message_store.session_exists(session_id):
            raise HTTPException(
                status_code=404,
                detail=f"Session {session_id} not found"
            )
        
        # Clear the session
        message_store.clear_session(session_id)
        
        logger.info(f"Successfully deleted session: {session_id}")
        
        return DeleteSessionResponse(
            status="success",
            session_id=session_id,
            message="Session history deleted successfully"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting session {session_id}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to delete session: {str(e)}"
        )

@router.get("/session/{session_id}", response_model=SessionResponse, response_model_exclude_none=True)
async def get_session(
    session_id: str,
    page: int = 1,
    page_size: int = 50,
    sort_desc: bool = True,
    hide_tools: bool = False
):
    """Get a session's message history with pagination.
    
    Args:
        session_id: The ID of the session to retrieve.
        page: Page number (1-based).
        page_size: Number of messages per page.
        sort_desc: Sort by most recent first if True.
        hide_tools: If True, excludes tool calls and outputs from the response.
        
    Returns:
        The session's message history with pagination info.
    """
    try:
        # Get message history
        message_history = MessageHistory(session_id)
        
        # Check if session exists
        exists = message_history._store.session_exists(session_id)
        
        if not exists:
            session_response = SessionResponse(
                session_id=session_id,
                messages=[],
                exists=False,
                total_messages=0,
                current_page=1,
                total_pages=0
            )
        else:
            # Get paginated messages
            paginated_messages, total_messages, current_page, total_pages = message_history.get_paginated_messages(
                page=page,
                page_size=page_size,
                sort_desc=sort_desc
            )
            
            # Format messages for API response
            formatted_messages = [
                message for message in (
                    message_history.format_message_for_api(msg, hide_tools=hide_tools)
                    for msg in paginated_messages
                )
                if message is not None
            ]
            
            # Wrap each formatted message dict into a MessageModel to ensure Pydantic processing
            clean_messages = [MessageModel(**msg) for msg in formatted_messages]
            
            session_response = SessionResponse(
                session_id=session_id,
                messages=clean_messages,
                exists=True,
                total_messages=total_messages,
                current_page=current_page,
                total_pages=total_pages
            )
        
        return session_response
    except Exception as e:
        logger.error(f"Error retrieving session {session_id}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve session: {str(e)}"
        ) 