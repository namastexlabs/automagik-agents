import logging
from datetime import datetime
from typing import List, Optional
import json
import math
import uuid
import inspect

from fastapi import APIRouter, HTTPException, Query, Path, Depends, Response
from starlette.responses import JSONResponse
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
    SessionInfo,
    UserCreate,
    UserUpdate,
    UserInfo,
    UserListResponse
)

# Import memory router
from src.api.memory_routes import memory_router
from src.db import execute_query, get_db_connection, get_user_by_identifier, list_users, update_user, list_sessions, create_session
from src.db.connection import generate_uuid, safe_uuid
from psycopg2.extras import RealDictCursor

# Create API router for v1 endpoints
router = APIRouter()

# Include memory router
router.include_router(memory_router)

# Get our module's logger
logger = logging.getLogger(__name__)

# Create an additional helper function for UUID validation
def is_valid_uuid(value: str) -> bool:
    """Check if a string is a valid UUID.
    
    Args:
        value: The string to check
        
    Returns:
        True if the string is a valid UUID, False otherwise
    """
    try:
        uuid.UUID(value)
        return True
    except (ValueError, AttributeError, TypeError):
        return False

@router.get("/agent/list", response_model=List[AgentInfo], tags=["Agents"], 
           summary="List Available Agents",
           description="Returns a list of all available agent templates that can be used.")
async def list_agents():
    """List all available agents."""
    agent_list = []
    for name in AgentFactory.list_available_agents():
        # Get agent type from factory
        agent_type = AgentFactory._agents[name][0].__name__
        
        # Get model and description from database if available
        model = "unknown"
        description = None
        
        try:
            from src.db import get_agent_by_name
            agent = get_agent_by_name(name)
            if agent:
                model = agent.model or "unknown"
                description = agent.description
        except Exception as e:
            logger.warning(f"Error getting agent details from database: {str(e)}")
        
        # Create agent info object with all fields
        agent_info = AgentInfo(
            name=name,
            type=agent_type,
            model=model,
            description=description
        )
        agent_list.append(agent_info)
    
    return agent_list

@router.post("/agent/{agent_name}/run", tags=["Agents"],
            summary="Run Agent",
            description="Execute an agent with the specified name. Optionally provide a session ID or name to maintain conversation context.")
async def run_agent(agent_name: str, request: AgentRunRequest):
    """Run an agent with the given name."""
    try:
        # Get the pre-initialized agent
        agent = AgentFactory.get_agent(agent_name)
        
        # Get session_origin from request
        session_origin = request.session_origin
        
        # Extract session_name if provided
        session_name = request.session_name
        
        # We'll initialize message_history later once we have a valid session_id
        # Removing this initialization to prevent duplicate session creation
        
        # Get the agent database ID if available
        agent_id = getattr(agent, "db_id", None)
        
        # If agent_id is not set, try to get it from the database
        if agent_id is None:
            from src.db import get_agent_by_name
            agent_db = get_agent_by_name(f"{agent_name}_agent" if not agent_name.endswith('_agent') else agent_name)
            if agent_db:
                agent_id = agent_db.id
                # Save it back to the agent instance for future use
                agent.db_id = agent_id
                logging.info(f"Found agent ID {agent_id} for agent {agent_name}")
            else:
                logging.warning(f"Could not find agent ID for agent {agent_name}")
        
        # Check if session name is provided, use it to lookup existing sessions
        if session_name:
            # Look up the session by name
            from src.db import get_session_by_name
            existing_session = get_session_by_name(session_name)
            if existing_session:
                # Found an existing session with this name
                session_id = existing_session.id
                existing_agent_id = existing_session.agent_id
                
                # Check if the session is already associated with a different agent
                if existing_agent_id is not None and existing_agent_id != agent_id:
                    logger.error(f"Session name '{session_name}' is already associated with agent ID {existing_agent_id}, cannot use with agent ID {agent_id}")
                    raise HTTPException(
                        status_code=409,
                        detail=f"Session name '{session_name}' is already associated with a different agent. Please use a different session name."
                    )
                
                # Found an existing session with this name, use it
                request.session_id = str(session_id)
                logger.info(f"Found existing session with name '{session_name}', using ID: {session_id}")
        
        # Check if session_id is provided
        if not request.session_id:
            # If no session_id is provided or no session found with the provided name
            # Create a new session with the session_name if provided
            try:
                # Use the repository pattern to create a session
                from src.db.models import Session
                
                # Create metadata with session_origin if provided
                metadata = {}
                if session_origin:
                    metadata['session_origin'] = session_origin
                
                # Create a Session model
                new_session = Session(
                    id=generate_uuid(),  # Use safe UUID generation
                    user_id=request.user_id,
                    agent_id=agent_id,
                    name=session_name,
                    platform=session_origin or 'web',
                    metadata=metadata
                )
                
                # Create the session using the repository function
                session_id = create_session(new_session)
                if not session_id:
                    logger.error("Failed to create session")
                    raise HTTPException(status_code=500, detail="Failed to create session")
                    
                request.session_id = str(session_id)
                logger.info(f"Created new session with ID: {session_id}, name: {session_name}, and origin: {session_origin}")
            except Exception as e:
                # Check for unique constraint violation
                if "duplicate key value violates unique constraint" in str(e) and "sessions_name_key" in str(e):
                    logger.error(f"Session name '{session_name}' already exists")
                    raise HTTPException(
                        status_code=409,
                        detail=f"Session name '{session_name}' already exists. Please use a different session name."
                    )
                # Re-raise other exceptions
                logger.error(f"Error creating session: {str(e)}")
                raise
        else:
            # Check if request.session_id is a session name instead of a UUID
            session_id = request.session_id
            try:
                # Validate if it's a UUID using our helper function
                if is_valid_uuid(request.session_id):
                    # It's a valid UUID, continue
                    pass
                else:
                    # Not a UUID, raise ValueError to trigger the except block
                    raise ValueError("Not a valid UUID")
            except ValueError:
                # Not a UUID, try to look up by name
                logger.info(f"Looking up session by name: {request.session_id}")
                
                # Use the db function to get session by name
                from src.db import get_session_by_name
                resolved_session = get_session_by_name(request.session_id)
                
                if resolved_session:
                    # Found a session with matching name
                    session_id = resolved_session.id
                    existing_agent_id = resolved_session.agent_id
                    
                    # Check if the session is already associated with a different agent
                    if existing_agent_id is not None and existing_agent_id != agent_id:
                        logger.error(f"Session name '{request.session_id}' is already associated with agent ID {existing_agent_id}, cannot use with agent ID {agent_id}")
                        raise HTTPException(
                            status_code=409,
                            detail=f"Session name '{request.session_id}' is already associated with a different agent. Please use a different session name."
                        )
                    
                    logger.info(f"Found session ID {session_id} for name {request.session_id}")
                else:
                    # Name doesn't exist yet, create a new session with this name
                    try:
                        # Use the repository pattern to create a session
                        from src.db.models import Session
                        
                        # Create metadata with session_origin if provided
                        metadata = {}
                        if session_origin:
                            metadata['session_origin'] = session_origin
                        
                        # Create a Session model
                        new_session = Session(
                            id=generate_uuid(),  # Use safe UUID generation
                            user_id=request.user_id,
                            agent_id=agent_id,
                            name=request.session_id,
                            platform=session_origin or 'web',
                            metadata=metadata
                        )
                        
                        # Create the session using the repository function
                        session_id = create_session(new_session)
                        if not session_id:
                            logger.error("Failed to create session")
                            raise HTTPException(status_code=500, detail="Failed to create session")
                            
                        session_id = str(session_id)
                        logger.info(f"Created new session with ID: {session_id} and name: {request.session_id}")
                    except Exception as e:
                        # Check for unique constraint violation
                        if "duplicate key value violates unique constraint" in str(e) and "sessions_name_key" in str(e):
                            logger.error(f"Session name '{request.session_id}' already exists")
                            raise HTTPException(
                                status_code=409,
                                detail=f"Session name '{request.session_id}' already exists. Please use a different session name."
                            )
                        # Re-raise other exceptions
                        logger.error(f"Error creating session: {str(e)}")
                        raise
                
                # Update the request.session_id with the actual UUID
                request.session_id = str(session_id)
            
            # Initialize message_history with the proper session_id
            message_history = MessageHistory(session_id=request.session_id, user_id=request.user_id)
        
        # Store channel_payload in the users table if provided
        if request.channel_payload:
            try:
                # Use the user_id directly as an integer
                user_id_int = request.user_id
                if user_id_int:
                    # Look up or create user
                    from src.db import User, get_user, create_user, update_user
                    
                    user = get_user(user_id_int)
                    if not user:
                        # Create a new user with this ID
                        user = User(
                            id=user_id_int,
                            user_data={"channel_payload": request.channel_payload}
                        )
                        create_user(user)
                    else:
                        # Update existing user with channel_payload
                        user_data = user.user_data or {}
                        user_data["channel_payload"] = request.channel_payload
                        user.user_data = user_data
                        update_user(user)
                    
                    logger.info(f"Updated user {user_id_int} with channel_payload")
            except Exception as e:
                logger.error(f"Error storing channel_payload for user {request.user_id}: {str(e)}")
        
        # Resolve the agent name to a numeric ID if needed
        try:
            # If agent_id is a string, try to look up the actual agent ID from the database
            if isinstance(agent_id, str) and not agent_id.isdigit():
                from src.db import get_agent_by_name
                agent_db = get_agent_by_name(agent_id)
                if agent_db and agent_db.id:
                    resolved_agent_id = agent_db.id
                    logger.info(f"Resolved agent name '{agent_id}' to numeric ID {resolved_agent_id}")
                    agent_id = resolved_agent_id
        except Exception as e:
            logger.warning(f"Error resolving agent name to ID: {str(e)}")
        
        # Update agent_id in the request
        request.agent_id = agent_id
        
        # Initialize message_history with the proper session_id
        message_history = MessageHistory(session_id=request.session_id, user_id=request.user_id)
        
        # Link the agent to the session in the database
        AgentFactory.link_agent_to_session(agent_name, request.session_id)
        
        # Get filtered messages up to the limit for agent processing
        filtered_messages = None
        if message_history and hasattr(message_history, 'get_filtered_messages'):
            filtered_messages = message_history.get_filtered_messages(
                message_limit=request.message_limit,
                sort_desc=False  # Sort chronologically for agent processing
            )

        # Process the message with additional metadata if available
        message_metadata = {
            "message_type": request.message_type,
            "media_url": request.mediaUrl, 
            "mime_type": request.mime_type
        }
        
        # Create a combined context with all available information
        combined_context = {**request.context, **message_metadata}
        
        # Add channel_payload to context if available
        if request.channel_payload:
            combined_context["channel_payload"] = request.channel_payload
        
        # Log incoming message details
        logger.info(f"Processing message from user {request.user_id} with type: {request.message_type}")
        if request.mediaUrl:
            logger.info(f"Media URL: {request.mediaUrl}, MIME type: {request.mime_type}")
        
        # Prepare multimodal content
        multimodal_content = {}
        
        # Handle legacy single media fields
        if request.mediaUrl and request.mime_type:
            logger.info(f"Processing legacy single media with URL: {request.mediaUrl} and type: {request.mime_type}")
            media_type = "unknown"
            if request.mime_type.startswith("image/"):
                media_type = "image"
                multimodal_content["image_url"] = request.mediaUrl
            elif request.mime_type.startswith("audio/"):
                media_type = "audio"
                multimodal_content["audio_url"] = request.mediaUrl
            elif request.mime_type.startswith(("application/", "text/")):
                media_type = "document"
                multimodal_content["document_url"] = request.mediaUrl
            logger.info(f"Detected media type: {media_type}")
        
        # Handle new multimodal content array
        if request.media_contents:
            logger.info(f"Processing {len(request.media_contents)} multimodal content items")
            for item in request.media_contents:
                if isinstance(item, ImageUrlContent):
                    multimodal_content["image_url"] = item.media_url
                    logger.info(f"Added image URL: {item.media_url}")
                elif isinstance(item, ImageBinaryContent):
                    multimodal_content["image_data"] = item.data
                    logger.info(f"Added binary image data (length: {len(item.data) if item.data else 0})")
                elif isinstance(item, AudioUrlContent):
                    multimodal_content["audio_url"] = item.media_url
                    logger.info(f"Added audio URL: {item.media_url}")
                elif isinstance(item, AudioBinaryContent):
                    multimodal_content["audio_data"] = item.data
                    logger.info(f"Added binary audio data (length: {len(item.data) if item.data else 0})")
                elif isinstance(item, DocumentUrlContent):
                    multimodal_content["document_url"] = item.media_url
                    logger.info(f"Added document URL: {item.media_url}")
                elif isinstance(item, DocumentBinaryContent):
                    multimodal_content["document_data"] = item.data
                    logger.info(f"Added binary document data (length: {len(item.data) if item.data else 0})")

        # If preserve_system_prompt flag is set, check for existing system_prompt in session
        if request.preserve_system_prompt:
            try:
                # Look up existing system_prompt in session metadata
                from src.db import get_session
                existing_session = get_session(uuid.UUID(request.session_id))
                if existing_session and existing_session.metadata:
                    try:
                        metadata = existing_session.metadata
                        if isinstance(metadata, str):
                            metadata = json.loads(metadata)
                            
                        if metadata and "system_prompt" in metadata:
                            # Use the existing system_prompt
                            if hasattr(agent, "system_prompt"):
                                agent.system_prompt = metadata["system_prompt"]
                                logger.info("Using existing system_prompt from session metadata")
                    except Exception as e:
                        logger.error(f"Error retrieving system_prompt from metadata: {str(e)}")
            except Exception as e:
                logger.error(f"Error handling preserve_system_prompt flag: {str(e)}")
        
        try:        
            # Check if the agent's process_message accepts message_already_added parameter
            agent_process_signature = inspect.signature(agent.process_message)
            supports_message_already_added = 'message_already_added' in agent_process_signature.parameters
            
            # Prepare base arguments for all agents
            process_args = {
                "session_id": request.session_id,
                "user_id": request.user_id,
                "context": combined_context,
                "message_history": message_history,  # Pass the existing MessageHistory object
            }
            
            # Only add the message ourselves if the agent supports message_already_added
            if supports_message_already_added:
                # Store the message in the message history
                message_history.add(
                    request.message_content,
                    agent_id=agent_id,
                    context=combined_context
                )
                # Indicate that we've already added the message
                process_args["message_already_added"] = True
            
            # Ensure system_prompt is stored for this session
            if hasattr(agent, "system_prompt") and agent.system_prompt:
                # Store in session metadata if not already present
                try:
                    from src.db import get_session, update_session
                    session = get_session(uuid.UUID(request.session_id))
                    if session:
                        # Get existing metadata or create new dictionary
                        metadata = session.metadata or {}
                        if isinstance(metadata, str):
                            try:
                                import json
                                metadata = json.loads(metadata)
                            except json.JSONDecodeError:
                                metadata = {}
                        
                        # Update system_prompt in metadata if not already set
                        if "system_prompt" not in metadata:
                            metadata["system_prompt"] = agent.system_prompt
                            session.metadata = metadata
                            
                            # Update session
                            update_session(session)
                            logger.info(f"Stored system prompt in session metadata")
                except Exception as e:
                    logger.error(f"Error updating session metadata with system prompt: {str(e)}")
            
            # Process the message with agent
            # Call process_message with appropriate arguments
            response = await agent.process_message(
                request.message_content,
                **process_args
            )
            
            # Return the parsed response
            return {
                "message": response.text,
                "session_id": request.session_id,
                "success": response.success,
                "tool_calls": response.tool_calls,
                "tool_outputs": response.tool_outputs,
            }
        except Exception as e:
            logger.error(f"Error processing message: {e}")
            return JSONResponse(
                status_code=500,
                content={"error": f"Error processing message: {str(e)}"}
            )
    except HTTPException as http_ex:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.error(f"Error running agent {agent_name}: {e}")
        return JSONResponse(
            status_code=500,
            content={"error": f"Error running agent: {str(e)}"}
        )

@router.get("/sessions", response_model=SessionListResponse, tags=["Sessions"],
            summary="List All Sessions",
            description="Retrieve a list of all sessions with pagination options.")
async def list_sessions_route(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(50, ge=1, le=100, description="Items per page"),
    sort_desc: bool = Query(True, description="Sort by most recent first")
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
        logger.info(f"Listing sessions - page={page}, page_size={page_size}, sort_desc={sort_desc}")
        
        # Use the enhanced repository function with pagination
        sessions, total_count = list_sessions(
            page=page,
            page_size=page_size,
            sort_desc=sort_desc
        )
        
        # Calculate total pages
        total_pages = math.ceil(total_count / page_size) if total_count > 0 else 1
        
        # Convert to session info objects
        session_info_list = [
            SessionInfo(
                id=str(session.id),
                name=session.name,
                user_id=session.user_id,
                agent_id=session.agent_id,
                platform=session.platform,
                metadata=session.metadata,
                created_at=session.created_at,
                updated_at=session.updated_at,
                run_finished_at=session.run_finished_at
            ) 
            for session in sessions
        ]
        
        logger.info(f"Found {len(session_info_list)} sessions (total {total_count})")
        
        # Create response
        response = SessionListResponse(
            sessions=session_info_list,
            total_count=total_count,
            page=page,
            page_size=page_size,
            total_pages=total_pages
        )
        
        return response
    except Exception as e:
        logger.error(f"Error listing sessions: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to list sessions: {str(e)}"
        )

@router.get("/sessions/{session_id_or_name}", response_model=SessionResponse, response_model_exclude_none=True, 
           tags=["Sessions"],
           summary="Get Session History",
           description="Retrieve a session's message history with pagination options. You can use either the session ID (UUID) or a session name.")
async def get_session_route(
    session_id_or_name: str,
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(50, ge=1, le=100, description="Items per page"),
    sort_desc: bool = Query(True, description="Sort by most recent first"),
    hide_tools: bool = Query(False, description="Exclude tool calls and outputs")
):
    """Get a session's message history with pagination.
    
    Args:
        session_id_or_name: The ID or name of the session to retrieve.
        page: Page number (1-based).
        page_size: Number of messages per page.
        sort_desc: Sort by most recent first if True.
        hide_tools: If True, excludes tool calls and outputs from the response.
        
    Returns:
        The session's message history with pagination info.
    """
    try:
        logger.info(f"Retrieving session with identifier: {session_id_or_name}")
        
        # Use repository functions to get the session
        from src.db import get_session, get_session_by_name
        
        # Determine if the input is a UUID or session name
        session = None
        try:
            # Try to parse as UUID using our helper
            if is_valid_uuid(session_id_or_name):
                session_id = uuid.UUID(session_id_or_name)
                logger.info(f"Looking up session by ID: {session_id}")
                session = get_session(session_id)
        except ValueError:
            # Not a UUID, try to look up by name
            logger.info(f"Looking up session by name: {session_id_or_name}")
            session = get_session_by_name(session_id_or_name)
        
        # Check if session exists
        if not session:
            logger.warning(f"Session not found with identifier: {session_id_or_name}")
            return SessionResponse(
                session_id=session_id_or_name,
                messages=[],
                exists=False,
                total_messages=0,
                current_page=1,
                total_pages=0
            )
        
        session_id = session.id
        logger.info(f"Found session with ID: {session_id}")
        
        # Get message history
        message_history = MessageHistory(str(session_id))
        
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
            session_id=str(session_id),
            messages=clean_messages,
            exists=True,
            total_messages=total_messages,
            current_page=current_page,
            total_pages=total_pages
        )
        
        return session_response
    except Exception as e:
        logger.error(f"Error retrieving session {session_id_or_name}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve session: {str(e)}"
        )

@router.delete("/sessions/{session_id_or_name}", tags=["Sessions"],
              summary="Delete Session",
              description="Delete a session's message history by its ID or name.")
async def delete_session_route(session_id_or_name: str):
    """Delete a session by ID or name."""
    try:
        # First determine if the input is a UUID or a name
        try:
            # Try to parse as UUID using our helper
            if is_valid_uuid(session_id_or_name):
                session_id = uuid.UUID(session_id_or_name)
                # It's a valid UUID, use it directly
                from src.db import get_session, delete_session, delete_session_messages
                
                # Get the session to verify it exists
                session = get_session(session_id)
                if not session:
                    return JSONResponse(
                        status_code=404,
                        content={"error": f"Session with ID {session_id_or_name} not found"}
                    )
                    
                # Delete all messages first
                delete_session_messages(session_id)
                
                # Then delete the session itself
                success = delete_session(session_id)
                
                if success:
                    return {"status": "success", "message": f"Session {session_id_or_name} deleted successfully"}
                else:
                    return JSONResponse(
                        status_code=500,
                        content={"error": f"Failed to delete session {session_id_or_name}"}
                    )
                
        except ValueError:
            # Not a valid UUID, try to find by name
            from src.db import get_session_by_name, delete_session, delete_session_messages
            
            # Get the session to verify it exists and get its ID
            session = get_session_by_name(session_id_or_name)
            if not session:
                return JSONResponse(
                    status_code=404,
                    content={"error": f"Session with name '{session_id_or_name}' not found"}
                )
                
            session_id = session.id
                
            # Delete all messages first
            delete_session_messages(session_id)
            
            # Then delete the session itself
            success = delete_session(session_id)
            
            if success:
                return {"status": "success", "message": f"Session '{session_id_or_name}' deleted successfully"}
            else:
                return JSONResponse(
                    status_code=500,
                    content={"error": f"Failed to delete session '{session_id_or_name}'"}
                )
    except Exception as e:
        logger.error(f"Error deleting session {session_id_or_name}: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"error": f"Failed to delete session: {str(e)}"}
        )

# User management endpoints
@router.get("/users", response_model=UserListResponse, tags=["Users"],
           summary="List Users",
           description="Returns a paginated list of users.\n\n**Requires Authentication**: This endpoint requires an API key.")
async def list_users_route(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page")
):
    """List all users with pagination."""
    try:
        logger.info(f"Listing users - page={page}, page_size={page_size}")
        
        # Use the repository function
        users, total_count = list_users(page=page, page_size=page_size)
        
        # Create the response
        user_list = [
            UserInfo(
                id=user.id,
                email=user.email,
                phone_number=user.phone_number,
                user_data=user.user_data,
                created_at=user.created_at,
                updated_at=user.updated_at
            )
            for user in users
        ]
        
        # Calculate pagination metadata
        total_pages = math.ceil(total_count / page_size) if total_count > 0 else 1
        has_next = page < total_pages
        has_prev = page > 1
        
        logger.info(f"Found {len(user_list)} users (total {total_count})")
        
        # Return paginated response
        return UserListResponse(
            users=user_list,
            total=total_count,
            page=page,
            page_size=page_size,
            has_next=has_next,
            has_prev=has_prev
        )
    except Exception as e:
        logger.error(f"Error listing users: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.post("/users", response_model=UserInfo, tags=["Users"],
            summary="Create User",
            description="Creates a new user with email, phone_number, and/or user_data fields.\n\n**Requires Authentication**: This endpoint requires an API key.")
async def create_user_route(user_create: UserCreate):
    """Create a new user."""
    try:
        # Need at least one identifier - email or phone_number
        if not user_create.email and not user_create.phone_number:
            raise HTTPException(status_code=400, detail="At least one of email or phone_number must be provided")

        logger.info(f"Creating user with email: {user_create.email}, phone_number: {user_create.phone_number}")
        if user_create.user_data:
            logger.info(f"User data: {json.dumps(user_create.user_data)}")
        
        # Create a User model from the UserCreate data
        from src.db.models import User
        from src.db import create_user
        
        user = User(
            email=user_create.email,
            phone_number=user_create.phone_number,
            user_data=user_create.user_data
        )
        
        # Use the repository function to create the user
        user_id = create_user(user)
        
        if not user_id:
            logger.error("Failed to create user")
            raise HTTPException(status_code=500, detail="Failed to create user")
        
        # Get the created user
        from src.db import get_user
        created_user = get_user(user_id)
        
        if not created_user:
            logger.error(f"Could not retrieve created user with ID: {user_id}")
            raise HTTPException(status_code=500, detail="User was created but could not be retrieved")
        
        logger.info(f"User created with ID: {created_user.id}")
        
        # Return user info
        return UserInfo(
            id=created_user.id,
            email=created_user.email,
            phone_number=created_user.phone_number,
            user_data=created_user.user_data,
            created_at=created_user.created_at,
            updated_at=created_user.updated_at
        )
    except HTTPException as e:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.error(f"Error creating user: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.get("/users/{user_identifier}", response_model=UserInfo, tags=["Users"],
            summary="Get User",
            description="Returns details for a specific user by ID, email, or phone number.\n\n**Requires Authentication**: This endpoint requires an API key.")
async def get_user_route(user_identifier: str = Path(..., description="The user ID, email, or phone number")):
    """Get user details by ID, email, or phone number."""
    try:
        logger.info(f"Looking up user with identifier: {user_identifier}")
        
        # Use the repository function instead of direct SQL
        user = get_user_by_identifier(user_identifier)
        
        # Check if user exists
        if not user:
            logger.warning(f"User not found with identifier: {user_identifier}")
            raise HTTPException(status_code=404, detail=f"User not found with identifier: {user_identifier}")
        
        # Log the found user details
        logger.info(f"Found user with ID: {user.id}")
        logger.info(f"  Email: {user.email}")
        logger.info(f"  Phone number: {user.phone_number}")
        
        # Return user info
        return UserInfo(
            id=user.id,
            email=user.email,
            phone_number=user.phone_number,
            user_data=user.user_data,
            created_at=user.created_at,
            updated_at=user.updated_at
        )
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.error(f"Error retrieving user: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.put("/users/{user_identifier}", response_model=UserInfo, tags=["Users"],
            summary="Update User",
            description="Updates an existing user identified by ID, email, or phone number.\n\n**Requires Authentication**: This endpoint requires an API key.")
async def update_user_route(user_update: UserUpdate, user_identifier: str = Path(..., description="The user ID, email, or phone number")):
    """Update an existing user."""
    try:
        logger.info(f"Updating user with identifier: {user_identifier}")
        logger.info(f"Update data: email={user_update.email}, phone_number={user_update.phone_number}")
        if user_update.user_data:
            logger.info(f"user_data={json.dumps(user_update.user_data)}")
        
        # Find the user using the repository function
        from src.db import get_user_by_identifier, update_user, get_user
        
        # Get the existing user
        user = get_user_by_identifier(user_identifier)
        
        # Check if user exists
        if not user:
            logger.warning(f"User not found with identifier: {user_identifier}")
            raise HTTPException(status_code=404, detail=f"User not found with identifier: {user_identifier}")
        
        logger.info(f"Found user with ID: {user.id}")
        
        # Update the user fields with new data if provided
        if user_update.email is not None:
            user.email = user_update.email
            
        if user_update.phone_number is not None:
            user.phone_number = user_update.phone_number
            
        if user_update.user_data is not None:
            user.user_data = user_update.user_data
        
        # Use the repository function to update the user
        updated_user_id = update_user(user)
        
        if not updated_user_id:
            logger.error(f"Failed to update user with ID: {user.id}")
            raise HTTPException(status_code=500, detail="Failed to update user")
        
        # Get the updated user
        updated_user = get_user(updated_user_id)
        
        if not updated_user:
            logger.error(f"Could not retrieve updated user with ID: {updated_user_id}")
            raise HTTPException(status_code=500, detail="User was updated but could not be retrieved")
        
        logger.info(f"User updated - ID: {updated_user.id}")
        
        return UserInfo(
            id=updated_user.id,
            email=updated_user.email,
            phone_number=updated_user.phone_number,
            user_data=updated_user.user_data,
            created_at=updated_user.created_at,
            updated_at=updated_user.updated_at
        )
    except HTTPException as e:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.error(f"Error updating user: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.delete("/users/{user_identifier}", response_model=DeleteSessionResponse, tags=["Users"],
               summary="Delete User",
               description="Deletes a user account by ID, email, or phone number.\n\n**Requires Authentication**: This endpoint requires an API key.")
async def delete_user_route(user_identifier: str = Path(..., description="The user ID, email, or phone number")):
    """Delete a user account by ID, email, or phone number."""
    try:
        logger.info(f"Attempting to delete user with identifier: {user_identifier}")
        
        # Find the user using the repository function
        from src.db import get_user_by_identifier, delete_user
        
        # Get the user to delete
        user = get_user_by_identifier(user_identifier)
        
        # Check if user exists
        if not user:
            logger.warning(f"User not found with identifier: {user_identifier}")
            raise HTTPException(status_code=404, detail=f"User not found with identifier: {user_identifier}")
        
        user_id = user.id
        logger.info(f"Found user with ID: {user_id}")
        
        # Use the repository function to delete the user
        success = delete_user(user_id)
        
        if not success:
            logger.error(f"Failed to delete user with ID: {user_id}")
            raise HTTPException(status_code=500, detail=f"Failed to delete user with ID: {user_id}")
        
        logger.info(f"Successfully deleted user with ID: {user_id}")
        
        # Return a successful response
        return DeleteSessionResponse(
            status="success",
            session_id=str(user_id),  # Use the session_id field to return the user_id
            message=f"User with ID {user_id} deleted successfully"
        )
    except Exception as e:
        logger.error(f"Error deleting user: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}") 