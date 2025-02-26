import logging
from datetime import datetime
from typing import List
import json

from fastapi import APIRouter, HTTPException
from src.agents.models.agent_factory import AgentFactory
from src.config import settings
from src.memory.message_history import MessageHistory
from src.api.models import (
    AgentRunRequest,
    AgentInfo,
    DeleteSessionResponse,
    MessageModel,
    SessionResponse,
    SessionListResponse,
    SessionInfo
)
from src.memory.pg_message_store import PostgresMessageStore
from src.utils.db import execute_query

# Create API router for v1 endpoints
router = APIRouter()

# Get our module's logger
logger = logging.getLogger(__name__)

@router.get("/agent/list", response_model=List[AgentInfo], tags=["Agents"], 
           summary="List Available Agents",
           description="Returns a list of all available agent templates that can be used.")
async def list_agents():
    """List all available agents."""
    return [
        AgentInfo(name=name, type=AgentFactory._agents[name][0].__name__)
        for name in AgentFactory.list_available_agents()
    ]

@router.post("/agent/{agent_name}/run", tags=["Agents"],
            summary="Run Agent",
            description="Execute an agent with the specified name. Optionally provide a session ID to maintain conversation context.")
async def run_agent(agent_name: str, request: AgentRunRequest):
    """Run an agent with the given name."""
    try:
        agent = AgentFactory.get_agent(agent_name)
        
        # Check if session_id is provided
        if not request.session_id:
            # If no session_id is provided, generate a new one
            from src.memory.pg_message_store import PostgresMessageStore
            store = PostgresMessageStore()
            # Generate a new session with an empty string (this will create a new session in the database)
            new_session_id = store._ensure_session_exists("", request.user_id)
            request.session_id = new_session_id
            logger.info(f"Created new session with ID: {new_session_id}")
        else:
            # Check if the provided session exists, if not create it
            from src.memory.pg_message_store import PostgresMessageStore
            store = PostgresMessageStore()
            if not store.session_exists(request.session_id):
                # Create the session with the provided ID
                store._ensure_session_exists(request.session_id, request.user_id)
                logger.info(f"Created session with provided ID: {request.session_id}")
            else:
                logger.info(f"Using existing session: {request.session_id}")
        
        # Store channel_payload in the users table if provided
        if request.channel_payload:
            try:
                # Convert user_id to numeric if possible
                numeric_user_id = 1  # Default
                if request.user_id != "default_user":
                    try:
                        numeric_user_id = int(request.user_id)
                    except ValueError:
                        logger.warning(f"Non-numeric user_id provided: {request.user_id}, using default ID 1")
                
                # Update the user record with the channel_payload
                execute_query(
                    """
                    UPDATE users 
                    SET channel_payload = %s, updated_at = %s
                    WHERE id = %s
                    """,
                    (
                        json.dumps(request.channel_payload),
                        datetime.utcnow(),
                        numeric_user_id
                    ),
                    fetch=False
                )
                logger.info(f"Updated channel_payload for user {numeric_user_id}")
            except Exception as e:
                logger.error(f"Error updating channel_payload for user {request.user_id}: {str(e)}")
        
        # Get message history with user_id
        message_history = MessageHistory(request.session_id, user_id=request.user_id)
        
        # Link the agent to the session in the database
        AgentFactory.link_agent_to_session(agent_name, request.session_id)
        
        if message_history and message_history.messages:
            # Get filtered messages up to the limit
            filtered_messages = message_history.get_filtered_messages(
                message_limit=request.message_limit,
                sort_desc=False  # Sort chronologically for agent processing
            )
            message_history.update_messages(filtered_messages)

        # Get the agent database ID if available
        agent_id = getattr(agent, "db_id", None)
        
        # If agent_id is not set, try to get it from the database
        if agent_id is None:
            from src.agents.models.agent_db import get_agent_by_name
            db_agent = get_agent_by_name(f"{agent_name}_agent" if not agent_name.endswith('_agent') else agent_name)
            if db_agent:
                agent_id = db_agent["id"]
                # Save it back to the agent instance for future use
                agent.db_id = agent_id
                logging.info(f"Found agent ID {agent_id} for agent {agent_name}")
            else:
                logging.warning(f"Could not find agent ID for agent {agent_name}")
        
        # Process the message with additional metadata if available
        message_metadata = {
            "message_type": request.message_type,
            "media_url": request.mediaUrl, 
            "mime_type": request.mime_type
        }
        
        # Log incoming message details
        logger.info(f"Processing message from user {request.user_id} with type: {request.message_type}")
        if request.mediaUrl:
            logger.info(f"Media URL: {request.mediaUrl}, MIME type: {request.mime_type}")
        
        response = await agent.process_message(
            request.message_content,  # Use message_content instead of message_input
            session_id=request.session_id,
            agent_id=agent_id,  # Pass the agent ID to be stored with the messages
            user_id=request.user_id,  # Pass the user ID
            context={**request.context, **message_metadata}  # Include message metadata in context
        )
        
        # Log the tool call and output counts more safely
        messages = response.history.get('messages', [])
        if messages:  # Only try to access if there are messages
            last_message = messages[-1]
            tool_call_count = len(last_message.get('tool_calls', []))
            tool_output_count = len(last_message.get('tool_outputs', []))
            logging.info(f"Agent run completed. Tool calls: {tool_call_count}, Tool outputs: {tool_output_count}")
        else:
            logging.info("Agent run completed. No messages in history.")
        
        return response
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.exception(f"Error running agent {agent_name}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/session/{session_id}", tags=["Sessions"],
              summary="Delete Session",
              description="Delete a session's message history by its ID.")
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
        
        # Clear the session messages
        message_store.clear_session(session_id)
        
        # Also delete the session from the sessions table
        execute_query(
            "DELETE FROM sessions WHERE id = %s",
            (session_id,),
            fetch=False
        )
        
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

@router.get("/session/{session_id}", response_model=SessionResponse, response_model_exclude_none=True, 
           tags=["Sessions"],
           summary="Get Session History",
           description="Retrieve a session's message history with pagination options.")
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

@router.get("/sessions", response_model=SessionListResponse)
async def list_sessions(
    page: int = 1, 
    page_size: int = 50, 
    sort_desc: bool = True
):
    """List all sessions with pagination.
    
    Args:
        page: Page number (1-based).
        page_size: Number of sessions per page.
        sort_desc: Sort by most recent first if True.
        
    Returns:
        List of sessions with pagination info.
    """
    try:
        # Get message store
        message_store = PostgresMessageStore()
        
        # Get all sessions
        result = message_store.get_all_sessions(
            page=page,
            page_size=page_size,
            sort_desc=sort_desc
        )
        
        # Convert to session info objects
        sessions = [SessionInfo(**session) for session in result['sessions']]
        
        # Create response
        response = SessionListResponse(
            sessions=sessions,
            total_count=result['total_count'],
            page=result['page'],
            page_size=result['page_size'],
            total_pages=result['total_pages']
        )
        
        return response
    except Exception as e:
        logger.error(f"Error listing sessions: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to list sessions: {str(e)}"
        ) 